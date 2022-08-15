"""Description of an experimental condition, items controlled in an experiment."""

"""
An ExperimentCondition is a specification of a level for all factors. This is represented
as a dictionary where the keys are factors and their value is a level.
"""

import smarte.constants as cn
from smarte.extended_dict import ExtendedDict
from smarte.iterate_dict import iterateDict

import pandas as pd
import os


class ExperimentCondition(ExtendedDict):

    def __init__(self, 
          biomodel_num=cn.SD_CONDITION_VALUE_ALL,
          method="differential_evolution",
          noise_mag=0,
          range_min_frac=0.5,
          range_max_frac=2,
          range_initial_frac=0.5,
          columns_deleted=0,
          max_fev=1000,
          ts_instance=cn.SD_CONDITION_VALUE_ALL,
          ):
        """
        Parameters
        ----------
        method: str (algorithm)
        noise_mag: float
        range_min_frac: float (lower bound of parameter range as fraction true value)
        range_max_frac: float (upper bound of parameter range as fraction true value)
        range_initial_frac: float (initial parameter value as fraction true value)
        columns_deleted: int (number of columns deleted)
        max_fev: int (maximum number of function evaluations)
        ts_instance: int (instance of the synthetic observed data)
        """
        super().__init__()
        self.kwargs = ExtendedDict({})  # Arguments passed
        for key in cn.SD_CONDITIONS:
            self.kwargs[key] = eval(key)
            if eval(key) == cn.SD_CONDITION_VALUE_ALL:
                self[key] = cn.SD_CONDITION_VALUE_ALL_DCT[key]
            else:
                self[key] = eval(key)

    @property
    def iterator(self):
        for dct in iterateDict(self):
            yield ExperimentCondition(**dct)

    def __str__(self):
        return str(self.kwargs)
