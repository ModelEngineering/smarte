"""Runs experiments for cn.SD_CONTROLLED_FACTORS"""

import smarte as smt
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
BIOMODEL_NUM = "biomodel_num"
STATUS = "status"
UNNAMED = "Unnamed:"
NONE_DCT = {k: None for k in cn.SD_ALL}
NUM_REPLICATION = 3


def getOutPath(num=None):
    if num is None:
        file_name = "biomodels_statistics.csv"
    else:
        file_name = "%d.csv" % num
    return os.path.join(cn.PROJECT_DIR, file_name)

def writeMessage(model_num, msg, is_only_report_success):
    if "Success" in msg:
        print("\n***Model %d: %s" % (model_num, msg))
    elif (not is_only_report_success):
        print("\n***Model %d: %s" % (model_num, msg))
    else:
        pass
    return


class ExperimentRunner(object):

    def __init__(self, condition_dct):
        """
        Parameters
        ----------
        condition_dct: dict
            key: cn.SD_CONTROLLED_FACTORS
            value: value of factor
        """
        self.condition_dct = condition_dct

    def run(self, start_model=1, num_model=1):
        """
        Runs experiment for all of BioModels.

        Returns
        -------
        dict
        """
        # TODO: Handle restart
        accum_dct = ExtendedDict({k: [] for k in cn.SD_ALL})
        for model_num, model in mdl.Model.iterateBiomodels(is_allerror=True,
              start_model=start_model, num_model=num_model):
            dct = dict(NONE_DCT)
            # Assign the qualifiers

            dct[cn.SD_NOISE_MAG] = noise_mag
            if model is not None:
                data_ts = getTimeseries(model_num, instance_num)
                try:
                    new_dct = smt.SBMLFitter.evaluateBiomodelFit(cls,
                          model_num, observed_ts,
                          range_min_frac=condition_dct[cn.SD_RANGE_MIN_FRAC],
                          range_max_frac=condition_dct[cn.SD_RANGE_MAX_FRAC],
                          initial_value_frac=condition_dct[cn.SD_INITIAL_VALUE_FRAC],
                          method_names=[condition_dct[cn.SD_METHOD],
                          max_fev=condition_dct[cn.MAX_FEV],
                          )

                    dct.update(new_dct)
                except (ValueError, RuntimeError) as exp:
                    dct[STATUS] = str(exp)
            else:
                dct[STATUS] = "Cannot create model."
            # Accumulate results
            if len(dct) > 1:
                accum_dct.append(dct)
            else:
                new_dct = dict(NONE_DCT)
                new_dct[BIOMODEL_NUM] = model_num
                new_dct[STATUS] = dct[STATUS]
                accum_dct.append(new_dct)
            df = pd.DataFrame(accum_dct)
            writeMessage(model_num, dct[STATUS], is_only_report_success)
            # Create entry for missing models
            df.to_csv(out_path)
    # Handle the missing models
    final_df = df.sort_values(BIOMODEL_NUM)
    final_df = final_df.set_index(BIOMODEL_NUM)
    final_df = final_df[final_df[cn.SD_STATUS] == "Success!"]
    for column in final_df.columns:
        if UNNAMED in column:
            del final_df[column]
    final_df.to_csv(out_path)
    

if __name__ == '__main__':
   for num in range(1, NUM_REPLICATION + 1):
       out_path = getOutPath(num)
       main(num_model=13, noise_mag=0.1, is_restart=True, start_num=1,
             out_path=out_path, max_fev=1000)
       print("\n\n***COMPLETE REPLICATION %d***" % num)
print("***DONE!***")
