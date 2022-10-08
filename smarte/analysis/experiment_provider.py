"""Provides experiment data contained in a zip archive"""

import smarte.constants as cn
import smarte.analysis.util as ut
from smarte.types.elemental_type import isStr

from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import zipfile

ZIP_EXT = ".zip"
MAX_LABEL = 5  # Maximum labels on a plot
# Deprecated symols
NUM_LATINCUBE = "num_latincube"


class ExperimentProvider(object):

    def __init__(self, filenames=None, directory=cn.EXPERIMENT_DIR,
          is_filter=True):
        """
        Parameters
        ----------
        filenames: list-str (names of zipfile including extenstion)
            Defaults to all zip files in directory
        directory: str (directory containing the zipfile)
        is_filter: bool (remove null records where fitting failed)
        """
        self.directory = directory
        self.filenames = filenames
        self.is_filter = is_filter
        self.df = self.makeDataframe(filenames=self.filenames, directory=self.directory)
        # Do fix-ups, handling evolution of experiment definitions
        self._fixup()
        self.factors = list(cn.SD_CONDITIONS)
        # Filtering
        if is_filter:
            self.filterUnsuccessfulExperiments()
            self.filterDuplicateConditions()

    def _fixup(self):
        """
        Fixes dataframe as a result of versioning issues.
        """
        columns = self.df.columns
        # Handle change from NUM_LATINCUBE -> LATINCUBE_IDX
        # This fix is not a correct interpretation of the calculations, but it creates
        # a usable factor name
        if NUM_LATINCUBE in columns:
            self.df = self.df.rename(columns={"num_latincube": cn.SD_LATINCUBE_IDX})
            self.df[cn.SD_LATINCUBE_IDX] = -1
        # Use the correct name for log ratio of error 
        self.df = self.df.rename(columns={
              "min_err": cn.SD_MIN_LOGERR,
              "median_err": cn.SD_MEDIAN_LOGERR,
              "max_err": cn.SD_MAX_LOGERR,
              })
        # Calculate the frc errors if they are not present
        if cn.SD_MIN_FRCERR not in columns:
            self.df[cn.SD_MIN_FRCERR] = self.df[cn.SD_MIN_LOGERR].apply(
                  lambda v: 2**v - 1)
            self.df[cn.SD_MEDIAN_FRCERR] = self.df[cn.SD_MEDIAN_LOGERR].apply(
                  lambda v: 2**v - 1)
            self.df[cn.SD_MAX_FRCERR] = self.df[cn.SD_MAX_LOGERR].apply(
                  lambda v: 2**v - 1)

    def _makeTestData(self):
        """
        Used to construct test dataset.
        """
        self.df.index = list(range(len(self.df)))
        indices = list(self.df.index)
        new_df = self.df.loc[indices[:1000], :]
        new_df.to_csv("test_experiment_provider.csv")

    @classmethod
    def getZippaths(cls, filenames=None, directory=cn.EXPERIMENT_DIR):
        """
        Retrieves all zipfiles in the directory.
        
        Parameters
        ----------
        filenames: list-str
        directory: str
        
        Returns
        -------
        list-str (paths to zipfiles)
        """
        if filenames is None:
            ffiles = os.listdir(directory)
            filenames = [f for f in ffiles if f[-4:] == ZIP_EXT]
        elif isStr(filenames):
            filenames = [filenames]
        else:
            filenames = list(filenames)
        return [os.path.join(directory, f) for f in filenames]

    @classmethod
    def makeDataframe(cls, **kwargs):
        """
        Reads CSVs in a zipfile.
        
        Parameters
        ----------
        kwargs: dict (arguments for getZippaths)
        
        Returns
        -------
        pd.DataFrame
        """
        dfs = []
        for zip_path in cls.getZippaths(**kwargs):
            with zipfile.ZipFile(zip_path) as myzip:
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
        non_null = [not n for n in self.df[cn.SD_MEDIAN_LOGERR].isnull().values]
        self.df = self.df[non_null]
        self._cleanDf()

    def filterDuplicateConditions(self):
        """
        Averages duplicate conditions.
        """
        dfg = self.df.groupby(self.factors).mean()
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

    def plotFactorCounts(self, is_plot=True, exclude_factors=[cn.SD_BIOMODEL_NUM]):
        """
        Bar plots of counts of each factor in the condition.
        """
        factors = [f for f in self.factors if not f in exclude_factors]
        if cn.SD_METHOD in factors:
            factors.remove(cn.SD_METHOD)
            factors.append(cn.SD_METHOD)  # put on bottom row
        num_plot = len(factors)
        num_col = 3
        num_row = num_plot//num_col
        if num_row*num_col < num_plot:
            num_row += 1
        figure, axes = plt.subplots(num_row, num_col, figsize=(10,10))
        plt.subplots_adjust(hspace=0.4)
        for idx, factor in enumerate(factors):
            icol = np.mod(idx, num_col)
            irow = int(idx//num_col)
            ax = axes[irow, icol]
            ser = self.makeCountSeries(factor)/1000
            ser.index = [str(i)[:5] if len(str(i)) > 5 else str(i) for i in ser.index]
            ser.plot.bar(ax=ax)
            ax.set_title(factor)
            labels = ut.subsetLabels(ser.index, MAX_LABEL)
            ax.set_xticklabels(labels, rotation=45)
            if icol == 0:
                ax.set_ylabel("count (1000s)")
            else:
                ax.set_ylabel("")
        if is_plot:
            plt.show()
     
