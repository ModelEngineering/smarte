"""Analyzes errors in parameter estimation."""
import smarte.constants as cn

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FIGSIZE = (10, 10)


class ErrorAnalyzer(object):

    def __init__(self, ser):
        """
        Parameters
        ----------
        ser: pd.Series
            index: instance identifier
            values: error metric in log2 units
            index.name: str (used on x-axis)
            name: str (used on y-axis)
        """
        self.ser = ser.groupby(ser.index).mean()

    def plot(self, is_plot=True, ax=None, title=""):
        """
        Plots values against index.

        Parameters
        ----------
        is_plot: bool
        ax: matplotlib.Axes
        """
        if ax is None:
            fig, ax = plt.subplots(1, figsize=FIGSIZE)
        ax.scatter(self.ser.index, self.ser, marker="*")
        #ax.set_xticks(np.arange(100, max(indices), 100))
        ax.set_xlabel(self.ser.index.name)
        ax.set_ylabel(self.ser.name)
        ax.set_title(title)
        if is_plot:
            plt.show()

    def hist(self, is_plot=True, ax=None, title="", **kwargs):
        """
        Histogram of error values

        Parameters
        ----------
        is_plot: bool
        ax: matplotlib.Axes
        kwargs: dict (optional parameters for plt.hist)
        """
        if ax is None:
            fig, ax = plt.subplots(1, figsize=FIGSIZE)
        ax.hist(self.ser, **kwargs)
        ax.set_xlabel(self.ser.name)
        ax.set_title(title)
        if is_plot:
            plt.show()
