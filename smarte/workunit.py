"""Workunit is a robust container of experiments to run and their results."""

import smarte.constants as cn
from smarte.persister import Persister
import smarte as smt
from smarte.condition_collection import ConditionCollection
from smarte.condition import Condition
from smarte.result_collection import ResultCollection
from smarte.factor_collection import FactorCollection

import os

WORKUNIT_FILE_PREFIX = "wu_"


class Workunit(ConditionCollection):

    def __init__(self, result_collection=None, excluded_factor_collection=None,
          out_dir=cn.EXPERIMENT_DIR,
          filename=None,
          **kwargs):
        """
        Parameters
        ----------
        result_collection: ResultCollection (previously accumulated results)
        excluded_factor_collection: FactorCollection
            factor levels to exclude from experiments
        out_dir: str (path to directory where files are found)
        kwargs: dict
            See cn.SD_CONDITIONS
        """
        super().__init__(**kwargs)
        self.result_collection = result_collection
        if self.result_collection is None:
            self.result_collection = ResultCollection()
        self.excluded_factor_collection = excluded_factor_collection
        if self.excluded_factor_collection is None:
            self.excluded_factor_collection = FactorCollection()
        self.out_dir = out_dir
        self.filename = filename
        if self.filename is None:
            self.filename = WORKUNIT_FILE_PREFIX + str(self)
        self.persister_path = os.path.join(self.out_dir, "%s.pcl" % self.filename)
        # File for this workunit
        self.persister = Persister(self.persister_path)

    def serialize(self):
        """
        Saves the current state of the workunit
        """
        self.persister.dump(self)

    @classmethod
    def deserialize(cls, workunit_str, out_dir=cn.EXPERIMENT_DIR):
        """
        Retrieves a previously saved Workunit.

        Parameters
        ----------
        workunit_str: str (String representation of the workload)
        out_dir: str (Directory for file)

        Returns
        -------
        Workunit
        """
        filename = "%s%s.pcl" % (WORKUNIT_FILE_PREFIX, workunit_str)
        path = os.path.join(out_dir, filename)
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
            if not condition in self.excluded_factor_collection:
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
           if ffile[0:len(WORKUNIT_FILE_PREFIX)]  \
                 == WORKUNIT_FILE_PREFIX:
               parts = os.path.splitext(ffile)
               if parts[1] == ".pcl":
                   filename = parts[0]
                   workunit_str = filename.replace(WORKUNIT_FILE_PREFIX, "")
                   workunits.append(cls.deserialize(workunit_str, out_dir=out_dir))
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
        return df

    def calcMultivaluedFactors(self):
        """
        Finds the factors for which there are multiple values.

        Returns
        -------
        list-str
        """
        return [k for k, v in self.items() if len(v) > 1]

    @classmethod
    def makeWorkunitsFromFile(cls, path, **kwargs):
        """
        Retrieves the workunits in a file.

        Parameters
        ----------
        path: str (path to file of workunits in string representation)
        kwargs: dict (optional arguments to use when constructing workunits)

        Returns
        -------
        list-workunit
        """
        with open(path, "r") as fd:
            lines = fd.readlines()
        workunit_strs = [l.strip() for l in lines]
        workunit_strs = [l for l in workunit_strs if l[0] != "#"]
        #
        workunits = []
        for workunit_str in workunit_strs:
            try:
                workunit = smt.Workunit.makeFromStr(workunit_str, **kwargs)
            except Exception as exp:
                print(exp)
                raise ValueError("Invalid workunit string: %s"
                      % workunit_str)
            workunits.append(workunit)
        return workunits
