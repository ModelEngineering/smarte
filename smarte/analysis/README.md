# ANALYSIS
This directory contains codes that run and analyze fitting experiments.


An experimental run consists of one or more replications, and each replication
has one or more simulations. A simulation is parameterized by the following factors:
  - Parameter min, max
  - Column deleted
  - Noise_mag: randomness introduced in observational data
  - Maximum number of function evalutions
  - Algorithm
  - Parameter initial value
  - BioModel

A replication contains simulations for multiple algorithms and BioModels, and 
each algorithm for the same BioModel uses the same initial value for each parameter
and the same synthetic observational data for each model.
A replication is contained in a single CSV file.

An experimental run constists of multiple replications, each of which uses a different
initial value and different observational data for each parameter and BioModel.
