"""Runs experiments for cn.SD_CONTROLLED_FACTORS"""

import smarte as smt
from smarte import constants as cn
import SBMLModel as mdl

import dask
from dask.distributed import Client
import os
import pandas as pd

F_LOWER = 0.25  # Lower end of range for value search
F_HIGHER = 4.0  # Upper end of range for value search
F_INITIAL = F_LOWER  # Starting point for search
OUT_FILE = os.path.join(cn.PROJECT_DIR, "biomodels_statistics.csv")
NUM_REPLICATION = 3
UNNAMED = "Unnamed:"
BIOMODEL_EXCLUDE_PATH = os.path.join(cn.DATA_DIR, "biomodels_exclude.csv")
BIOMODEL_EXCLUDE_DF = pd.read_csv(BIOMODEL_EXCLUDE_PATH)
BIOMODEL_EXCLUDES = list(BIOMODEL_EXCLUDE_DF[cn.SD_BIOMODEL_NUM].values)
DUMMY_RESULT = {"a": 0.5, "b": 0.5}
EXCLUDE_FACTOR_DCT = dict(biomodel_num=BIOMODEL_EXCLUDES)


def wrapper(workunit):
    runner = smt.ExperimentRunner(workunit)
    df = runner.runWorkunit()
    return df


class ExperimentRunner(object):

    def __init__(self, workunit, directory=cn.EXPERIMENT_DIR,
          exclude_factor_dct=None, out_path=None):
        """
        Parameters
        ----------
        workunit: Workunit
        directory: str (directory for file output)
        exclude_factor_dct: dict (any condition with a factor value is excluded)
             key: factor
             value: list-levels
        out_path: str (path where results are stored)
        """
        self.workunit = workunit
        self.exclude_factor_dct = exclude_factor_dct
        if self.exclude_factor_dct is None:
            self.exclude_factor_dct = EXCLUDE_FACTOR_DCT
        self.directory = directory
        self.out_path = out_path
        if self.out_path is None:
            self.out_path = self.makePath(self.workunit, self.directory)
        self.factors = self.workunit.calcMultivaluedFactors()

    def _writeMessage(self, condition, status, is_report):
        if is_report:
            stgs = ["%s=%s" % (k, str(condition[k])) for k in self.factors]
            stg = ", ".join(stgs)
            print("***%s: %s" % (stg, status))

    @staticmethod
    def makePath(workunit, directory=cn.EXPERIMENT_DIR):
        """
        Consturcts a path to the CSV file for the workunit used in this experiment.

        Parameters
        ----------
        workunit: Workunit
        directory: str

        Returns
        -------
        str
        """
        filename = "%s.csv" % str(workunit)
        return os.path.join(directory, filename)

    def runWorkunit(self, is_recover=True, is_report=True):
        """
        Runs experiment for all of BioModels. Has recovery capability
        where continues with an existing CSV file.

        Parameters
        ----------
        is_recover: bool (recover existing results if they exist)
        is_report: bool (report progress)

        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: biomodel_num
        """
        # Check for a restart
        results = smt.ExperimentResult.makeAggregateResult()
        condition_strs = []
        if os.path.isfile(self.out_path) and is_recover:
            df = self.readCsv(self.out_path)
            if df is not None:
                results = smt.ExperimentResult.makeAggregateResult(df)
                conditions = smt.ExperimentCondition.getFromDF(df)
                condition_strs = [str(c) for c in conditions]
        # Find the subset of conditions to process
        conditions = []
        for condition in self.workunit.iterator:
            # See if already processed
            if str(condition) in condition_strs:
                continue
            # Check for excluded factor value
            is_skip = False
            for factor in self.exclude_factor_dct.keys():
                if condition[factor] in self.exclude_factor_dct[factor]:
                    is_skip = True
                    break
            if is_skip:
                continue
            conditions.append(condition)
        #
        return self.runConditions(conditions, results=results, is_report=is_report)

    def runConditions(self, conditions, results=None, is_report=True):
        """
        Runs experiment for all of BioModels. Has recovery capability
        where continues with an existing CSV file.

        Parameters
        ----------
        conditions: iterable-condition
        results: list-ExperimentalResult
        is_recover: bool (recover existing results if they exist)
        is_report: bool (report progress)

        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: biomodel_num
        """
        if results is None:
            results = []
        for condition in conditions:
            biomodel_num = condition[cn.SD_BIOMODEL_NUM]
            result = smt.ExperimentResult(**condition)
            try:
                model = mdl.Model.getBiomodel(biomodel_num)
            except ValueError:
                model = None
            if model is None:
                result[cn.SD_STATUS] = "Cannot create model."
            # Assign the qualifiers
            else:
                observed_ts = self.getTimeseries(biomodel_num,
                      condition[cn.SD_NOISE_MAG], condition[cn.SD_TS_INSTANCE])
                try:
                    new_result = smt.SBMLFitter.evaluateBiomodelFit(
                          biomodel_num, observed_ts,
                          range_min_frac=condition[cn.SD_RANGE_MIN_FRAC],
                          range_max_frac=condition[cn.SD_RANGE_MAX_FRAC],
                          latincube_idx=condition[cn.SD_LATINCUBE_IDX],
                          method_names=condition[cn.SD_METHOD],
                          max_fev=condition[cn.SD_MAX_FEV],
                          )
                    result.update(new_result)
                except (ValueError, RuntimeError) as exp:
                    result[cn.SD_STATUS] = str(exp)
                # Accumulate results
                results.append(result)
            # Save the results
            df = self.writeResults(results)
            #
            self._writeMessage(condition, result[cn.SD_STATUS], is_report=is_report)
        # Handle the missing models
        return df

    @staticmethod
    def getTimeseries(biomodel_num, noise_mag, ts_instance):
        """
        Obtains the timeseries for the model and replication instance.

        Parameters
        ----------
        biomodel_num: int
        ts_instance: int (index of synthetic time series for model)

        Returns
        -------
        Timeseries
        """
        directory = "%d--%s" % (biomodel_num, str(noise_mag))
        path = os.path.join(cn.DATA_DIR, directory)
        filename = "%d.csv" % ts_instance
        path = os.path.join(path, filename)
        df = pd.read_csv(path)
        if "miliseconds" in df.columns:
            df = df.rename(columns={"miliseconds": cn.MILLISECONDS})
        df = df.set_index(cn.MILLISECONDS)
        return df

    @classmethod
    def readCsv(cls, path=None, workunit=None, directory=cn.EXPERIMENT_DIR):
        """
        Creates a DataFrame from a CSV file structured as ExperimentResult.

        Parameters
        ----------
        path: str (explicit path to use)
        workunit: Workunit (used to infer path if no explicit path)
        directory: str (contains file)

        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: int (biomodel number)
        """
        if path is None:
            path = cls.makePath(workunit, directory)
        try:
            df = pd.read_csv(path, index_col=cn.SD_BIOMODEL_NUM)
        except Exception:
            return None
        for column in df.columns:
            if UNNAMED in column:
                del df[column]
        return df

    def writeResults(self, results, path=None):
        """
        Writes the results to the designated file.

        Parameters
        ----------
        results: list-ExperimentResult

        Returns
        -------
        pd.DataFrame
        """
        if path is None:
            path = self.out_path
        df = pd.DataFrame(results)
        final_df = df.sort_values(cn.SD_BIOMODEL_NUM)
        final_df = final_df.set_index(cn.SD_BIOMODEL_NUM)
        final_df.to_csv(path, index=True)
        return final_df

    @classmethod
    def runWorkunits(cls, num_worker=4, path=cn.WORKUNITS_FILE):
        """
        Runs workunits in parallel.

        Parameters
        ----------
        path: str (path to file of workunits in string representation)

        Returns
        -------
        """
        # Create the local cluster
        client = Client(n_workers=num_worker, memory_limit='3GB',
               threads_per_worker=1)
        lazy_results = []
        try:
            #
            with open(path, "r") as fd:
                lines = fd.readlines()
            #
            lazy_results = []
            for line in lines:
                # Remove trailing newline
                new_line = line.strip()
                # Handle comments
                if new_line[0]  == "#":
                    continue
                # Extract the workunit
                try:
                    workunit = smt.Workunit.getFromStr(new_line)
                except:
                    raise ValueError("Invalid workunit string: %s"
                          % new_line)
                # Assemble the list of computations
                lazy_result = dask.delayed(wrapper)(workunit)
                lazy_results.append(lazy_result)
            #
        except Exception as exp:
            print(exp)
        final_result = dask.compute(*lazy_results)  # trigger computation
        client.close()
        return final_result


if __name__ == '__main__':
    if False:
        workunit_str = "biomodel_num--all__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--all"
        a_workunit = smt.Workunit.getFromStr(workunit_str)
        this_runner = smt.ExperimentRunner(a_workunit)
        this_runner.runWorkunit()
    else:
        ExperimentRunner.runWorkunits(num_worker=12)
