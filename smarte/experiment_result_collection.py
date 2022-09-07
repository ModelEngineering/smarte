"""Container for a collection of experiment results"""

import smarte.constants as cn
from smarte.experiment_condition import ExperimentCondition
from smarte.extended_dict import ExtendedDict

import numpy as np
import pandas as pd

UNNAMED = "Unnamed:"


class ExperimentResultCollection(ExtendedDict):

    def __init__(self, df=None, **kwargs):
        """
        Parameters
        ----------
        df: DataFrame
            columns: cn.SD_ALL (except BIOMODEL_NUM)
            index: cn.BIOMODEL_NUM
        """
        super().__init__(kwargs)
        if df is not None:
            for column in df.columns:
                if column in cn.SD_ALL:
                    self[column] = list(df[column].values)
        for key in cn.SD_ALL:
            if not key in self.keys():
                self[key] = []
        keys = list(self.keys())
        size = len(self[keys[0]])
        for key in keys:
            if len(self[key]) < size:
                new_values = list(np.repeat(None, size))
                self[key].extend(new_values)
        dct = {k: v for k, v in self.items() if k in cn.SD_CONDITIONS}
        self.conditions = ExperimentCondition(**dct)

    def __len__(self):
        """
        Number of experiments.
        
        Returns
        -------
        int
        """
        keys = list(self.keys())
        return len(self[keys[0]])

    def copy(self):
        """
        Create an object with the same values as this object.
        
        Returns
        -------
        ExperimentResultCollection
        """
        new_collection = ExperimentResultCollection()
        import pdb; pdb.set_trace()
        for key, value in self.items():
            new_collection[key] = list(value)           
        return new_collection

    def equals(self, result_collection):
        """
        Test if the conditions of the ExperimentResultCollections are the same.
        Parameters
        ----------
        
        Returns
        -------
        """
        return self.conditions.equals(result_collection.conditions)
