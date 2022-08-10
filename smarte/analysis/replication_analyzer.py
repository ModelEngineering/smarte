"""Analyzes an iteration across all models."""

import smarte.constants as cn

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import SBMLModel as mdl


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

    def plotOneTime(self, manager=None, xaxis=cn.SD_NUM_SPECIES,
        is_plot=True,  is_nfev=True, is_tot_time=True, **kwargs):
        """
        Plots the model calculation times.

        Parameters
        ----------
        xaxis: str (variable on the x-axis)
        manager: OptionManager
        is_nfev: bool (plot number of function evaluations)
        is_tot_time: bool (plot total time)
        kwargs: dict (plot options)

        Returns
        ------
        OptionManager
        """
        if manager is None:
            manager = mdl.OptionManager(kwargs)
        manager.plot_opts.set(mdl.cn.O_XLABEL, default=xaxis)
        ax = manager.plot_opts.get(mdl.cn.O_AX)
        if is_nfev:
            ax1 = ax
            if ax1 is None:
                _, ax1 = plt.subplots()
            # Number of species
            ax1.scatter(self.df[xaxis], self.df[cn.SD_CNT], color='g')
            ax1.set_ylabel('function evaluations', color='g')
            ax1.set_xlabel(xaxis)
            manager.doPlotOpts()
        if is_nfev and is_tot_time:
            ax2 = ax1.twinx()
        elif is_tot_time:
            ax2 = ax
        if is_tot_time:
            ax2.scatter(self.df[xaxis], self.df[cn.SD_TOT_TIME], color='b')
            ax2.set_ylabel('total time (sec)', color='b')
            ax2.set_xlabel(xaxis)
        #
        manager.doPlotOpts()
        if is_plot:
            manager.doFigOpts()
        return manager

    def plotOneEstimationError(self, manager=None, xaxis=cn.SD_NUM_SPECIES,
        is_plot=True,  is_min=True, is_avg=True, is_max=True, **kwargs):
        """
        Plots the model estimation accuracties.

        Parameters
        ----------
        xaxis: str (variable on the x-axis)
        manager: OptionManager
        is_min: bool (plot the min estimation error)
        is_avg: bool (plot the avg estimation error)
        is_max: bool (plot the max estimation error)
        kwargs: dict (plot options)

        Returns
        ------
        OptionManager
        """
        if manager is None:
            manager = mdl.OptionManager(kwargs)
        manager.plot_opts.set(mdl.cn.O_XLABEL, default=xaxis)
        ax = manager.plot_opts.get(mdl.cn.O_AX)
        if ax is None:
            _, ax = plt.subplots()
        if is_min:
            # Number of species
            ax.scatter(self.df[xaxis], self.df[cn.SD_MIN_ERR], color='g')
        if is_avg:
            ax.scatter(self.df[xaxis], self.df[cn.SD_AVG_ERR], color='b')
        if is_max:
            ax.scatter(self.df[xaxis], self.df[cn.SD_MAX_ERR], color='purple')
        ax.set_ylabel('estimation error (log2 estimated/actual)')
        ax.set_xlabel(xaxis)
        #
        legend_spec = mdl.cn.LegendSpec(["min", "avg", "max"])
        manager.plot_opts.set(mdl.cn.O_LEGEND_SPEC, default=legend_spec)
        manager.doPlotOpts()
        if is_plot:
            manager.doFigOpts()
        return manager

    def plotManyTimes(self, is_plot=True, **kwargs):
        """
        Plots the model time results.

        Parameters
        ----------
        kwargs: dict (plot options)
        """
        fig = plt.figure(constrained_layout=True)
        gs = fig.add_gridspec(2, 4)
        ax1 = fig.add_subplot(gs[0, 0:2])
        ax2 = fig.add_subplot(gs[0, 2:4])
        ax3 = fig.add_subplot(gs[1, 0:2])
        ax4a = fig.add_subplot(gs[1, 2])
        ax4b = fig.add_subplot(gs[1, 3])
        mgr = self.plotOneTime(xaxis=cn.SD_NUM_SPECIES, ax=ax1, is_plot=False,
             **kwargs) 
        _ = self.plotOneTime(xaxis=cn.SD_NUM_REACTION, ax=ax2,
             is_plot=False, **kwargs) 
        _ = self.plotOneTime(xaxis=cn.SD_NUM_PARAMETER, ax=ax3,
              is_plot=False, **kwargs)
        # Histograms
        ax4a.hist(self.df[cn.SD_TOT_TIME], bins=100, density=True,
              histtype='step', cumulative=1,)
        ax4a.set_xlabel("total time (sec)")
        ax4b.hist(self.df[cn.SD_CNT], bins=100, density=True,
              histtype='step', cumulative=1,)
        ax4b.set_xlabel("function evalutions")
        mgr.doFigOpts()

    def plotManyEstimationError(self, is_plot=True, **kwargs):
        """
        Plots the model time results.

        Parameters
        ----------
        kwargs: dict (plot options)
        """
        fig = plt.figure(constrained_layout=True)
        gs = fig.add_gridspec(2, 6)
        ax1 = fig.add_subplot(gs[0, 0:3])
        ax2 = fig.add_subplot(gs[0, 3:6])
        ax3 = fig.add_subplot(gs[1, 0:3])
        ax4a = fig.add_subplot(gs[1, 3])
        ax4b = fig.add_subplot(gs[1, 4])
        ax4c = fig.add_subplot(gs[1, 5])
        mgr = self.plotOneEstimationError(xaxis=cn.SD_NUM_SPECIES, ax=ax1, is_plot=False,
             **kwargs) 
        _ = self.plotOneEstimationError(xaxis=cn.SD_NUM_REACTION, ax=ax2,
             is_plot=False, **kwargs) 
        _ = self.plotOneEstimationError(xaxis=cn.SD_NUM_PARAMETER, ax=ax3,
              is_plot=False, **kwargs)
        # Histograms
        ax4a.hist(self.df[cn.SD_MIN_ERR], bins=100, density=True,
              histtype='step', cumulative=1,)
        ax4a.set_xlabel("min error")
        ax4b.hist(self.df[cn.SD_AVG_ERR], bins=100, density=True,
              histtype='step', cumulative=1,)
        ax4b.set_xlabel("avg error")
        ax4c.hist(self.df[cn.SD_MAX_ERR], bins=100, density=True,
              histtype='step', cumulative=1,)
        ax4c.set_xlabel("max error")
        mgr.doFigOpts()
   
        mgr.doFigOpts()
   
