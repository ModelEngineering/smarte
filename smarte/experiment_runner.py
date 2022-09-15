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
from smarte.condition import Condition
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


class ExperimentRunner(object):

    def __init__(self, workunit):
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
        self.multivalued_factors = self.workunit.calcMultivaluedFactors()

    def _writeMessage(self, condition, status, is_report):
        if is_report:
            stgs = ["%s=%s" % (k, str(condition[k])) for k in self.multivalued_factors]
            stg = ", ".join(stgs)
            print("***%s: %s" % (stg, status))

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

    def run(self, is_report=True):
        """
        Runs experiment for all conditions specified in self.workunit.

        Parameters
        ----------
        is_report: bool (report progress)

        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: biomodel_num
        """
        for condition in self.workunit.iterate(Condition, is_recover=True):
            # Setup to run the experiment
            biomodel_num = condition[cn.SD_BIOMODEL_NUM]
            result = smt.ExperimentResult(**condition)
            try:
                model = mdl.Model.getBiomodel(biomodel_num)
            except ValueError:
                model = None
            if model is None:
                result[cn.SD_STATUS] = "Cannot create model."
                self.workunit.appendResult(result)
            # Assign the qualifiers
            else:
                observed_ts = self.getTimeseries(biomodel_num,
                      condition[cn.SD_NOISE_MAG], condition[cn.SD_TS_INSTANCE])
                try:
                   result = smt.SBMLFitter.evaluateBiomodelFit(
                          biomodel_num, observed_ts,
                          range_min_frac=condition[cn.SD_RANGE_MIN_FRAC],
                          range_max_frac=condition[cn.SD_RANGE_MAX_FRAC],
                          latincube_idx=condition[cn.SD_LATINCUBE_IDX],
                          method_names=condition[cn.SD_METHOD],
                          max_fev=condition[cn.SD_MAX_FEV],
                          )
                except (ValueError, RuntimeError) as exp:
                    result[cn.SD_STATUS] = str(exp)
                self.workunit.appendResult(result)
                # Accumulate results
            # Save the results
            self.workunit.serialize()
            #
            self._writeMessage(condition, result[cn.SD_STATUS], is_report=is_report)
        # Handle the missing models
        return self.workunit.result_collection.makeDataframe()

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
