"""Creates synthetic data for valid biomodels."""

import smarte as smt
from smarte import constants as cn
import SBMLModel as mdl

import os
import lmfit
import numpy as np
import pandas as pd
import os


DIR_PAT = "%s--%s"

def main(noise_mag=0, start_num=1, num_model=1, num_replica=1, is_force=False):
    """
    Creates replicas of synthetic data. Result are in the data directory.

    Parameters
    ----------
    noise_mag: float (units of std for noise)
    start_num: int (starting model)
    num_model: int (number of models)
    num_replica: int (number of replicas created)
    is_force: bool (overwrite existing file)

    Returns
    -------
    int (number files added)
    """
    num_added = 0
    for model_num, model in mdl.Model.iterateBiomodels(
          start_num=start_num, num_model=num_model, is_allerror=True):
        dir_name = DIR_PAT % (str(model_num), str(noise_mag))
        dir_path = os.path.join(cn.DATA_DIR, dir_name)
        if noise_mag > 0:
            data = smt.SBMLFitter.makeBiomodelSyntheticData(model_num, noise_mag,
                num_dataset=num_replica)
        else:
            # Do separate simulations
            data = []
            for _ in range(num_replica):
                new_data = smt.SBMLFitter.makeBiomodelSyntheticData(model_num,
                    noise_mag, num_dataset=1)
                if len(new_data) > 0:
                    data.append(new_data[0])
        for idx, ts in enumerate(data):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            num = idx + 1
            filename = "%d.csv" % num
            path = os.path.join(dir_path, filename)
            if (not os.path.isfile(path)) or is_force:
                num_added += 1
                ts.to_csv(path, index=True)
    return num_added
    

if __name__ == '__main__':
    num = main(num_model=1200, noise_mag=0, start_num=578111, num_replica=3, is_force=True)
    print("***Added %d CSV files" % num)
