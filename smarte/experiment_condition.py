"""Description of an experimental condition, items controlled in an experiment."""

import smarte.constants as cn

import pandas as pd
import os

CONDITION_SEP = "_"  # Separates conditions
KEY_VALUE_SEP = "--" # Separates the key and its value


class ExperimentCondition(dict):

    def __init__(self, **kwargs):
        super.__init__()
        for key in self.keys():
            if not key in cn.SD_CONTROLLED_FACTORS:
                raise ValueError("Invalid condition: %s" % k)
        for key in cn.SD_CONTROLLED_FACTORS:
            if not key in self.keys():
                raise ValueError("Missing value for condition: %s" % key)
    
    def __str__(self):
        """
        Creates a name based on the conditions.

        Returns
        -------
        str
        """
        names = [k + KEY_VALUE_SEP + str(v) for k, v in self.dct.items()]
        return CONDITION_SEP.join(names)

    @classmethod
    def getCondition(cls, name):
        """
        Decodes the name.

        Parameters
        ----------
        path: str (path to directory)
        
        Returns
        -------
        Condition
            key: condition
            value: value of condition
        """
        dct = {}
        for part in name:
            pair = part.split(KEY_VALUE_SEP)
            try:
                value = int(pair[1])
            except:
                try:
                    value = float(pair[1])
                except:
                    value = pair[1]
            dct[pair[0]] = value
        return cls(**dct)
