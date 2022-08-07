"""Constants used in smarte"""
import os

END_TIME = 5  # Default simulation end time
START_TIME = 0  # Default simulation start time
TIME = "time"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT_DIR = os.path.join(PROJECT_DIR, "experiments")
# Keys in statistics dictionary
SD_AVG_ERR = "avg_err"  #average error in parameter estimation
SD_AVG_TIME = "avg_time"  #average time for an evaluation
SD_BIOMODEL_NUM = "biomodel_num"  #number of the biomodel
SD_CNT = "cnt"  #count of instances ran
SD_MAX_ERR = "max_err"  #largest error in parameter estimation
SD_METHOD = "method"  #evaluation method
SD_MIN_ERR = "min_err"  #smallest error in parameter estimation
SD_NUM_SPECIES = "num_species"  #number of floating species
SD_NUM_REACTIONS = "num_reactions"  #number of reactions
SD_NUM_PARAMETERS = "num_parameters"  #number of parameters
SD_TOT_TIME = "tot_time"  #total run time
SD_NOISE_MAG = "noise_mag"  #magnitude of the noise used
SD_STATUS = "status"  #str (reason for failure)
SD_ALL =  [SD_AVG_ERR, SD_AVG_TIME, SD_BIOMODEL_NUM, SD_CNT, SD_MAX_ERR, SD_METHOD,
      SD_MIN_ERR, SD_NUM_SPECIES, SD_NUM_REACTIONS, SD_NUM_PARAMETERS, SD_TOT_TIME,
      SD_NOISE_MAG, SD_STATUS,
      ]
