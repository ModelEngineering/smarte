"""Analyzes an experimental run, replications with the same factor levels."""

"""
An experimental run consists of one or more replications, and each replication
has one or more simulations. A simulation is parameterized by the following factors:
    Parameter min, max
    Column deleted
    Noise_mag: randomness introduced in observational data
    Maximum number of function evalutions
    Algorithm
    Parameter initial value
    BioModel

A replication contains simulations for multiple algorithms and BioModels, and 
each algorithm for the same BioModel uses the same initial value for each parameter
and the same synthetic observational data for each model.
A replication is contained in a single CSV file.

An experimental run constists of multiple replications, each of which uses a different
initial value and different observational data for each parameter and BioModel.
"""

import smarte.constants as cn

import pandas as pd
import numpy as np


class ReplicationAnalyzer(object):
    # Creates a clean replication DataFrame
    # Eliminates superfluous columns


    def __init__(self, path):
        """
        Handles missing simulations in a replication.
        
        Parameters
        ----------
        path: str (path to replication CSV)
        """
        self.path = path
        df = pd.read_csv(path)
        keeps = [i == "Success!" for i in df[cn.SD_STATUS]]
        for column in df.columns:
            if "Unnamed:" in column:
                del df[column]
        del df[cn.SD_STATUS]
        self.df = df[keeps]
        self.df = self.df.set_index(cn.SD_BIOMODEL_NUM)

    def serialize(self, path):
        self.df.to_csv(path)


class RunAnalyzer(object):
    # Aggregates replications for a run

    def __init__(self, path):
        """
        Constructs summary statistics for a run.

        Parameters
        ----------
        path: str (path to directory with replication CSVs)
        """
        #self.repliications =
