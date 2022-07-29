"""Constants used in smarte"""
import os

END_TIME = 5  # Default simulation end time
START_TIME = 0  # Default simulation start time
TIME = "time"
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
