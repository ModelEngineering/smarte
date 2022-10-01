"""
Performs 1-way Analysis of Variance With Replications

Three kinds of columns are considered:
  instance columns specify instances of analysis
  factor columns indicate what is to be compared within an instance
  replication columns are factors that are treated as replications
  value_column contains values of what is being compared
"""

import numpy as np
import pandas as pd


# DataFrame columns
SSB = "ssb"  # sum of squares


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
        # Calculate statistics
        self.levels = list(self.dfg.indices.keys())
        self.count_ser = pd.Series(self.dfg.count())
        self.mean_ser = pd.Series(self.dfg.mean())
        self.std_ser = pd.Series(self.dfg.std())
        self.fstat = self.calcFstat()

    def _calcFstat(self)
        """
        Calculates the Fstatistic

        Returns
        -------
        """
        
 
