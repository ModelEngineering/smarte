"""Creates Latin Cube Entries

Creates a CSV file whose columns are stripes in the latin cube and whose
rows are random numbers within the stripe.

"""

import smarte.constants as cn

import lhsmdu
import os
import pandas as pd
import numpy as np


NUM_PARAMETER = 500
NUM_LATINCUBE = 10
OUT_PATH = os.path.join(cn.DATA_DIR, "latin_cube.csv")

samples = lhsmdu.sample(NUM_PARAMETER, NUM_LATINCUBE)
df = pd.DataFrame(samples)
df.columns = range(1, len(df.columns)+ 1)
df.to_csv(OUT_PATH, index=True)
print("***Latin cube written to %s" % OUT_PATH)
