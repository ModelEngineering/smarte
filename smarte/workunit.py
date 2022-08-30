"""Describes multiple conditions to simulate"""

import smarte.constants as cn
import smarte as smt
from smarte.extended_dict import ExtendedDict
from smarte.iterate_dict import iterateDict

import pandas as pd


class Workunit(ExtendedDict):
    # All values are lists

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        See cn.SD_CONDITION_DCT
        """
        super().__init__(**kwargs)
        self.kwargs = ExtendedDict(kwargs)  # Arguments passed
        # Fill in missing conditions
        for key, value in cn.SD_CONDITION_DCT.items():
            # Fill in missing conditions
            if not key in kwargs.keys():
                self.kwargs[key] = value
                self[key] = value
        # Convert values to lists if needed
        for key, value in self.items():
            if isinstance(value, str):
                value = value.strip()
            if value == cn.SD_CONDITION_VALUE_ALL:
                self[key] = cn.SD_CONDITION_VALUE_ALL_DCT[key]
            elif isinstance(value, str):
                self[key] = [value]
            elif isinstance(value, list):
                self[key] = value
            else:
                self[key] = [value]

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
                new_value = [cn.SD_CONDITION_VALUE_ALL]
            else:
                new_value = value
            new_workunit[key] = new_value
        if "?" in new_workunit:
            import pdb; pdb.set_trace()
        return new_workunit

    @classmethod
    def makeEmpty(cls):
        return cls(biomodel_num=[],
          method=[],
          noise_mag=[],
          range_min_frac=[],
          range_max_frac=[],
          num_latincube=[],
          columns_deleted=[],
          max_fev=[],
          ts_instance=[],
          )
