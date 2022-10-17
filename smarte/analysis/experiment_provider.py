"""Provides experiment data contained in a zip archive"""

import smarte.constants as cn
import smarte.util as ut
import smarte.analysis.util as uut
from smarte.types.elemental_type import isStr

import copy
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
BLC_SUFFIX = "_blc"  # suffix for best latincube


class ExperimentProvider(object):

    def __init__(self, filenames=None, directory=cn.EXPERIMENT_DIR,
          df=None, is_filter=True):
        """
        Parameters
        ----------
        filenames: list-str (names of zipfile including extenstion)
            Defaults to all zip files in directory
        directory: str (directory containing the zipfile)
        df: pd.DataFrame (if data already present)
        is_filter: bool (remove null records where fitting failed)
        """
        self.directory = directory
        self.filenames = filenames
        self.is_filter = is_filter
        if df is None:
            self.dff = self.makeDataframe(filenames=self.filenames,
                  directory=self.directory)
        else:
            self.dff = df.copy()
        self.dff = ut.cleanDf(self.dff)
        self.df = self.dff.copy()  # Keep the original dataframe
        self.df.index = range(len(self.df))
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
        add_df = self.calcBestLatincubeFits()
        self.df = pd.concat([self.df, add_df])

    def _makeTestData(self, max_ts_instance=2):
        """
        Used to construct test dataset.
        """
        df = self.dff[self.dff[cn.SD_TS_INSTANCE] <= max_ts_instance]
        return ut.cleanDf(df)

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
        ut.cleanDf(self.df, others=["level_"])

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
        # Find duplicate indices
        factor_all_df = self.df[self.factors]
        factor_dedup_df = factor_all_df.drop_duplicates()
        dup_idxs = set(factor_all_df.index).difference(factor_dedup_df.index)
        dup_df = copy.deepcopy(self.df.loc[dup_idxs, :])
        # Average values for these indices
        dup_dfg = dup_df.groupby(self.factors)
        sers = []
        for key, idxs in dup_dfg.groups.items():
            # Handle single duplicates
            if len(idxs) == 1:
                self.df.drop(index=idxs, axis=0)
            else:
                # Construct a new row that is the mean values of duplicates for factors
                ser = self.df.loc[idxs, cn.SD_METRICS].mean()
                for pos, factor in enumerate(self.factors):
                    ser[factor] = key[pos]
                ser[cn.SD_STATUS] = cn.SD_STATUS_SUCCESS
                self.df.drop(index=idxs, axis=0)
                sers.append(ser)
        add_df = pd.concat(sers, axis=1).transpose()
        self.df = pd.concat([self.df, add_df])
        #
        self._cleanDf()

    def makeCountSeries(self, factor):
        """
        Creates a series of counts for values (levels) of the factor in the data.

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

    def calcBestLatincubeFits(self, num_latincube=None):
        """
        Uses data from the ExperimentProvider to construct the results for a fitter
        whose parameter estimates are those for each distinct set of conditions
        the latincube_idxs 1 through num_latincube.

        Parameters
        ----------
        num_latincube: int (number of latincubes to use, sequential indices)
            default: maximum number

        Returns
        -------
        pd.DataFrame
            columns: same as self.df, except:
                <method> = <method>_blc (best latincube)
                latincube_idx = -1
        """
        conditions = list(cn.SD_CONDITIONS)
        if num_latincube is None:
            num_latincube = max(self.df[cn.SD_LATINCUBE_IDX])
        conditions.remove(cn.SD_LATINCUBE_IDX)
        df = self.df[self.df[cn.SD_LATINCUBE_IDX] > 0]
        dct = df.groupby(conditions).groups
        condition_df = pd.DataFrame(dct.keys(), columns = conditions)
        #
        sers = []
        for key, indexes in dct.items():
            idxs = list(indexes)
            count = min(num_latincube, len(idxs))
            idxs = idxs[0:count]
            sorted_idxs = sorted(idxs, key=lambda i: self.df.loc[i, cn.SD_RSSQ])
            min_idx = sorted_idxs[0]
            ser = pd.Series(self.df.loc[min_idx, :])
            ser[cn.SD_LATINCUBE_IDX] = -num_latincube
            ser[cn.SD_METHOD] += BLC_SUFFIX
            sers.append(ser)
        # Construct the dataframe
        df = pd.concat(sers, axis=1)
        df = ut.cleanDf(df.transpose())
        df.index = range(len(df))
        return df

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
            labels = uut.subsetLabels(ser.index, MAX_LABEL)
            ax.set_xticklabels(labels, rotation=45)
            if icol == 0:
                ax.set_ylabel("count (1000s)")
            else:
                ax.set_ylabel("")
        if is_plot:
            plt.show()
     
