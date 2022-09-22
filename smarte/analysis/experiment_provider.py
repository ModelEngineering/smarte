"""Provides experiment data contained in a zip archive"""

import smarte.constants as cn

from io import StringIO
import numpy as np
import os
import pandas as pd
import zipfile


class ExperimentProvider(object):

    def __init__(self, filename="experiments.zip", directory=cn.EXPERIMENT_DIR,
          is_filter=True):
        """
        Parameters
        ----------
        filename: str (name of zipfile including extenstion)
        directory: str (directory containing the zipfile)
        """
        self.path= os.path.join(directory, filename)
        self.is_filter = is_filter
        self.df = self.extractZipped()
        self.conditions = list(cn.SD_CONDITIONS)
        if "num_latincube" in self.df.columns:
            self.conditions.remove(cn.SD_LATINCUBE_IDX)
            self.conditions.append("num_latincube")
        if is_filter:
            self.filterUnsuccessfulExperiments()
            self.filterDuplicateConditions()

    def _makeTestData(self):
        """
        Used to construct test dataset.
        """
        self.df.index = list(range(len(self.df)))
        indices = list(self.df.index)
        new_df = self.df.loc[indices[:1000], :]
        new_df.to_csv("test_experiment_provider.csv")

    def extractZipped(self):
        """
        Reads CSVs in a zipfile.
        
        Returns
        -------
        pd.DataFrame
        """
        dfs = []
        with zipfile.ZipFile(self.path) as myzip:
            for ffile in myzip.namelist():
                with myzip.open(ffile) as myfile:
                    byte_lines = (myfile.readlines())
                    lines = [l.decode() for l in byte_lines]
                    lines = "\n".join(lines)
                    df = pd.read_csv(StringIO(lines))
                    dfs.append(df)
        return pd.concat(dfs)

    def _cleanDf(self):
        self.df = self.df.reset_index()
        self.df.index = list(range(len(self.df)))
        columns = list(self.df.columns)
        for column in columns:
            if "Unnamed:" in column:
                del self.df[column]
            if "level_" in column:
                del self.df[column]

    def filterUnsuccessfulExperiments(self):
        """
        Removes experiments that did not produce data.
        """
        self.df = self.df[self.df[cn.SD_STATUS] == cn.SD_STATUS_SUCCESS]
        non_null = [not n for n in self.df[cn.SD_MEDIAN_ERR].isnull().values]
        self.df = self.df[non_null]
        self._cleanDf()

    def filterDuplicateConditions(self):
        """
        Averages duplicate conditions.
        """
        dfg = self.df.groupby(self.conditions).mean()
        self.df = pd.DataFrame(dfg)
        self.df = self.df.reset_index()
        self._cleanDf()

    def makeCountSeries(self, factor):
        """
        Creates a series of counts for values of the factor in the data.

        Parameters
        ----------
        factor: str (condition)
        
        Returns
        -------
        Series
            index: value of factor
            value: count of occurrences in data
        """
        df = pd.DataFrame(self.df.groupby(factor).count())
        return df[cn.SD_TOT_TIME]  # Pick a non-condition column for count values

    def plotConditionCounts(self, is_plot=True):
        """
        Bar plots of counts of each condition value.
        """
        pass
