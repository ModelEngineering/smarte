"""
 Created on July 2 2022

@author: joseph-hellerstein

Fits an SBML model using one or more fitting algorithms.
Provides statistics on fitting collections of BioModels.
Synthetic data are
"""

import smarte.constants as cn
import fitterpp as fpp
import SBMLModel as mdl

import lmfit
import numpy as np
import pandas as pd

MIN_FRAC = 0.5
MAX_FRAC = 2


class SBMLFitter():

    def __init__(self, model_reference:str,
          parameters:lmfit.Parameters,
          data,
          start_time= cn.START_TIME, end_time=cn.END_TIME,
          point_density=10, **fitterpp_opt):
        """
        Constructs estimates of parameter values. Only muteable parameters are
        considered.

        Parameters
        ----------
        model_reference: ExtendedRoadRunner/str
            roadrunner model or antimony model or Model object
        data: DataFrame or Timeseries or NamedArray or csv file
            Column names must be the same as the names used in roadrunner output.
            For example, the chemical species "GLU" is denoted by "[GLU]"
        parameters: lmfit.Parameters
            range and initial values of parameters
        fitting_methods: list-str (e.g., ["differential_evolution", "leastsq"])
        start_time: float
            start time for the simulation
        end_time: float
            end time for the simulation
        point_density: float
            number of points simulated for each time unit
        fitterpp_opt: dict
            options for Fitterpp constructor

        Usage
        -----
        smarte = SBMLFitter(roadrunnerModel, parameters, "observed.csv")
        core.fit()  # Do the fit
        """
        if isinstance(model_reference, mdl.Model):
            self.model = model_reference
        else:
            self.model = mdl.Model(model_reference)
        self.data_ts = mdl.Timeseries(data)
        self.data_columns = list(self.data_ts.columns)  # non-time columns
        self.parameters = self.subsetToMuteableParameters(parameters)
        self.end_time = end_time
        self.start_time = start_time
        self.num_point = int(point_density*(self.end_time - start_time)) + 1
        # Calculate standard deviations
        self.full_columns = list(self.data_columns)
        if cn.TIME not in self.full_columns:
            self.full_columns.append(cn.TIME)
        self.std_ser = self.model.calculateStds(self.start_time, self.end_time,
              self.num_point, self.full_columns)
        # Set up the fitter
        self.fitter = fpp.Fitterpp(self._simulate, self.parameters, self.data_ts,
              **fitterpp_opt)

    def subsetToMuteableParameters(self, parameters):
        """
        Returns a subset of parameters that can be modified.

        Parameters
        ----------
        parameters: lmfit.Parameters(parameters to evaluate)

        Returns
        -------
        lmfit.Parameters
        """
        parameter_dct = parameters.valuesdict()
        new_parameters = lmfit.Parameters()
        for name, value in parameter_dct.items():
            if np.isclose(value, 0.0):
                continue
            try:
                self.model.set({name: value})
                parameter = parameters.get(name)
                new_parameters.add(parameter)
            except Exception:
                continue
        return new_parameters

    def _simulate(self, is_dataframe=False, **parameter_dct):
        """
        Runs the simulation for particular parameter values.

        Parameters
        ----------
        parameter_dct:
            key: parameter name
            value: value assigned

        Returns
        -------
        Timeseries if is_dataframe
            columns: columns in data
            index: time in ms
        numpy.array if not is_dataframe
            columns: columns in data
        """
        # Set the value of the parameters
        self.model.set(parameter_dct)
        # Run the simulation
        self.model.roadrunner.reset()
        if is_dataframe:
            arr = self.model.simulate(self.start_time,
                  self.end_time, self.num_point, self.full_columns)
            result = mdl.Timeseries(arr)
        else:
            result = self.model.roadrunner.simulate(self.start_time,
                  self.end_time, self.num_point, self.data_columns)
        return result

    def fit(self):
        """
        Fits the model by adjusting values of parameters based on
        differences between simulated and provided values of
        floating species.

        Example
        -------
        sfitter = Smarte(sbml_model, data)
        sfitter.fit(parameters)
        """
        self.fitter.execute()

    def getAccuracies(self, true_parameters):
        """
        Evaluates the accuracy of a fit by comparing fitted values with the
        true value of parameters.

        Parameters
        ----------
        true_parameters: lmfit.Parameters

        Returns
        -------
        pd.Series
            index: parameter name
            value: fractional deviation from true value
        """
        if self.fitter is None:
            self.fit()
        parameter_dct = true_parameters.valuesdict()
        self.fit()
        if self.fitter.final_params is None:
            error_dct = {n: np.nan n in true_parameters.valuesdict().keys()}
        else:
            value_dct = dict(self.fitter.final_params.valuesdict())
            error_dct = {n: np.nan if v == 0 else np.log2(v/parameter_dct[n])
                   for n, v in value_dct.items()}
        # Calculate estimation errors
        return pd.Series(error_dct, index=value_dct.keys())

    def evaluateFit(self, true_parameters):
        """
        Calculates fitter statistics.

        Parameters
        ----------
        true_parameters: lmfit.Parameters

        Returns
        -------
        dict
            avg_err: average error in parameter estimation
            avg_time: average time for an evaluation
            cnt: count of instances ran
            max_err: largest error in parameter estimation
            method: evaluation method
            min_err: smallest error in parameter estimation
            num_species: number of floating species
            num_reactions: number of reactions
            num_parameters: number of parameters
            status: str (result of running)
            tot_time: total run time
        """
        true_parameters = self.subsetToMuteableParameters(true_parameters)
        ser = self.getAccuracies(true_parameters)
        abs_ser = ser.apply(lambda v: np.abs(v))
        indices = list(abs_ser.index)
        dct = {}
        sorted_values = sorted(ser.values, key=lambda v: np.abs(v))
        dct[cn.SD_MEDIAN_ERR] = ser.median()
        dct[cn.SD_MAX_ERR] = sorted_values[-1]
        dct[cn.SD_MIN_ERR] = sorted_values[0]
        df_stats = self.fitter.plotPerformance(is_plot=False)
        indices = list(df_stats.index)
        dct[cn.SD_METHOD] = indices[0]
        dct[cn.SD_TOT_TIME] = df_stats.loc[indices[0], "tot"]
        dct[cn.SD_AVG_TIME] = df_stats.loc[indices[0], "avg"]
        dct[cn.SD_CNT] = df_stats.loc[indices[0], "cnt"]
        dct[cn.SD_NUM_SPECIES] = len(self.model.species_names)
        dct[cn.SD_NUM_PARAMETER] = len(self.model.parameter_names)
        dct[cn.SD_NUM_REACTION] = len(self.model.reaction_names)
        dct[cn.SD_STATUS] = "Success!"
        return dct

    @classmethod
    def evaluateBiomodelFit(cls, model_num, observed_ts,
           range_min_frac=0.5, range_max_frac=2.0, initial_value_frac=0,
           **fitterpp_opt):
        """
        Compares the fitted and actual values of model parameters for a BioModel.
        Statistics are reported for the first methond only.
        Returns a status if fail.

        Parameters are calculated as follows:
            min = true_value*range_min_frac
            max = true_value*range_max_frac
            value = true_value*initial_value_frac

        Parameters
        ----------
        model_num: int/Model (model number in data directory)
        observed_ts: Timeseries
            data used for parameter estimation
        range_min_frac: float
        range_max_frac: float
        Initial_value: float in [0, 1]
        fitterpp_opt: dict (options for Fitterpp constructor)

        Returns
        -------
        dict
            avg_err: average error in parameter estimation
            avg_time: average time for an evaluation
            cnt: count of instances ran
            max_err: largest error in parameter estimation
            method: evaluation method
            min_err: smallest error in parameter estimation
            num_species: number of floating species
            num_reactions: number of reactions
            num_parameters: number of parameters
            tot_time: total run time
            biomodel_num: number of the biomodel
            noise_mag: magnitude of the noise used
            status: str (reason for failure)
        """
        dct = {}
        success = True
        if "Model" in str(type(model_num)):
            model = model_num
        else:
            try:
                model = mdl.Model.getBiomodel(model_num)
                if model is None:
                    success = False
            except Exception:
                success = False
        if not success:
            dct[cn.SD_STATUS] = "Could not construct model."
            return dct
        # Construct true parameters
        fitterpp_opt = dict(fitterpp_opt)
        fitterpp_opt["is_collect"] = True
        parameter_dct = model.get(model.parameter_names)
        if (len(parameter_dct) > 0) and (len(model.species_names) > 0):
            evaluate_parameters = fpp.dictToParameters(parameter_dct,
                min_frac=range_min_frac, max_frac=range_max_frac,
                value_frac=initial_value_frac)
            true_parameters = fpp.dictToParameters(parameter_dct)
            # Do the fit and evaluation
            try:
                sfitter = cls(model, evaluate_parameters, observed_ts,
                      **fitterpp_opt)
                true_parameters = sfitter.subsetToMuteableParameters(
                      true_parameters)
                if len(true_parameters) > 0:
                    dct = sfitter.evaluateFit(true_parameters)
                    dct[cn.SD_BIOMODEL_NUM] = model.biomodel_num
                else:
                    dct[cn.SD_STATUS] = "No muteable parameters."
            except (RuntimeError, IndexError):
                dct[cn.SD_STATUS] = "Could not construct fitter."
        else:
            dct[cn.SD_STATUS] = "No parameters or no floating species."
        return dct

    @classmethod
    def makeBiomodelSyntheticData(cls, model_num, noise_mag, num_dataset=1):
        """
        Generates synthetic observational data for a model.

        Parameters
        ----------
        model_num: int/Model (model number in data directory)
        noise_mag: float
            range of values (in units of std) added to the true simulation

        Returns
        -------
        list-Timeseries
        """
        results = []
        #
        success = True
        if "Model" in str(type(model_num)):
            model = model_num
        else:
            try:
                model = mdl.Model.getBiomodel(model_num)
                if model is None:
                    success = False
            except Exception:
                success = False
        if not success:
            return results
        # Prepare data for evaluation
        for _ in range(2*num_dataset):
            if len(results) >= num_dataset:
                break
            observed_ts = model.simulate(noise_mag=noise_mag,
                  std_ser=model.calculateStds())
            results.append(observed_ts)
        #
        return results
