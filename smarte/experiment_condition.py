"""Description of an experimental condition, items controlled in an experiment."""

"""
An ExperimentCondition is a specification of a level for all factors. This is represented
as a dictionary where the keys are factors and their value is a level.
"""

import smarte.constants as cn
from smarte.extended_dict import ExtendedDict
from smarte.iterate_dict import iterateDict

import pandas as pd


class ExperimentCondition(ExtendedDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        See cn.SD_CONDITION_DCT
        """
        super().__init__(**kwargs)
        self.kwargs = ExtendedDict(kwargs)  # Arguments passed
        for key, value in cn.SD_CONDITION_DCT.items():
            # Fill in missing conditions
            if not key in kwargs.keys():
                self.kwargs[key] = value
                self[key] = value
            # Expand "all" keywords
            if self.kwargs[key] == cn.SD_CONDITION_VALUE_ALL:
                self[key] = cn.SD_CONDITION_VALUE_ALL_DCT[key]

    def __str__(self):
        return str(self.kwargs)

    @classmethod
    def getFromDF(cls, df):
        """
        Extracts conditions from a dataframe

        Returns
        -------
        list-ExperimentCondition
        """
        conditions = []
        condition_df = df.reset_index()
        condition_df = condition_df[cn.SD_CONDITIONS]
        condition_df = condition_df.drop_duplicates(ignore_index=False)
        for _, row in condition_df.iterrows():
            dct = {k: row[k] for k in cn.SD_CONDITIONS}
            condition = ExperimentCondition(**dct)
            conditions.append(condition)
        return conditions
