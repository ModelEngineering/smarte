"""Calculates statistics on synthetic data, placing csv in directory"""

import smarte as smt
from smarte import constants as cn
import SBMLModel as mdl

import os
import lmfit
import numpy as np
import pandas as pd
import os


DIR_PAT = "%s--%s"
STATISTICS_FILE = "statistics.csv"


def main(noise_mag=0, start_num=1, num_model=1, num_replica=1):
    """
    Calculates statistics for CSV files.

    Parameters
    ----------
    noise_mag: float (units of std for noise)
    start_num: int (starting model)
    num_model: int (number of models)
    num_replica: int (number of replicas to process)

    Returns
    -------
    int (number of files written)
    """
    num_file = 0
    for model_num, model in mdl.Model.iterateBiomodels(
          start_num=start_num, num_model=num_model, is_allerror=True):
        dir_name = DIR_PAT % (str(model_num), str(noise_mag))
        dir_path = os.path.join(cn.DATA_DIR, dir_name)
        if not os.path.exists(dir_path):
            continue
        dct = {n: [] for n in [cn.REPL, cn.SSQ, cn.COUNT]}
        for replica in range(1, num_replica+1):
            file_path = os.path.join(dir_path, "%d.csv" % replica)
            if not os.path.isfile(file_path):
                  raise ValueError("Cannot file %s" % file_path)
            df = pd.read_csv(file_path)
            del df[cn.MILLISECONDS]
            # Calculate statistics
            count = len(df)*len(df.columns)
            ssq = df - df.mean()
            ssq = np.sum(np.sum(ssq**2))
            dct[cn.SSQ].append(ssq)
            dct[cn.COUNT].append(count)
            dct[cn.REPL].append(replica)
        # Write to csv
        statistic_df = pd.DataFrame(dct, columns=[cn.REPL, cn.SSQ, cn.COUNT])
        path = os.path.join(dir_path, STATISTICS_FILE)
        statistic_df.to_csv(path)
        num_file += 1
    return num_file
    

if __name__ == '__main__':
    num = main(num_model=1200, noise_mag=0, start_num=1, num_replica=3)
    print("***Added %d statistics files" % num)
