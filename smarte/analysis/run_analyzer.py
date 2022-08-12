"""Analyzes an experimental run consisting of many replications"""


from smarte.analysis.replication_analyzer import ReplicationAnalyzer
import smarte.constants as cn

import os
import pandas as pd
import numpy as np


CONDITION_SEP = "_"  # Separates conditions
KEY_VALUE_SEP = "--" # Separates the key and its value


class RunAnalyzer(object):
    # Aggregates replications for a run

    def __init__(self, path):
        """
        Constructs summary statistics for a run.

        Parameters
        ----------
        path: str (path to directory with replication CSVs)
        """
        self.repliications = self.getReplications(path)
        self.condition_dct = self.getConditionDct(path)

    @staticmethod
    def getReplications(path):
        """
        Constructs the replication for each CSV file in the path directory

        Parameters
        ----------
        path: str (directory)
        
        Returns
        -------
        list-ReplicationAnalyzer
        """
        ffile_names = os.listdir(path)
        csv_file_names = [f for f in ffile_names if ".csv" in f]
        csv_paths = [os.path.join(path, f) for f in csv_file_names]
        replications = [ReplicationAnalyzer(p) for p in csv_paths]
        return replications

    @staticmethod
    def getConditionDct(path):
        """
        Decodes the directory as a dictionary of conditions and values.

        Parameters
        ----------
        path: str (path to directory)
        
        Returns
        -------
        dict
            key: condition
            value: value of condition
        """
        dct = {}
        parts = path.split(CONDITION_SEP)
        for part in parts:
            pair = part.split(KEY_VALUE_SEP)
            try:
                value = int(pair[1])
            except:
                try:
                    value = float(pair[1])
                except:
                    value = pair[1]
            dct[pair[0]] = value
        return dct

    @staticmethod
    def mkPath(condition_dct):
        """
        Creates the path for the condition dictionary.

        Parameters
        ----------
        condition_dct: dict
            key: condition ("CD" constant)
            value: value of condition
        
        Returns
        -------
        str (path to directory)
        """
        filename_parts = [k + KEY_VALUE_SEP + str(v) for k, v in condition_dct.items()]
        return CONDITION_SEP.join(filename_parts)
