"""
Performs 1-way Analysis of Variance With Replications

Three kinds of columns are considered:
  instance columns specify instances of analysis
  factor columns indicate what is to be compared within an instance
  replication columns are factors that are treated as replications
  value_column contains values of what is being compared
"""

import collections
import numpy as np
import pandas as pd
from scipy.stats import f


# DataFrame columns
SSB = "ssb"  # sum of squares


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
        tdf = self.dfg.std()
        self.std_ser = tdf[self.value_name]
        self.fstat = self._calcFstatistic()

    def _calcFstatistic(self):
        """
        Calculates the Fstatisticistic

        Returns
        -------
        FStatistic
        """
        within_ssq = np.sum(self.std_ser*(self.count_ser - 1))
        between_ssq = np.sum(self.count_ser*self.mean_ser**2)  \
              - np.sum(self.value_ser**2)/self.num_tot
        within_df = self.num_tot - self.num_level
        stat = between_ssq/within_ssq
        between_df = self.num_level - 1
        sl = 1 - f.cdf(stat, within_df, between_df)
        return FStatistic(stat=stat, sl=sl, wdf=within_df, bdf=between_df)

        
        
 
