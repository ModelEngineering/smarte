"""
Performs 1-way Analysis of Variance With Replications

Three kinds of columns are considered:
  instance columns specify instances of analysis
  factor columns indicate what is to be compared within an instance
  replication columns are factors that are treated as replications
  value_column contains values of what is being compared
"""
import smarte.analysis.util as ut
import smarte.constants as cn

import collections
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import f


# DataFrame columns
INSTANCE = "instance"
SEPARATOR = "__"  # Separates names in instances
MAX_LABEL = 5


# stat: F ratio
# sl: signicance level
# wdf: within degrees of freedom
# bdf: between degrees of freedom
FStatistic = collections.namedtuple("FStatistic", "stat sl wdf bdf")

class Anova(object):

    def __init__(self, df, factor_name, replication_name, value_name):
        """
        Parameters
        ----------
        factor_name: str (name of factor whose levels are compared)
        replication_name: str (column that identifies replications of the factor level)
        value_column: str (value compared)
        df: pd.DataFrame
            index: instances
            columns: factor_name, replication_name
        """
        self.factor_name = factor_name
        self.replication_name = replication_name
        self.value_name = value_name
        self.columns = [self.value_name, self.factor_name, self.replication_name]
        self.df = df[self.columns]
        self.dfg = self.df.groupby(factor_name)
        self.value_ser = self.df[self.value_name]
        # Calculate statistics
        self.num_tot = len(self.df)
        self.levels = list(self.dfg.indices.keys())
        self.num_level = len(self.levels)
        tdf = self.dfg.count()
        self.count_ser = tdf[self.value_name]
        tdf = self.dfg.mean()
        self.mean_ser = tdf[self.value_name]
        tdf = self.dfg.var()
        self.var_ser = tdf[self.value_name]
        self.fstat = self._calcFstatistic()

    def _calcFstatistic(self):
        """
        Calculates the Fstatisticistic

        Returns
        -------
        FStatistic
        """
        within_ssq = np.sum(self.var_ser*(self.count_ser - 1))
        between_ssq = np.sum(self.count_ser*self.mean_ser**2)  \
              - np.sum(self.value_ser**2)/self.num_tot
        within_df = self.num_tot - self.num_level
        between_df = self.num_level - 1
        if (np.isclose(within_ssq, 0)) or (between_df == 0):
            sl = 1
            stat = np.nan
        else:
            stat = between_ssq/within_ssq
            sl = 1 - f.cdf(stat, within_df, between_df)
        return FStatistic(stat=stat, sl=sl, wdf=within_df, bdf=between_df)

    @classmethod
    def calcSl(cls, instance_names, df, factor_name, replication_name, value_name):
        """
        Calculates significance levels for all distinct alues of instance_names
        and plots them.

        Parameters
        ----------
        instance_names: list-str (columns that define instances)
        factor_name: str (name of factor whose levels are compared)
        replication_name: str (column that identifies replications of the factor level)
        value_column: str (value compared)
        df: pd.DataFrame
            index: instances
            columns: factor_name, replication_name

        Returns
        -------
        pd.Series
            index: values of instance_names
            value: significance levels
        """
        # Construct the instance column
        instances = []
        new_df = df.copy()
        new_df[INSTANCE] = ""
        is_first = True
        for column in instance_names:
            if is_first:
                ser = new_df[column].astype(str)
                is_first = False
            else:
                ser = new_df[INSTANCE] + SEPARATOR + new_df[column].astype(str)
            new_df[INSTANCE] = ser
        instances = list(new_df[INSTANCE].values)
        # Construct the significance levels
        sls = []
        instance_idxs = list(set(instances))
        for instance in instance_idxs:
            t_df = new_df[new_df[INSTANCE] == instance]
            anova = Anova(t_df, factor_name, replication_name, value_name)
            sls.append(anova.fstat.sl)
        ser = pd.Series(sls, index=instance_idxs)
        return ser

    @classmethod
    def plotSl(cls, df, factor_name, replication_name, value_name,
          is_plot=True, ax=None, marker_color="blue", title_prefix=""):
        """
        Calculates significance levels for all distinct alues of instance_names
        and plots them.

        Parameters
        ----------
        factor_name: str (name of factor whose levels are compared)
        replication_name: str (column that identifies replications of the factor level)
        value_column: str (value compared)
        df: pd.DataFrame
            index: instances
            columns: factor_name, replication_name
        is_plot: bool
        """
        ser = cls.calcSl([cn.SD_BIOMODEL_NUM], df, factor_name, replication_name,
              value_name)
        if ax is None:
            fig, ax = plt.subplots(1, figsize=(10, 10))
        plot_ser = -np.log10(ser)
        indices = [int(i) for i in plot_ser.index]
        ax.scatter(indices, plot_ser, marker="*", color=marker_color)
        ax.set_xticks(np.arange(100, max(indices), 100))
        ax.plot([min(indices), max(indices)], [2, 2], linestyle="--")
        ax.set_xlabel(cn.SD_BIOMODEL_NUM)
        ax.set_ylabel("-log10 sl")
        ax.set_title(title_prefix + factor_name)
        if is_plot:
            plt.show()
