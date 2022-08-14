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

    def _writeMessage(self, model_num, msg, is_only_report_success):
        if "Success" in msg:
            print("\n***Model %d: %s" % (model_num, msg))
        elif (not is_only_report_success):
            print("\n***Model %d: %s" % (model_num, msg))
        else:
            pass
        return

    @staticmethod
    def makePath(condition, directory):
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

    def run(self, start_model=1, num_model=1, is_recover=True):
        """
        Runs experiment for all of BioModels. Has recovery capability
        where continues with an existing CSV file.

        Parameters
        ----------
        start_model: int
        num_model: int
        is_recover: bool (recover existing results if they exist)

        Returns
        -------
        dict
        """
        # Handle restart
        if os.path.isfile(self.out_path) and is_recover:
            df = pd.read_csv(self.out_path)
            results = ExperimentResult(df.to_dict())
        else:
            results = ExperimentResult()
        # Iterate across the models
        for model_num, model in mdl.Model.iterateBiomodels(is_allerror=True,
              start_model=start_model, num_model=num_model):
            result = ExperimentResult()
            if model is None:
                result[cn.SD_STATUS] = "Cannot create model."
            # Assign the qualifiers
            else:
                # TODO
                data_ts = self.getTimeseries()
                try:
                    new_dct = smt.SBMLFitter.evaluateBiomodelFit(cls,
                          model_num, observed_ts,
                          range_min_frac=condition[cn.SD_RANGE_MIN_FRAC],
                          range_max_frac=condition[cn.SD_RANGE_MAX_FRAC],
                          initial_value_frac=condition[cn.SD_INITIAL_VALUE_FRAC],
                          method_names=condition[cn.SD_METHOD],
                          max_fev=condition[cn.MAX_FEV],
                          )
                    result.update(dct)
                except (ValueError, RuntimeError) as exp:
                    result[cn.SD_STATUS] = str(exp)
            # Accumulate results
            results.append(dct)
            df = pd.DataFrame(results)
            self._writeMessage(model_num, dct[cn.SD_STATUS], is_only_report_success)
            # Create entry for missing models
            df.to_csv(out_path)
        # Handle the missing models
        final_df = df.sort_values(cn.SD_BIOMODEL_NUM)
        final_df = final_df.set_index(cn.SD_BIOMODEL_NUM)
        final_df = final_df[final_df[cn.SD_STATUS] == "Success!"]
        for column in final_df.columns:
            if UNNAMED in column:
                del final_df[column]
        final_df.to_csv(self.out_path)

    def getTimeseries(self):
        """
        Obtains the timeseries for the model and replication instance.

        Returns
        -------
        Timeseries
        """
        path = os.path.join(cn.DATA_DIR, str(self.condition[cn.SD_BIOMODEL_NUM]))
        filename = "%d.csv" % self.condition[cn.TS_INSTANCE]
        path = os.path.join(path, filename)
        return pd.read_csv(path)
