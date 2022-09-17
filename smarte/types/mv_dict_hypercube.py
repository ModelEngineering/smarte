"""Dictionary whose values represent a hypercube"""

from smarte.types.sv_dict import SVDict
from smarte.types.mv_dict import MVDict
from smarte.types.mv_dict_table import MVDictTable

import numpy as np


class MVDictHypercube(MVDict):

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

    def __len__(self):
        """
        Calculates the length of the list produced by iteration.

        Returns
        -------
        int
        """
        sizes = [len(v) for v in self.values()]
        return np.prod(sizes)

    def makeMVDictTable(self, mv_table_cls=None):
        """
        Creates a MVDictTable.

        Parameters
        ----------
        mv_table_cls: Class (inherents from MVDictTable)

        Returns
        -------
        mv_table_cls
        """
        class _SVDict(SVDict):
            default_dct = self.default_dct
        #
        class _MVDictTable(MVDictTable):
            default_dct = self.default_dct
            expansion_dct = self.expansion_dct
        #
        if mv_table_cls is None:
            mv_table_cls = _MVDictTable
        sv_dicts = list(self.iterate(_SVDict, is_restart=True))
        return mv_table_cls.makeFromSVDicts(mv_table_cls, sv_dicts)
