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
import tellurium as te
import typing


class SBMLFitter():

    def __init__(self, model_reference:str, data,
          parameters:lmfit.Parameters, fitter_methods=None,
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
        smarte = SBMLFitter(roadrunnerModel, "observed.csv",
            parameters_to_fit=parameters_to_fit)
        core.fit()  # Do the fit
        """
        self.model = anl.Model(model_reference)
        self.data_ts = anl.Timeseries(data)
        self.data_columns = list(self.data_ts.columns)  # non-time columns
        self.parameters = parameters
        self.end_time = end_time
        self.start_time = start_time
        self.num_point = int(point_density*(self.end_time - start_time)) + 1
        # Set up the fitter
        self.fitter = fpp.Fitterpp(self._simulate, self.parameters, self.data_ts,
              methods=fitter_methods)
     
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
            arr = self.model.simulate(self.start_time, self.end_time, self.num_point,
                  columns)
            result = anl.Timeseries(arr)
        else:
            result = self.model.roadrunner.simulate(self.start_time, self.end_time,
                  self.num_point, self.data_columns)
        return result

    def fit(self, parameters:lmfit.Parameters, fitting_methods=None):
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
