"""Creates workunits based on levels of factors"""

import smarte as smt
import smarte.constants as cn

import os


workunits = []
for method in ["differential_evolution", "leastsq"]:
    for range_initial_frac in [0.5, 0.8, 1.2, 1.5, 2.0]:
        for noise_mag in [0.1, 0.2]:
            workunit = smt.Workunit(method=method,
                  range_initial_frac=range_initial_frac,
                  noise_mag=noise_mag,
                  max_fev=10000)
            workunits.append(str(workunit))

with open(cn.WORKUNITS_FILE, "w") as fd:
    fd.write("\n".join(workunits))
