"""Describes multiple conditions to simulate"""

import smarte.constants as cn
import smarte as smt
from smarte.extended_dict import ExtendedDict
from smarte.iterate_dict import iterateDict

import pandas as pd


class Workunit(ExtendedDict):
    # All values are lists

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
        super().__init__(
              biomodel_num=biomodel_num,
              method=method,
              noise_mag=noise_mag,
              range_min_frac=range_min_frac,
              range_max_frac=range_max_frac,
              range_initial_frac=range_initial_frac,
              columns_deleted=columns_deleted,
              max_fev=max_fev,
              ts_instance=ts_instance,
        )
        self.kwargs = ExtendedDict({})  # Arguments passed
        for key in cn.SD_CONDITIONS:
            value = eval(key)
            if isinstance(value, str):
                value = value.strip()
            self.kwargs[key] = value
            if value == cn.SD_CONDITION_VALUE_ALL:
                self[key] = cn.SD_CONDITION_VALUE_ALL_DCT[key]
            elif isinstance(value, str):
                self[key] = [eval(key)]
            elif isinstance(value, list):
                self[key] = eval(key)
            else:
                self[key] = [eval(key)]

    @property
    def iterator(self):
        for dct in iterateDict(self):
            yield smt.ExperimentCondition(**dct)

    def __str__(self):
        return str(self.kwargs)

    def calcMultivaluedFactors(self):
        """
        Finds the factors for which there are multiple values.
        
        Returns
        -------
        list-str
        """
        return [k for k, v in self.items() if len(v) > 1]

    def removeExpansions(self):
        """
        Removes the expansion of "all" values.
        """
        new_workunit = Workunit(**self.kwargs)
        for key, value in new_workunit.items():
            if self.kwargs[key] == cn.SD_CONDITION_VALUE_ALL:
                new_value = cn.SD_CONDITION_VALUE_ALL
            else:
                new_value = value
            new_workunit[key] = [new_value]
        return new_workunit
