"""ElementDict that has a single value for each attribute"""

from smarte.types.elemental_dict import ElementalDict
from smarte.types.sv_dict import SVDict
from smarte.types.elemental_type import isList

import copy

ALL = "all"


class MVDict(ElementalDict):

    expansion_dct = {}  # Override as needed

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict
        """
        super().__init__(**kwargs)
        # Add null lists where needed
        # Do the expansions
        for key, value in self.items():
            if value == ALL:
                if not key in self.expansion_dct.keys():
                    raise ValueError("No expansion entry for key %s" % key)
                self[key] = copy.deepcopy(self.expansion_dct[key])
        # Ensure that all elements are lists
        for key, value in self.items():
            if not isList(value):
                self[key] = [copy.deepcopy(value)]
        # Iterator position
        self.iterate_idx = 0

    def append(self, dct):
        """
        Appends values in dictionary to keys in the MVDict.

        Parameters
        ----------
        dct: dict
            key: key to use
            value: value to append
        """
        for key, value in self.items():
            if key in dct.keys():
                self[key].append(dct[key])

    def extend(self, dct, is_duplicates=False):
        """
        Extends values in dictionary.

        Parameters
        ----------
        dct: dict
            key: key to use
            value: value to append
        """
        for key, value in self.items():
            if key in dct.keys():
                self[key].extend(dct[key])

    def iterate(self, cls, is_restart=True):
        """
        Iterates on all elements in the dictionary. Uses _next method that is
        class specific. This is an abstract implementation.

        Parameters
        ----------
        cls: inherits from SVDict
        is_restart: bool
        
        Returns
        -------
        SVDict
        """
        if is_restart:
            self.iterate_idx = 0
        for idx, dct in enumerate(self._next()):
            if idx < self.iterate_idx:
                continue
            yield cls(**dct)
            self.iterate_idx = idx + 1

    def _next(self):
        raise RuntimeError("Must override")

    def __contains__(self, sv_dict):
        """
        Tests if the SVDict is in this collection.
        Preserves the iterator index for restarts.

        Parameters
        ----------
        sv_dict: inherits from SVDict
        
        Returns
        -------
        bool
        """
        iterate_idx = self.iterate_idx
        cls = sv_dict.__class__
        result = False
        for item in self.iterate(cls, is_restart=True):
            if item.equals(sv_dict):
                result = True
                break
        self.iterate_idx = iterate_idx
        return result
