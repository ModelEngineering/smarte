"""This tool validates fitting algorithsm"""

"""
Constructs statistics for models in BioModels.
"""

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


def write_msg(model_num, msg, is_onlyreportsuccess):
    if "Success" in msg:
        print("\n***Model %d: %s" % (model_num, msg))
    elif (not is_onlyreportsuccess):
        print("\n***Model %d: %s" % (model_num, msg))
    else:
        pass
    return

def main(noise_mag=0, out_path=OUT_FILE, is_restart=True,
      is_onlyreportsuccess=True, **kwargs):
    """
    Compares the fitted and actual values of model parameters.

    Parameters
    ----------
    noise_mag: float (standard deviation added to true model)
    out_path: str (where output is saved)
    is_restart: bool (ignore prior output if it exists)
    is_onlyreportsuccess: bool (only report successfully processed files)
    kwargs: dict (optional parameters to iterateBiomodels)
    
    Returns
    -------
    Series
        index: parameter name
        value: fraction error from parameter estimate
    """
    if os.path.isfile(out_path) and (not is_restart):
        df = pd.read_csv(out_path)
        accum_dct = ExtendedDict(df.to_dict())
        accum_dct = {k: v for k,v in accum_dct.items() if not UNNAMED in k}
    else:
        accum_dct = ExtendedDict()
        df = pd.DataFrame({BIOMODEL_NUM: [-1]})
    for model_num, model in mdl.Model.iterateBiomodels(is_allerror=True, **kwargs):
        if not model_num in df[BIOMODEL_NUM].values:
            dct = {}
            if model is not None:
                try:
                    dct = smt.SBMLFitter.evaluateBiomodelFit(model, noise_mag)
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
            write_msg(model_num, dct[STATUS], is_onlyreportsuccess)
            # Create entry for missing models
            df.to_csv(out_path)
    # Handle the missing models
    final_df = df.sort_values(BIOMODEL_NUM)
    final_df.index = range(1, len(final_df)+1)
    for column in final_df.columns:
        if UNNAMED in column:
            del final_df[column]
    final_df.to_csv(out_path)
    print("Done!")
    

if __name__ == '__main__':
    main(num_model=1200, noise_mag=0.1, is_restart=True, start_num=1)
