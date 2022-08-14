"""Constants used in smarte"""
import os
import zipfile

END_TIME = 5  # Default simulation end time
START_TIME = 0  # Default simulation start time
TIME = "time"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT_DIR = os.path.join(PROJECT_DIR, "experiments")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
# Keys in statistics dictionary
SD_AVG_TIME = "avg_time"  #average time for an evaluation
SD_BIOMODEL_NUM = "biomodel_num"  #number of the biomodel
SD_COLUMNS_DELETED = "columns_deleted"  # Number of columns deleted in synthetic observational data
SD_CNT = "cnt"  #count of instances ran
SD_MAX_ERR = "max_err"  # parameter error with the largest absolute value
SD_MAX_FEV = "max_fev"  # Maximum number of function evaluations
SD_MEDIAN_ERR = "median_err"  # Median of the error values for a parameter
SD_METHOD = "method"  # Name of fitting algorithm
SD_MIN_ERR = "min_err"  # parameter error with the smallest absolute value
SD_NUM_SPECIES = "num_species"  #number of floating species
SD_NUM_REACTION = "num_reaction"  #number of reactions
SD_NUM_PARAMETER = "num_parameter"  #number of parameters
SD_TOT_TIME = "tot_time"  #total run time
SD_TS_INSTANCE = "ts_instance"  # instance of the synthetic observational data
SD_NOISE_MAG = "noise_mag"  #magnitude of the noise used
SD_RANGE_INITIAL_FRAC = "range_initial_frac"  # fraction of value for initial value
SD_RANGE_MAX_FRAC = "range_max_frac"  # fraction of value for max of range
SD_RANGE_MIN_FRAC = "range_min_frac"  # fraction of value for min of range
SD_STATUS = "status"  #str (reason for failure)
# A califier is something the descries the model or the experiment
# These values are not aggregated
SD_CONDITIONS = [SD_BIOMODEL_NUM, SD_METHOD, SD_NOISE_MAG,  SD_RANGE_MIN_FRAC,
      SD_RANGE_MAX_FRAC, SD_RANGE_INITIAL_FRAC, SD_COLUMNS_DELETED,
      SD_MAX_FEV, SD_TS_INSTANCE,]
SD_MODEL_DESCRIPTORS = [SD_NUM_SPECIES, SD_NUM_REACTION, SD_NUM_PARAMETER]
SD_QUALIFIERS = list(SD_MODEL_DESCRIPTORS)
SD_QUALIFIERS.extend(SD_CONDITIONS)
SD_QUALIFIERS.extend(SD_MODEL_DESCRIPTORS)
SD_ERROR_METRICS =  [SD_MEDIAN_ERR, SD_MAX_ERR, SD_MIN_ERR]
SD_TIME_METRICS =  [SD_AVG_TIME, SD_CNT, SD_TOT_TIME, ]
SD_METRICS = list(SD_ERROR_METRICS)
SD_METRICS.extend(SD_TIME_METRICS)
SD_METRICS.append(SD_STATUS)
SD_ALL = list(SD_QUALIFIERS)
SD_ALL.extend(SD_METRICS)
# Universal values for conditions
SD_CONDITION_VALUE_ALL = "*"
SD_CONDITION_VALUE_ALL_DCT = {
      SD_BIOMODEL_NUM: list(range(1, 1200)),
      SD_TS_INSTANCE:  list(range(1, 4)),
      }
