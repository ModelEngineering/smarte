"""This tool validates fitting algorithsm"""

"""
Constructs statistics for models in BioModels.
"""

import smarte as smt
from smarte import constants as cn
from smarte.extended_dict import ExtendedDict
import analyzeSBML as anl

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

def main(noise_mag=0, out_path=OUT_FILE, **kwargs):
    """
    Compares the fitted and actual values of model parameters.

    Parameters
    ----------
    noise_mag: float (standard deviation added to true model)
    out_path: where output is saved
    kwargs: optional parameters to iterateBiomodels
    
    Returns
    -------
    Series
        index: parameter name
        value: fraction error from parameter estimate
    """
    if os.path.isfile(out_path):
        df = pd.read_csv(out_path)
        accum_dct = ExtendedDict(df.to_dict())
        accum_dct = {k: v for k,v in accum_dct.items() if not UNNAMED in k}
    else:
        accum_dct = ExtendedDict()
        df = pd.DataFrame({BIOMODEL_NUM: [-1]})
    missing_models = {}
    for model_num, model in anl.Model.iterateBiomodels(**kwargs):
        if not model_num in df[BIOMODEL_NUM].values:
            if model is not None:
                try:
                    dct = smt.SBMLFitter.evaluateBiomodelFit(model, noise_mag)
                    if len(dct) > 0:
                        accum_dct.append(dct)
                        print("\n***Model %d success!" % model_num)
                    else:
                        msg = "\n***Model %d: All parameters are 0 or are not muteable.\n"
                        print(msg % model_num)
                        missing_models[model_num] = "parameters are 0 or not muteable"
                except (ValueError, RuntimeError) as exp:
                    print("\n***Model %d: %s\n" % (model.biomodel_num, exp))
                    missing_models[model_num] = "exception"
            else:
                print("\n***Model %d: Model does not run!\n" % model_num)
                missing_models[model_num] = "does not run"
            df = pd.DataFrame(accum_dct)
            # Create entry for missing models
            df.to_csv(out_path)
    # Handle the missing models
    indices = list(df.index)
    ser = df.loc[indices[0], :]
    for idx in ser.index:
        ser.loc[idx] = None
    sers = []
    for key, value in missing_models.items():
        new_ser = ser.copy()
        new_ser.loc[BIOMODEL_NUM] = key
        new_ser.loc[STATUS] = value
        sers.append(new_ser)
    if len(sers) > 0:
        new_df = pd.concat(sers, axis=1).transpose()
        final_df = pd.concat([new_df, df], axis=0)
    else:
        final_df = df
    final_df = final_df.sort_values(BIOMODEL_NUM)
    final_df.index = range(1, len(final_df)+1)
    for column in final_df.columns:
        if UNNAMED in column:
            del final_df[column]
    final_df.to_csv(out_path)
    

if __name__ == '__main__':
    main(num_model=1000, noise_mag=0.1)
