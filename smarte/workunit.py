"""Workunit is a robust container of experiments to run and their results."""

import smarte.constants as cn
from smarte.persister import Persister
import smarte as smt
from smarte.condition_collection import ConditionCollection
from smarte.condition import Condition
from smarte.result_collection import ResultCollection
from smarte.factor_collection import FactorCollection

import numpy as np
import os
import pandas as pd

WORKUNIT_PERSISTER_FILE_PREFIX = "wu_"


class Workunit(ConditionCollection):

    def __init__(self, result_collection=ResultCollection(),
          excluded_factor_levels=FactorCollection(),
          out_dir=cn.EXPERIMENT_DIR,
          filename=None,
          **kwargs):
        """
        Parameters
        ----------
        result_collection: ResultCollection (previously accumulated results)
        excluded_factor_levels: FactorCollection
            factor levels to exclude from experiments
        out_dir: str (path to directory where files are found)
        kwargs: dict
            See cn.SD_CONDITIONS
        """
        super().__init__(**kwargs)
        self.result_collection = result_collection
        self.excluded_factor_levels = excluded_factor_levels
        self.out_dir = out_dir
        self.filename = filename
        if self.filename is None:
            self.filename = WORKUNIT_PERSISTER_FILE_PREFIX + str(self)
        self.persister_path = os.path.join(self.out_dir, "%s.pcl" % self.filename)
        # File for this workunit
        self.persister = Persister(self.persister_path)

    def serialize(self):
        """
        Saves the current state of the workunit
        """
        self.persister.dump(self)

    @classmethod
    def deserialize(cls, path):
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
        """
        Tests if two workunits have the same conditions and results.

        Parameters
        ----------
        workunit: Workunit
        
        Returns
        -------
        bool
        """
        b1 = super().equals(workunit)
        b2 = self.result_collection.equals(workunit.result_collection)
        return b1 and b2

    def appendResult(self, result):
        """
        Adds results to completed experiments.

        Parameters
        ----------
        result: Result
        """
        self.result_collection.append(result)

    def iterate(self, is_restart=True):
        """
        Iterates across all permitted conditions. Takes into account excluded
        conditions.

        Parameters
        ----------
        is_restart: bool
        
        Returns
        -------
        Condition
        """
        for condition in super().iterate(Condition, is_restart=is_restart):
            if not condition in self.excluded_factor_levels:
                yield condition

    @classmethod
    def getWorkunits(cls, out_dir=cn.EXPERIMENT_DIR):
        """
        Finds all of the workunits in the directory.

        Parameters
        ----------
        out_dir: str (directory to search)
        
        Returns
        -------
        list-Workunit
        """
        ffiles = os.listdir(out_dir)
        workunits = []
        for ffile in ffiles:
            if ffile[0:len(WORKUNIT_PERSISTER_FILE_PREFIX)+1]  \
                  == WORKUNIT_PERSISTER_FILE_PREFIX:
               import pdb; pdb.set_trace()
               parts = os.path.splitext(ffile)
               if parts[1] == ".pcl":
                   path = os.path.join(directory, ffile)
                   workunits.append(cls.deserialize(path))
        return workunits

    def makeResultCsv(self, path=None):
        """
        Writes the results of experiments.

        Parameters
        ----------
        path: str
        """
        df = self.result_collection.makeDataframe()
        if path is None:
            path = self.filename + ".csv"
            path = os.path.join(self.out_dir, path)
        df.to_csv(path)

    def calcMultivaluedFactors(self):
        """
        Finds the factors for which there are multiple values.
        
        Returns
        -------
        list-str
        """
        return [k for k, v in self.items() if len(v) > 1]
