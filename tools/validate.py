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

F_LOWER = 0.25  # Lower end of range for value search
F_HIGHER = 4.0  # Upper end of range for value search
F_INITIAL = F_LOWER  # Starting point for search

def main(model_num, noise_mag):
    """
    Compares the fitted and actual values of model parameters.

    Parameters
    ----------
    model_num: int (model number in data directory)
    noise_mag: float (standard deviation added to true model)
    
    Returns
    -------
    Series
        index: parameter name
        value: fraction error from parameter estimate
    """
    model = smt.Fitterpp.getDataPath(model_num)
    parameter_dct = model.get(model.parameter_names)
    data_ts = model.simulate()
    nrow = len(data_ts)
    ncol = len(data_ts.columns)
    random_arr = noise_mag*np.random.rand(nrow*ncol)
    random_arr = np.reshape(random_arr, (nrow, ncol))
    random_df = pd.DataFrame(random_arr, columns=data_ts.columns,
        index=data_ts.index)
    observed_df = pd.DataFrame(data_ts) + random_df
    observed_ts = anl.Timeseries(observed_df)
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
    value_dct = sfitter.fitter.final_params.valuesdict()
    error_dct = {n: np.nan if v == 0 else (parameter_dct[n] - v)/parameter_dct[n]
           for n, v in value_dct.items()}
    # Calculate estimation errors
    error_ser = pd.Series(error_dct, index=value_dct.keys())
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    result = main(183, 1)
    import pdb; pdb.set_trace()

