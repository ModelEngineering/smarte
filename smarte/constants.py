"""Constants used in smarte"""

from smarte.types.mv_dict import ALL

import os
import zipfile


"""
Metric notes
     logerr = log2(predicted/actual)
     frcerr = (predicted - actual)/actual
"""

END_TIME = 5  # Default simulation end time
START_TIME = 0  # Default simulation start time
TIME = "time"
MILLISECONDS = "milliseconds"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT_DIR = os.path.join(PROJECT_DIR, "experiments")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
WORKUNITS_FILE = os.path.join(EXPERIMENT_DIR, "workunits.txt")
# Keys in statistics dictionary
SD_AVG_TIME = "avg_time"  #average time for an evaluation
SD_BIOMODEL_NUM = "biomodel_num"  #number of the biomodel
SD_COLUMNS_DELETED = "columns_deleted"  # Number of columns deleted in synthetic observational data
SD_CNT = "cnt"  #count of instances ran
SD_MAX_FRCERR = "max_frcerr"  # parameter error with the largest absolute value in frac
SD_MAX_LOGERR = "max_logerr"  # largest absolute value in log ratio
SD_MAX_FEV = "max_fev"  # Maximum number of function evaluations for an application
#                         of a method. For multistart (latincube), this maximum
#                         is used for each instance.
SD_MEDIAN_FRCERR = "median_frcerr"  # Median of the frc error values for a parameter
SD_MEDIAN_LOGERR = "median_logerr"  # Median of the log error values for a parameter
SD_METHOD = "method"  # Name of fitting algorithm
SD_MIN_FRCERR = "min_frcerr"  # frc error with the smallest absolute value
SD_MIN_LOGERR = "min_logerr"  # log ratio error with the smallest absolute value
SD_NUM_SPECIES = "num_species"  #number of floating species
SD_NUM_REACTION = "num_reaction"  #number of reactions
SD_NUM_PARAMETER = "num_parameter"  #number of parameters
SD_RSSQ = "rssq"  # residual sum of squares for fit
SD_TOT_TIME = "tot_time"  #total run time
SD_TS_INSTANCE = "ts_instance"  # instance of the synthetic observational data
SD_NOISE_MAG = "noise_mag"  #magnitude of the noise used
SD_LATINCUBE_IDX = "latincube_idx"  # index of the latin cube strip used
SD_RANGE_MAX_FRAC = "range_max_frac"  # fraction of value for max of range
SD_RANGE_MIN_FRAC = "range_min_frac"  # fraction of value for min of range
SD_STATUS = "status"  #str (reason for failure)
# Universal values for conditions
SD_CONDITION_VALUE_ALL = ALL
SD_CONDITION_EXPANSION_DCT = {
      SD_BIOMODEL_NUM: list(range(1, 1060)),
      SD_LATINCUBE_IDX: list(range(1, 11)),  # 10 latin cubes
      SD_TS_INSTANCE:  list(range(1, 6)),
      }
# A califier is something the descries the model or the experiment
# These values are not aggregated
SD_CONDITION_DCT = {
      SD_BIOMODEL_NUM: SD_CONDITION_VALUE_ALL,
      SD_COLUMNS_DELETED: 0,
      SD_MAX_FEV: 1000,
      SD_METHOD: "differential_evolution",
      SD_NOISE_MAG: 0,
      SD_LATINCUBE_IDX: SD_CONDITION_VALUE_ALL,
      SD_RANGE_MIN_FRAC: 0.5,
      SD_RANGE_MAX_FRAC: 2.0,
      SD_TS_INSTANCE: SD_CONDITION_VALUE_ALL,
}
SD_CONDITIONS = list(SD_CONDITION_DCT.keys())
SD_MODEL_DESCRIPTORS = [SD_NUM_SPECIES, SD_NUM_REACTION, SD_NUM_PARAMETER]
SD_QUALIFIERS = list(SD_MODEL_DESCRIPTORS)
SD_QUALIFIERS.extend(SD_CONDITIONS)
SD_ERROR_METRICS =  [SD_MEDIAN_LOGERR, SD_MAX_LOGERR, SD_MIN_LOGERR, SD_RSSQ,
      SD_MEDIAN_FRCERR, SD_MAX_FRCERR, SD_MIN_FRCERR,
      ]
SD_TIME_METRICS =  [SD_AVG_TIME, SD_CNT, SD_TOT_TIME, ]
SD_METRICS = list(SD_ERROR_METRICS)
SD_METRICS.extend(SD_TIME_METRICS)
SD_METRICS.append(SD_STATUS)
SD_ALL = list(SD_QUALIFIERS)
SD_ALL.extend(SD_METRICS)
SD_ALL_DCT = {k: None for k in SD_ALL}
{SD_ALL_DCT.update({k: v}) for k, v in SD_CONDITION_DCT.items()}
# Field values
SD_STATUS_SUCCESS = "Success!"
# Miscellaneous
VALUE_SEP = "--"
