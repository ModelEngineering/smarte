"""Specifies experiments and holds experiment results. Provides restarts"""

import smarte.constants as cn
from smarte.persister import Persister
import smarte as smt
from smarte.condition_collection import ConditionCollection
from smarte.result_collection import ResultCollection
from smarte.factor_collection import FactorCollection

import numpy as np
import os
import pandas as pd

PERSISTER_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTER_FILENAME = "workunit.pcl"
PERSISTER_PATH = os.path.join(PERSISTER_DIR, PERSISTER_FILENAME)


class Workunit(ConditionCollection):

    def __init__(self, result_collection=ResultCollection(),
          exclude_conditions=FactorCollection(),
          persister_path=PERSISTER_PATH, **kwargs):
        """
        Parameters
        ----------
        result_collection: ResultCollection (previously accumulated results)
        exclude_conditions: FactorCollection (factor levels to exclude from experiments)
        persister_path: str (path to persister file)
        kwargs: dict
            See cn.SD_CONDITIONS
        """
        super().__init__(**kwargs)
        # Result collection 
        # Hashes for conditions
        self.include_condition_hashs = [hash(str(c)) for c
              in self.include_conditions]
        self.exclude_condition_hashs = [hash(str(c)) for c
              in self.exclude_conditions]
        result_conditions = smt.ExperimentCondition.getFromResultCollection(
              self.result_collection)
        self.result_condition_hashs = [hash(str(c)) for c in result_conditions]
        # Fill in missing conditions
        if len(self.include_conditions) == 0:
            for key, value in cn.SD_CONDITION_DCT.items():
                # Fill in missing conditions
                if not key in kwargs.keys():
                    self.kwargs[key] = value
                    self[key] = value
        # Convert values to lists if needed
        for key, value in self.items():
            if isinstance(value, str):
                value = value.strip()
            if value == cn.SD_CONDITION_VALUE_ALL:
                self[key] = cn.SD_CONDITION_EXPANSION_DCT[key]
            elif isinstance(value, str):
                self[key] = [value]
            elif isinstance(value, list):
                self[key] = value
            else:
                self[key] = [value]
        # File for this workunit
        self.persister = Persister(persister_path)

    def serialize(self):
        """
        Saves the current state of the workunit
        """
        self.persister.dump(self)

    @classmethod
    def deserialize(cls, path=PERSISTER_PATH):
        """
        Retrieves a previously saved Workunit.

        Parameters
        ----------
        path: str (Path to a persister file)
        
        Returns
        -------
        Workunit
        """
        persister = Persister(path)
        data = persister.load()
        return data
    
    def equals(self, workunit):
        b1 = super().equals(workunit)
        b2 = self.result_collection.equals(workunit.result_collection)
        import pdb; pdb.set_trace()
        return b1 and b2

    def extend(self, workunit):
        """
        Combines another Workunit with this one.

        Parameters
        ----------
        workunit: Workunit
        """
        # Extend the dict values
        super().extend(workunit) # Extend the dict values
        self.result_collection.extend(workunit.result_collection, is_duplicates=True)

    # FIXME: TEST BELOW HERE

    def  __len__(self):
        """
        Number of conditions to simulate.
        
        Returns
        -------
        int
        """
        return len(list(self.iterator))

    # TODO: implement. Create hash for all conditions in workunit
    def __contains__(self, condition):
        """
        Determines if the condition is in the Workunit.

        Parameters
        ----------
        condition: ExperimentCondition
        
        Returns
        -------
        bool
        """

    @property
    def iterator(self):
        """
        Iterates across all conditions taking into account explicit includes
        and excludes as well as previously completed experiments.
        -------
        ExperimentCondition
        """
        for condition in self.include_conditions:
            yield condition
        #
        for dct in iterateDict(self):
            condition = smt.ExperimentCondition(**dct)
            if hash(str(condition)) in self.exclude_condition_hashs:
                continue
            yield condition

    # FIXME: How include includes, excludes
    def __str__(self):
        return str(self.kwargs)

    def calcMultivaluedFactors(self):
        """
        Finds the factors for which there are multiple values.
        
        Returns
        -------
        list-str
        """
        return [k for k, v in self.items() if len(v) > 1]
