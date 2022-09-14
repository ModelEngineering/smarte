"""Runs experiments for cn.SD_CONTROLLED_FACTORS"""
"""
1.  WorkunitInfo -> Workunit with ExperimentResultCollection
    Concatenate
    clean: remove conditions that are in result
2. Figure out where the history files are for doing fine grain scheduling
3. Naming files for workunits. workunit has a filename. Use that.
"""

import smarte as smt
from smarte import constants as cn
from smarte.result_collection import ResultCollection
import SBMLModel as mdl

import collections
import dask
from dask.distributed import Client
import numpy as np
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
FINE_GRAIN_RESULT_PAT = "fine_grain_result-%d.csv"


WorkunitInfo = collections.namedtuple("WorkunitInfo",
      "conditions result_collection")


def workunitRunnerWrapper(workunit):
    runner = smt.ExperimentRunner(workunit)
    df = runner.runWorkunit()
    return df

def conditionRunnerWrapper(conditions, result_collection):
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

    @classmethod
    def recover(cls, is_recover, path):
        """
        Recovers results if they exist.

        Parameters
        ----------
        is_recover: bool (recover existing results if they exist)
        path: str (path to file to recover from)

        Returns
        -------
        ExperimentResultCollection
        """
        result_collection = ExperimentResultCollection()
        if is_recover and (path is not None):
            if os.path.isfile(path):
                df = cls.readCsv(path)
                if df is not None:
                    for name in cn.SD_ALL:
                        if not name in list(df.columns):
                            raise RuntimeError(
                                  "Missing attribute in result: %s" % name)
                    result_collection = smt.ExperimentResultCollection(df=df)
        return result_collection

    @classmethod
    def getWorkunitInfoCls(cls, workunit, path=None, is_recover=True,
          exclude_factor_dct=EXCLUDE_FACTOR_DCT):
        """
        Creates the information needed to run experiments for a workunit.
        Eliminates conditions that have been processed already.

        Parameters
        ----------
        workunit: ExperimentWorkunit
        path: str (path to recover previous results)
        is_recover: bool (recover existing results if they exist)
        exclude_factor_dct: dictionary of factor values to exclude

        Returns
        -------
        WorkunitInfo
        """
        # Handle a restart by getting conditions that have been processed
        result_collection = cls.recover(is_recover, path)
        condition_strs = [str(c) for c in result_conditions]
        conditions = []
        for condition in workunit.iterator:
            if str(condition) in condition_strs:
                continue
            # Check for excluded factor value
            is_skip = False
            for factor in exclude_factor_dct.keys():
                if condition[factor] in exclude_factor_dct[factor]:
                    is_skip = True
                    break
            if is_skip:
                continue
            conditions.append(condition)
        #
        return WorkunitInfo(conditions=conditions, result_collection=result_collection)

    def getWorkunitInfo(self, is_recover=True):
        """
        Creates the information needed to run experiments for a workunit.

        Parameters
        ----------
        is_recover: bool (recover existing results if they exist)

        Returns
        -------
        WorkunitInfo
        """
        return self.getWorkunitInfoCls(self.workunit, path=self.out_path,
              is_recover=is_recover, exclude_factor_dct=self.exclude_factor_dct)

    @classmethod
    def iteratePartitionedConditions(cls, paths, workunits, num_partition=1, is_recover=True):
        """
        Iterator that provides evenly divided partitions of WorkunitInfo. Among the
        number of partitions.

        Parameters
        ----------
        paths: list-str (paths from which information is obtained)
        num_partition: int (number of partitions to create for parallel exeriments)
        is_recover: bool (recover existing results if they exist)

        Returns
        -------
        list-WorkunitInfo
        """
        # Merge the results
        result_collections = [cls.recover(is_recover=is_recover, path=p) for p in paths]
        all_result_collection = smt.ExperimentResultCollection()
        [all_result_collection.extend(c) for c in result_collections]
        completed_conditions = smt.ExperimentCondition.getFromResultCollection(result_collection)
        completed_condition_strs = [str(c) for c in completed_conditions]
        # Find the conditions yet to be done
        workunit_infos = [cls.getWorkunitInfoCls(cls, w, is_recover=False) for w in workunits]
        all_conditions = []
        [all_conditions.extend(w.conditions) for w in workunit_infos]
        selected_conditions = [c for c in all_conditions if not str(c) in completed_condition_strs]
        # Partition the work
        is_first = True
        size = len(selected_conditions)
        for idx in range(num_partition):
            conditions = []
            for pos in range(idx, size, num_partition):
                conditions.append(selected_conditions[pos])
            if is_first:
                workunit_info = WorkunitInfo(conditions=conditions, result_collection=all_result_collection)
                is_first = False
            else:
                workunit_info = WorkunitInfo(conditions=conditions, result_collection=[])
            yield workunit_info

    def runWorkunit(self, is_recover=True, is_report=True):
        """
        Runs experiment for a workunit. Handles recovery of an interrupted run.

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
        workunit_info = self.getWorkunitInfo(is_recover=True)
        return self.runConditions(
              workunit_info.conditions, 
              result_collection=workunit_info.result_collection,
              is_report=is_report)

    # TODO: use workunit_info instead of conditions, result_collection?
    def runConditions(self, conditions, result_collection=None, is_report=True):
        """
        Runs experiment for all of BioModels. Has recovery capability
        where continues with an existing CSV file.
        Assumes that conditions are not in result_collection.

        Parameters
        ----------
        conditions: list-condition (experiments to run)
        result_collection: ExperimentalResultCollection (completed experiments)
        is_recover: bool (recover existing results if they exist)
        is_report: bool (report progress)

        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: biomodel_num
        """
        if result_collection is None:
            result_collection = smt.ExperimentResultCollection()
        for condition in conditions:
            # Setup to run the experiment
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
                result_collection.append(result)
            # Save the results
            df = self.writeResults(result_collection)
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
            df = pd.read_csv(path)
        except Exception:
            return None
        for column in df.columns:
            if UNNAMED in column:
                del df[column]
        return df

    def writeResults(self, result_collection, path=None):
        """
        Writes the results to the designated file.

        Parameters
        ----------
        result_collection: ExperimentResultCollection

        Returns
        -------
        pd.DataFrame
        """
        if path is None:
            path = self.out_path
        df = pd.DataFrame(result_collection)
        final_df = df.sort_values(cn.SD_BIOMODEL_NUM)
        final_df.to_csv(path, index=True)
        return final_df

    @staticmethod
    def getWorkunitsFromFile(path):
        """
        Retrieves the workunits in a file.

        Parameters
        ----------
        path: str (path to file of workunits in string representation)
        
        Returns
        -------
        list-workunit
        """
        with open(path, "r") as fd:
            lines = fd.readlines()
        workunit_strs = [l.strip() for l in lines]
        #
        workunits = []
        for workunit_str in workunit_strs:
            try:
                workunit = smt.Workunit.getFromStr(workunit_str)
            except:
                raise ValueError("Invalid workunit string: %s"
                      % workunit_str)
            workunits.append(workunit)
        return workunits

    @classmethod
    def runWorkunits(cls, num_worker=4, path=cn.WORKUNITS_FILE,
          is_coarse_schedule=True):
        """
        Runs workunits in parallel.

        Parameters
        ----------
        path: str (path to file of workunits in string representation)
        is_coarse_schedule: bool (schedule at the granularity of workunit)

        Returns
        -------
        """
        # Create the local cluster
        client = Client(n_workers=num_worker, memory_limit='3GB',
               threads_per_worker=1)
        lazy_results = []
        workunits = getWorkunitsFromFile(path)
        # Schedule the work
        # TODO: Finish
        if not is_coarse_schedule:
            # Schedule at the granularity of experiment
            runner = ExperimentRunner(workunit)
            for workunit_info in runner.iterateWorkunitInfo(num_worker):
                lazy_result = dask.delayed(conditionRunnerWrapper)(
                      workunit_info.conditions, workunit_info.result_collection)
                lazy_results.append(lazy_result)
        else:
            # Distribute work units
            for workunit_str in workunit_strs:
                # Handle comments
                if workunit_str[0]  == "#":
                    continue
                # Extract the workunit
                try:
                    workunit = smt.Workunit.getFromStr(workunit_str)
                except:
                    raise ValueError("Invalid workunit string: %s"
                          % workunt_str)
                # Assemble the list of computations
                lazy_result = dask.delayed(workunitRunnerWrapper)(workunit)
                lazy_results.append(lazy_result)
        #
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
