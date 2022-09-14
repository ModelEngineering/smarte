"""Dictionary whose values represent a hypercube"""

from smarte.types.mv_dict import MVDict
from smarte.types.mv_dict_table import MVDictTable

import pandas as pd


class MVDictHypercube(MVDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict
        """
        super().__init__(**kwargs)

    def _next(self):
        """
        Iterator for lists of the same length.

        Returns
        -------
        dict
        """
        def get(dct, index_dct):
            return {k: dct[k][index_dct[k]] for k in dct.keys()}
        # Ensure that dct consists of lists
        index_dct = {k: 0 for k in self.keys()}  # list position for each key
        keys = list(self.keys()) #  Order in which keys are incremented
        keys.reverse()
        # First value
        yield get(self, index_dct)
        # Iteration
        done = False
        while not done:
            carry = 1
            for key in keys:
                new_index = index_dct[key] + carry
                if new_index == len(self[key]):
                    index_dct[key] = 0
                    carry = 1
                else:
                    carry = 0
                    index_dct[key] = new_index
                    break
            #
            if carry == 0:
                yield get(self, index_dct)
            else:
                # Have completed iteration
                break

    def makeMVDictTable(self, cls):
        """
        Creates a MVDictTable.

        Parameters
        ----------
        cls: inherents from MVDictTable
        
        Returns
        -------
        cls
        """
        sv_dicts = list(self.iterate(is_restart=True))
        return MVDictTable.makeFromSVDicts(sv_dicts)
