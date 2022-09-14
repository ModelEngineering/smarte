"""Dictionary whose values are lists of the same length"""

from smarte.types.sv_dict import SVDict
from smarte.types.mv_dict import MVDict

import pandas as pd


class MVDictTable(MVDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict
        """
        super().__init__(**kwargs)
        self.first_key = list(self.keys())[0]
        trues = [len(v) == len(self[self.first_key]) for v in self.values()]
        if not all(trues):
            raise ValueError("All lists must have the same length.")

    def _next(self):
        """
        Iterator for lists of the same length.

        Returns
        -------
        dict
        """
        for idx in range(len(self[self.first_key])):
            dct = {k: v[idx] for k, v in self.items()}
            yield dct

    @classmethod
    def makeFromSVDicts(cls, sv_dicts):
        """
        Create MVDictTable from a collection of SVDict.

        Parameters
        ----------
        sv_dicts: list-SVDict
        
        Returns
        -------
        MVDictTable
        """
        dct = {k: [] for k in cls.default_dct.keys()}
        for this_dct in sv_dicts:
            [dct[k].append(v) for k, v in this_dct.items()]
        return cls(**dct)
                
    def makeDataframe(self): 
        """
        Creates a datafrome from the dictionary.

        Returns
        -------
        pd.DataFrame
        """
        return pd.DataFrame(self)
