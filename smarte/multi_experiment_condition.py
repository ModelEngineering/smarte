"""MultiExperimentCondition compactly represents many ExperimentConditions"""

"""
A MultiExperimentCondition is a compact representation of a set of ExperimentConditions.
The keys are factors. The values are a non-empty set of levels. To further simplify this
representation, there is a "universal set" defined for each factor. The entry "*" indicates
that the set of levels for a factor is its universal set.
"""

"""
TODO
1. Specify cn.SD_UNIVERSAL, cn.SD_UNIVERSAL_DCT
2. Implement DictIterator
"""

from smarte.experiment_condition import ExperimentCondition
import smarte.constants as cn
from smarte.extended_dict import ExtendedDict
from smarte.dict_iterator import DictIterator


class MultiExperimentCondition(ExtendedDict):

    def __init__(self, condition, **kwargs):
        """
        Parameters
        ----------
        condition: ExperimentCondition (default levels for factors)
        kwargs: dict
            key: factor
            value: list (or "*") of levels
        """
        for factor, level in condition.items():
            if factor in kwargs.keys():
                if kwargs[key] == cn.SD_UNIVERSAL:
                    self[key] = cn.SD_UNIVERSAL_DCT[key]
                else:
                    self[key] = kwargs[key]
            else:
                self[key] = [value]

    def iterator(self):
        """
        Iteratively returns all ExperimentConditions specified by the
        MultiExperimentCondition.
 
        Returns
        -------
        iterator-ExperimentCondition
        """
        for dct in iterateDict(self):
            yield ExperimentCondition(dct)

    def add(self, dct):
        """
        Adds the levels for a set of factors.

        Parameters
        ----------
        dct: dict
            key: factor
            value: list-level (float, int, str)
        
        Returns
        -------
        MultiExperimentCondition
        """

    def subtract(self, dct):
        """
        Removes the levels for a set of factors.

        Parameters
        ----------
        dct: dict
            key: factor
            value: list-level (float, int, str)
        
        Returns
        -------
        MultiExperimentCondition
        """

    def union(self, other):
        """
        Computes the union of levels for the factors.

        Parameters
        ----------
        other: MultiExperimentCondition
            key: factor
            value: list-level (float, int, str)
        
        Returns
        -------
        MultiExperimentCondition
        """

    def intersection(self, other):
        """
        Computes the intersection of levels for the factors.
        Raises an exception if the intersection of levels is empty
        for some factor.

        Parameters
        ----------
        other: MultiExperimentCondition
            key: factor
            value: list-level (float, int, str)
        
        Returns
        -------
        MultiExperimentCondition
        """
