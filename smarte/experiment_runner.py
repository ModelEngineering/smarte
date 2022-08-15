"""Runs experiments for cn.SD_CONTROLLED_FACTORS"""


import smarte as smt
from smarte.experiment_condition import ExperimentCondition
from smarte import constants as cn
from smarte.extended_dict import ExtendedDict
import SBMLModel as mdl

import os
import lmfit
import numpy as np
import pandas as pd
import os

F_LOWER = 0.25  # Lower end of range for value search
F_HIGHER = 4.0  # Upper end of range for value search
F_INITIAL = F_LOWER  # Starting point for search
OUT_FILE = os.path.join(cn.PROJECT_DIR, "biomodels_statistics.csv")
NUM_REPLICATION = 3


class ExperimentRunner(object):

    def __init__(self, condition, directory=cn.EXPERIMENT_DIR):
        """
        Parameters
        ----------
        condition: ExperimentCondition
        """
        self.condition = condition
        self.directory = directory
        self.out_path = self.makePath(self.condition, self.directory)

    def _writeMessage(self, model_num, msg, is_report):
        if is_report:
            print("\n***Model %d: %s" % (model_num, msg))
        return

    @staticmethod
    def makePath(condition, directory=cn.EXPERIMENT_DIR):
        """
        Consturcts a path to the CSV file for the conditions used in this experiment.

        Parameters
        ----------
        condition: ExperimentCondition
        directory: str

        Returns
        -------
        str
        """
        filename = "%s.csv" % str(condition)
        return os.path.join(directory, filename)

    def run(self, is_recover=True, is_report=True):
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
        # Handle restart
        if os.path.isfile(self.out_path) and is_recover:
            df = pd.read_csv(self.out_path)
            results = smt.ExperimentResult.makeAggregateResult(df)
        else:
            results = smt.ExperimentResult.makeAggregateResult()
        # Iterate across the models
        for condition in self.condition.iterator:
            biomodel_num = condition[cn.SD_BIOMODEL_NUM]
            result = smt.ExperimentResult(**condition)
            model = mdl.Model.getBiomodel(biomodel_num)
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
                          initial_value_frac=condition[cn.SD_RANGE_INITIAL_FRAC],
                          method_names=condition[cn.SD_METHOD],
                          max_fev=condition[cn.SD_MAX_FEV],
                          )
                    result.update(new_result)
                except (ValueError, RuntimeError) as exp:
                    result[cn.SD_STATUS] = str(exp)
                # Accumulate results
                results.append(result)
            # Save the results
            df = pd.DataFrame(results)
            df.to_csv(self.out_path)
            #
            self._writeMessage(biomodel_num, result[cn.SD_STATUS],
                  is_report=is_report)
        # Handle the missing models
        final_df = df.sort_values(cn.SD_BIOMODEL_NUM)
        final_df = final_df.set_index(cn.SD_BIOMODEL_NUM)
        final_df = final_df[final_df[cn.SD_STATUS] == "Success!"]
        final_df.to_csv(self.out_path)
        return final_df

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
        # TODO: fix data so this is no longer needed
        if "miliseconds" in df.columns:
            df = df.rename(columns={"miliseconds": cn.MILLISECONDS})
        df = df.set_index(cn.MILLISECONDS)
        return df

    @classmethod
    def readCsv(cls, path=None, condition=None, directory=cn.EXPERIMENT_DIR):
        """
        Reads the CSV file for a condition.

        Parameters
        ----------
        path: str (explicit path to use)
        condition: ExperimentCondition (used to infer path if no explicit path)
        directory: str (contains file)
        
        Returns
        -------
        DataFrame
            columns: cn.SD_ALL
            index: int (biomodel number)
        """
        if path is None:
            path = cls.makePath(condition, directory)
        df = pd.read_csv(path)
        df = df.set_index(cn.SD_BIOMODEL_NUM)
        return df

if __name__ == '__main__':
    condition = smt.ExperimentCondition(biomodel_num=list(range(1, 11)),
          ts_instance=[1,2])
    runner = smt.ExperimentRunner(condition)
    runner.run()
