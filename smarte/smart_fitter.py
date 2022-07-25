"""
 Created on July 2 2022

@author: joseph-hellerstein

Core logic of SMARTE.

TODO:
2. Do fit using initial lmfit and SMARTE
3. Optionally specify ouput columns 
"""

import smarte
import smarte.constants as cn
import analyzeSBML as anl

import copy
import lmfit
import numpy as np
import tellurium as te
import typing


END_TIME = 5


class SmartFitter():

    def __init__(self, model_reference:str, data:pd.DataFrame, parameters:lmfit.Parameters,
          fitter_methods=None, end_time=END_TIME):
        """
        Constructs estimates of parameter values.

        Parameters
        ----------
        model_reference: ExtendedRoadRunner/str
            roadrunner model or antimony model
        data: DataFrame or Timeseries or NamedArray or csv file
        params: lmfit.parameters
            range and initial values of parameters
        fitting_methods: list-str (e.g., ["differential_evolution", "leastsq"])
        end_time: float
            end time for the simulation

        Usage
        -----
                          ]
        smarte = SmarteCore(roadrunnerModel, "observed.csv",
            parameters_to_fit=parameters_to_fit)
        core.fit()  # Do the fit
        """
        self.model = anl.Model(model_reference)
        self.data_ts = anl.Timeseries(data)
        self.data_columns = list(self.data_ts.columns)  # non-time columns
        self.parameters = parameters
        self.end_time = end_time
        self.num_point = int(self.point_density*self.end_time)
        # Set up the fitter
        self.fitter = Fitterpp(self._simulate, self.parameters, self.data_df, methods=fitter_methods)
     
    def _simulate(self, is_dataframe=True, **parameter_dct):
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
        """
        # Set the value of the parameters
        self.model.set(parameter_dct)
        # Run the simulation
        self.model.roadrunner.reset()
        if is_dataframe:
            result = self.model.simulate(0, self.end_time, self.num_point,
                  self.data_columns)
        else:
            columns = list(self.data_columns)
            columns.append(cn.TIME)
            arr = self.model.simulate(0, self.end_time, self.num_point,
                  columns)
            result = Timeseries(arr)
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
        self.fitter = Fitterpp(self._simulate, parameters, self.data_df)
        self.fitter.execute()
