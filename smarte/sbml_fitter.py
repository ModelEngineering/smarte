"""
 Created on July 2 2022

@author: joseph-hellerstein

Fits an SBML model using one or more fitting algorithms.
Provides statistics on fitting collections of BioModels.
Synthetic data are
"""

import smarte
import smarte.constants as cn
import fitterpp as fpp
import SBMLModel as mdl

import SBMLModel as mdl
import copy
import fitterpp as fpp
import lmfit
import numpy as np
import os
import pandas as pd
import tellurium as te
import typing

F_MIN = 0.5
F_MAX = 2
F_VALUE = F_MIN


class SBMLFitter():

    def __init__(self, model_reference:str,
          parameters:lmfit.Parameters,
          data,
          fitter_methods=None, is_collect=False,
          start_time= cn.START_TIME, end_time=cn.END_TIME,
          point_density=10):
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
        is_collect: bool
            collect fitting statistics
        point_density: float
            number of points simulated for each time unit

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
        # Set up the fitter
        self.fitter = fpp.Fitterpp(self._simulate, self.parameters, self.data_ts,
              methods=fitter_methods, is_collect=is_collect)

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
            except:
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
            columns = list(self.data_columns)
            columns.append(cn.TIME)
            arr = self.model.roadrunner.simulate(self.start_time,
                  self.end_time, self.num_point, columns)
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
        value_dct = dict(self.fitter.final_params.valuesdict())
        error_dct = {n: np.nan if v == 0 else (parameter_dct[n] - v)/parameter_dct[n]
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
        dct["avg_err"] = abs_ser.mean()
        dct["max_err"] = abs_ser.max()
        dct["min_err"] = abs_ser.min()
        df_stats = self.fitter.plotPerformance(is_plot=False)
        indices = list(df_stats.index)
        dct["method"] = indices[0]
        dct["tot_time"] = df_stats.loc[indices[0], "tot"]
        dct["avg_time"] = df_stats.loc[indices[0], "avg"]
        dct["cnt"] = df_stats.loc[indices[0], "cnt"]
        dct["num_species"] = len(self.model.species_names)
        dct["num_parameters"] = len(self.model.parameter_names)
        dct["num_reactions"] = len(self.model.reaction_names)
        dct["status"] = "success!"
        return dct

    @classmethod
    def evaluateBiomodelFit(cls, model_num, noise_mag):
        """
        Compares the fitted and actual values of model parameters for a BioModel.
        Statistics are reported for the first methond only.
    
        Parameters
        ----------
        model_num: int/Model (model number in data directory)
        noise_mag: float (standard deviation added to true model)
        
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
        """
        if "Model" in str(type(model_num)):
            model = model_num
        else:
            model = mdl.Model.getBiomodel(model_num)
        observed_ts = model.simulate(noise_mag=noise_mag)
        # Construct true parameters
        parameter_dct = model.get(model.parameter_names)
        if len(parameter_dct) > 0:
            evaluate_parameters = fpp.dictToParameters(parameter_dct,
                min_frac=F_MIN, max_frac=F_MAX, value_frac=F_VALUE)
            true_parameters = fpp.dictToParameters(parameter_dct)
            # Do the fit and evaluation
            sfitter = cls(model, evaluate_parameters, observed_ts, is_collect=True)
            true_parameters = sfitter.subsetToMuteableParameters(true_parameters)
            if len(true_parameters) > 0:
                dct = sfitter.evaluateFit(true_parameters)
                dct["biomodel_num"] = model.biomodel_num
                dct["noise_mag"] = noise_mag
            else:
                dct = {}
        else:
            dct = {}
        return dct
