"""Container for the results of experiments."""

import smarte.constants as cn
from smarte.extended_dict import ExtendedDict

import pandas as pd
import numpy as np


UNNAMED = "Unnamed:"


class ExperimentResult(ExtendedDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        dct: dict (partial experiment information)
        """
        super().__init__(kwargs)
        for key in self.keys():
            if UNNAMED in key:
                del self[key]
        for key in cn.SD_ALL:
            if not key in self.keys():
                self[key] = None
    
    def __str__(self):
        """
        Creates a name based on the conditions.

        Returns
        -------
        str
        """
        names = [k + KEY_VALUE_SEP + str(v) for k, v in self.items()]
        return CONDITION_SEP.join(names)
