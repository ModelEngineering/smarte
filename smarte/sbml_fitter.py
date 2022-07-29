"""
 Created on July 2 2022

@author: joseph-hellerstein

Core logic of SMARTE.

"""

import smarte
import smarte.constants as cn

import analyzeSBML as anl
import copy
import fitterpp as fpp
import lmfit
import numpy as np
import os
import pandas as pd
import tellurium as te
import typing


PREFIX = "BIOMD0000000%03d.xml"


class SBMLFitter():

    def __init__(self, model_reference:str,
          parameters:lmfit.Parameters,
          data,
          fitter_methods=None,
          start_time= cn.START_TIME, end_time=cn.END_TIME,
          point_density=10):
        """
        Constructs estimates of parameter values.

        Parameters
        ----------
        model_reference: ExtendedRoadRunner/str
            roadrunner model or antimony model
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

        Usage
        -----
        smarte = SBMLFitter(roadrunnerModel, parameters, "observed.csv")
        core.fit()  # Do the fit
        """
        self.model = anl.Model(model_reference)
        self.data_ts = anl.Timeseries(data)
        self.data_columns = list(self.data_ts.columns)  # non-time columns
        self.parameters = self._findValidParameters(parameters)
        self.end_time = end_time
        self.start_time = start_time
        self.num_point = int(point_density*(self.end_time - start_time)) + 1
        # Set up the fitter
        self.fitter = fpp.Fitterpp(self._simulate, self.parameters, self.data_ts,
              methods=fitter_methods)

    def _findValidParameters(self, parameters):
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
            try:
                self.model.set({name: value})
                new_parameters.add(parameters.get(name))
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
            result = anl.Timeseries(arr)
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

    def evaluate(self, true_parameters):
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

    @staticmethod
    def getModelFromDataPath(model_num):
        """
        Gets a numbered model.

        Parameters
        ----------
        model_num: int
        
        Returns
        -------
        Model
        """
        return Model(os.path.join(cn.DATA_DIR, PREFIX % model_num))
