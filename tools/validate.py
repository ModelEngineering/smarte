"""This tool validates fitting algorithsm"""

"""
The tools checks how the fitted parameters compare with
the actual parameters.
"""

import smarte as smt
import analyzeSBML as anl

import lmfit
import numpy as np
import pandas as pd
import os

PREFIX = "BIOMD0000000%03d.xml"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
F_LOWER = 0.25  # Lower end of range for value search
F_HIGHER = 4.0  # Upper end of range for value search
F_INITIAL = F_LOWER  # Starting point for search

def main(model_num, noise_std):
    """
    Compares the fitted and actual values of model parameters.

    Parameters
    ----------
    model_num: int (model number in data directory)
    noise_std: float (standard deviation added to true model)
    
    Returns
    -------
    Series
        index: parameter name
        value: fraction error from parameter estimate
    """
    path = os.path.join(DATA_DIR, PREFIX % model_num)
    model = anl.Model(path)
    parameter_dct = model.get(model.parameter_names)
    data_ts = model.simulate()
    data_df = data_ts.applymap(lambda v: v + np.random.rand(noise_std))
    observed_ts = anl.Timeseries(data_df)
    # Do the fit
    parameters = lmfit.Parameters()
    for name, value in parameter_dct.items():
        if value > 0:
            try:
                model.set({name: value})
            except:
                continue
            parameters.add(name, min=value*F_LOWER, max=value*F_HIGHER,
                value=value*F_INITIAL)
    sfitter = smt.SBMLFitter(path, observed_ts, parameters)
    sfitter.fit()
    value_dct = sfitter.final_params.valuesdict()
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    result = main(183, 1)
    import pdb; pdb.set_trace()

