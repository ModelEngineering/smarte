"""Creates workunits based on levels of factors"""

import smarte as smt
import smarte.constants as cn

import os


workunits = []
for method in ["differential_evolution", "leastsq"]:
    for num_latincube in [1, 2, 4, 8]:
        for noise_mag in [0.1, 0.2]:
            for max_fev in [1000, 10000]:
                workunit = smt.Workunit(method=method,
                      num_latincube=num_latincube,
                      noise_mag=noise_mag,
                      max_fev=max_fev)
                workunits.append(str(workunit))

with open(cn.WORKUNITS_FILE, "w") as fd:
    fd.write("\n".join(workunits))
