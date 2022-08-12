"""Constants used in smarte"""
import os

END_TIME = 5  # Default simulation end time
START_TIME = 0  # Default simulation start time
TIME = "time"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT_DIR = os.path.join(PROJECT_DIR, "experiments")
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
SD_NOISE_INSTANCE = "noise_instance"  # instance of the noise magnitude
SD_NOISE_MAG = "noise_mag"  #magnitude of the noise used
SD_RANGE_INITIAL_FRAC = "range_max_frac"  # fraction of value for initial value
SD_RANGE_MAX_FRAC = "range_max_frac"  # fraction of value for max of range
SD_RANGE_MIN_FRAC = "range_min_frac"  # fraction of value for min of range
SD_STATUS = "status"  #str (reason for failure)
# A califier is something the descries the model or the experiment
# These values are not aggregated
SD_CONTROLLED_FACTORS = [SD_METHOD, SD_NOISE_MAG,  SD_RANGE_MIN_FRAC,
      SD_RANGE_MAX_FRAC, SD_RANGE_INITIAL_FRAC, SD_COLUMNS_DELETED,
      SD_MAX_FEV, SD_NOISE_INSTANCE,]
SD_QUALIFIER =  [SD_BIOMODEL_NUM,
      SD_NUM_SPECIES, SD_NUM_REACTION, SD_NUM_PARAMETER, SD_STATUS,
      ]
SD_QUALIFIER.extend(SD_CONTROLLED_FACTORS)
SD_METRIC_ERROR =  [SD_MEDIAN_ERR, SD_MAX_ERR, SD_MIN_ERR]
SD_METRIC_TIME =  [SD_AVG_TIME, SD_CNT, SD_TOT_TIME, ]
SD_METRIC = list(SD_METRIC_ERROR)
SD_METRIC.extend(SD_METRIC_TIME)
SD_ALL = list(SD_QUALIFIER)
SD_ALL.extend(SD_METRIC)
# Condition keys
CD_NOISE = "Noise"
CD_COLUMNS_DELETED = "ColumnsDeleted"
CD_RANGE_MAX = "RangeMax"  # In units of fraction of the true parameter value
CD_RANGE_MIN = "RangeMin"  # In units of fraction of the true parameter value
CD_MAX_FEV = "Maxfev"
CD_ALL = [CD_NOISE, CD_COLUMNS_DELETED, CD_RANGE_MAX, CD_RANGE_MIN,
      CD_MAX_FEV]
