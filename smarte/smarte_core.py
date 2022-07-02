"""
 Created on July 2 2022

@author: joseph-hellerstein

Core logic of SMARTE.

TODO:
1. Do fit using only lmfit
2. Do fit using initial lmfit and SMARTE
"""

import smarte
import smarte.constants as cn
import analyzeSBML as anl

import copy
import lmfit
import numpy as np
import tellurium as te
import typing


class SmarteCore():

    def __init__(self, model_reference, observed_data, parameters_to_fit=None,
          endTime=None,
          selected_columns=None,
          ):
        """
        Constructs estimates of parameter values.

        Parameters
        ----------
        endTime: float
            end time for the simulation
        model_reference: ExtendedRoadRunner/str
            roadrunner model or antimony model
        observed_data: DataFrame or Timeseries or NamedArray
        parameters_to_fit: list-str/SBstoat.Parameter/None
            parameters in the model that you want to fit
            if None, no parameters are fit
        selected_columns: list-str
            species names you wish use to fit the model
            default: all columns in observed_data

        Usage
        -----
                          ]
        core = SmarteCore(roadrunnerModel, "observed.csv",
            parameters_to_fit=parameters_to_fit)
        core.fit()  # Do the fit
        """
        self.model = anl.Model(model_reference)
        self.observed_data_ts = anl.Timeseries(observed_data)
        self.parameters_to_fit = parameters_to_fit

    def updateFittedAndResiduals(self, **kwargs)->np.ndarray:
        """
        Updates values of self.fittedTS and self.residualsTS
        based on self.params.

        Parameters
        ----------
        kwargs: dict
            arguments for simulation

        Instance Variables Updated
        --------------------------
        self.fittedTS
        self.residualsTS

        Returns
        -------
        1-d ndarray of residuals
        """
        self.fittedTS = self.simulate(**kwargs)  # Updates self.fittedTS
        if self._selectedIdxs is None:
            self._updateSelectedIdxs()
        self.fittedTS = self.fittedTS[self._selectedIdxs]
        residualsArr = self.calcResiduals(self.params)
        numRow = len(self.fittedTS)
        numCol = len(residualsArr)//numRow
        residualsArr = np.reshape(residualsArr, (numRow, numCol))
        cols = self.selected_columns
        if self.residualsTS is None:
            self.residualsTS = self.observedTS.subsetColumns(cols)
        self.residualsTS[cols] = residualsArr

    @staticmethod
    def selectCompatibleIndices(bigTimes, smallTimes):
        """
        Finds the indices such that smallTimes[n] is close to bigTimes[indices[n]]

        Parameters
        ----------
        bigTimes: np.ndarray
        smalltimes: np.ndarray

        Returns
        np.ndarray
        """
        indices = []
        for idx, _ in enumerate(smallTimes):
            distances = (bigTimes - smallTimes[idx])**2
            def getValue(k):
                return distances[k]
            thisIndices = sorted(range(len(distances)), key=getValue)
            indices.append(thisIndices[0])
        return np.array(indices)

    def calcResiduals(self, params)->np.ndarray:
        """
        Compute the residuals between objective and experimental data
        Handle nan values in observedTS. This internal-only method
        is implemented to maximize efficieency.

        Parameters
        ----------
        params: lmfit.Parameters
            arguments for simulation

        Returns
        -------
        1-d ndarray of residuals
        """
        if self._selectedIdxs is None:
            self._updateSelectedIdxs()
        dataArr = ModelFitterCore.runSimulationNumpy(parameters=params,
              model_reference=self.roadrunnerModel,
              startTime=self.observedTS.start,
              endTime=self.endTime,
              numPoint=self.numPoint,
              selected_columns=self.selected_columns,
              _logger=self.logger,
              _loggerPrefix=self._loggerPrefix)
        if dataArr is None:
            residualsArr = np.repeat(LARGE_RESIDUAL, len(self._observedArr))
        else:
            truncatedArr = dataArr[self._selectedIdxs, 1:]
            truncatedArr = truncatedArr.flatten()
            residualsArr = self._observedArr - truncatedArr
            if self._isObservedNan:
                residualsArr = np.nan_to_num(residualsArr)
        return residualsArr

    def fit(self, params:lmfit.Parameters=None):
        """
        Fits the model by adjusting values of parameters based on
        differences between simulated and provided values of
        floating species.

        Parameters
        ----------
        params: lmfit.parameters
            starting values of parameters

        Example
        -------
        f.fitModel()
        """
        if params is None:
            params = self.params
        self.initializeRoadRunnerModel()
        if self.parameters_to_fit is not None:
            self.optimizer = Optimizer.optimize(self.calcResiduals, params,
                  self._fitterMethods, logger=self.logger,
                  numRestart=self._numRestart)
            self.minimizerResult = self.optimizer.minimizerResult
        # Ensure that residualsTS and fittedTS match the parameters
        self.updateFittedAndResiduals(params=self.params)
