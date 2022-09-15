"""A collection of factor values."""


import smarte.constants as cn
from smarte.types.mv_dict import MVDict
from smarte.condition import Condition


class FactorCollection(MVDict):
    # Keys are factors. Value is a list of levels.
    default_dct = {k: [] for k in cn.SD_CONDITION_DCT.keys()}
    expansion_dct = dict(cn.SD_CONDITION_EXPANSION_DCT)

    def __contains__(self, condition):
        """
        Determines if the condition has a value of one of the factors.

        Parameters
        ----------
        condition: Condition
        
        Returns
        -------
        bool
        """
        for factor, levels in self.items():
            if condition[factor] in levels:
                return True
        return False
