"""Runs experiments for cn.SD_CONTROLLED_FACTORS"""
"""
1.  WorkunitInfo -> Workunit with ResultCollection
    Concatenate
    clean: remove conditions that are in result
2. Figure out where the history files are for doing fine grain scheduling
3. Naming files for workunits. workunit has a filename. Use that.
"""

import smarte as smt
from smarte import constants as cn
from smarte.result_collection import ResultCollection
from smarte.result import Result
from smarte.condition import Condition
from smarte.workunit import Workunit
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


def workunitRunnerWrapper(workunit):
    print(str(workunit))
    runner = smt.WorkunitRunner(workunit)
    return runner.run()


class WorkunitRunner(object):

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
        # Iterate on conditions specified in the Workunit.
        # If there is an interruption and the calculation is restarted,
        # continue from where left off.
        for condition in self.workunit.iterate(is_restart=False):
            # Setup to run the experiment
            biomodel_num = condition[cn.SD_BIOMODEL_NUM]
            result = smt.Result(**condition)
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
                   dct = smt.SBMLFitter.evaluateBiomodelFit(
                          biomodel_num, observed_ts,
                          range_min_frac=condition[cn.SD_RANGE_MIN_FRAC],
                          range_max_frac=condition[cn.SD_RANGE_MAX_FRAC],
                          latincube_idx=condition[cn.SD_LATINCUBE_IDX],
                          method_names=condition[cn.SD_METHOD],
                          max_fev=condition[cn.SD_MAX_FEV],
                          )
                except (ValueError, RuntimeError) as exp:
                    result[cn.SD_STATUS] = str(exp)
                dct.update(condition)
                result = Result(**dct)
                self.workunit.appendResult(result)
                # Accumulate results
            # Save the results
            self.workunit.serialize()
            df = self.workunit.makeResultCsv()
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
        return mdl.Timeseries(df)

    @classmethod
    def schedule(cls, num_worker=4, path=cn.WORKUNITS_FILE):
        """
        Schedules workunits to run in parallel.

        Parameters
        ----------
        num_worker: int (number of parallel calculations)
        path: str (location of file with the workunits string representations)
        """
        # Create the local cluster
        client = Client(n_workers=num_worker, memory_limit='3GB',
               threads_per_worker=1)
        lazy_results = []
        workunits = Workunit.makeWorkunitsFromFile(path)
        # Assemble the list of computations
        for workunit in workunits:
            lazy_result = dask.delayed(workunitRunnerWrapper)(workunit)
            lazy_results.append(lazy_result)
        # Trigger the computation
        final_result = dask.compute(*lazy_results)
        client.close()
        return final_result


if __name__ == '__main__':
    if False:
        workunit_str = "biomodel_num--all__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--all"
        a_workunit = smt.Workunit.makeFromStr(workunit_str)
        this_runner = smt.WorkunitRunner(a_workunit)
        this_runner.run()
    else:
        WorkunitRunner.schedule(num_worker=12)
