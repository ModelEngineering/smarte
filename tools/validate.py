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
    observed_ts = model.simulate(noise_mag=noise_mag)
    # Construct true parameters
    true_parameters = lmfit.Parameters()
    for name, value in parameter_dct.items():
        true_parameters.add(name=name, value=value, min=value, max=value)
    # Initialize parameters
    parameters = lmfit.Parameters()
    for name, value in parameter_dct.items():
        if value > 0:
            try:
                model.set({name: value})
            except:
                continue
            parameters.add(name, min=value*F_LOWER, max=value*F_HIGHER,
                value=value*F_INITIAL)
    sfitter = smt.SBMLFitter(path, parameters, observed_ts)
    ser = sfitter.evaluate(true_parameters)
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    result = main(183, 1)
    import pdb; pdb.set_trace()

