"""Creates workunits based on levels of factors"""

import smarte as smt
import smarte.constants as cn

import os


workunits = []
for max_fev in [1000]:
    for method in ["differential_evolution", "leastsq"]:
        for latincube_idx in range(1, 2):
            for noise_mag in [0.1, 0.2]:
                for ts_instance in [1, 2]:
                    workunit = smt.Workunit(
                          max_fev=max_fev,
                          method=method,
                          latincube_idx=latincube_idx,
                          noise_mag=noise_mag,
                          ts_instance=ts_instance,
                          )
                    workunits.append(str(workunit))

with open(cn.WORKUNITS_FILE, "w") as fd:
    fd.write("\n".join(workunits))
