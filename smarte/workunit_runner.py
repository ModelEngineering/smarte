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
from smarte.result import Result
from smarte.workunit import Workunit
import SBMLModel as mdl

import argparse
import os
import pandas as pd
import sys

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
                except (ValueError, RuntimeError) as exp1:
                    result[cn.SD_STATUS] = str(exp1)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runs simulations for a workunit.")
    parser.add_argument("workunit_str", type=str,
          help="workunit in string representation")
    args = parser.parse_args()
    for key in cn.SD_CONDITIONS:
        if not key in args.workunit_str:
            print("*** Input Error. Workunit is missing '%s'." % key)
            sys.exit(-1)
    # Recover the workunit if it exists
    try:
        a_workunit = Workunit.deserialize(args.workunit_str, out_dir=cn.EXPERIMENT_DIR)
    except Exception as exp:
        # Not present. Create a new workunit.
        try:
            a_workunit = Workunit.makeFromStr(args.workunit_str)
        except Exception as exp1:
            print(exp1)
            raise ValueError("*** Input Error: Bad workunit string: %s"
                  % args.workunit_str)
    #
    runner = WorkunitRunner(a_workunit)
    _ = runner.run()
    print("\n***COMPLETED %s" % args.workunit_str)
