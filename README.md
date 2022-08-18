# SMART ESTIMATION OF PARAMETERS IN REACTION NETWORKS (SMARTE)

# Concepts

* A **factor** is something that is changed in an experiment, such as start concentration of a species and algorithm for parameter estimation.
* A **level** for a factor is a value that is assigned the factor for an experiment.
* **Factor space** has dimensions of factors, and the coordinates for a factor are its levels.
* A **condition** is a collection of pairs factor and level.
* A **work unit** is a collection of conditions. Typically, conditions are chosen as a hypercube in factor space.

# Repository Structure
* `docs` - sphinx documentation
* `tools` - standalone scripts
* `smarte` - project code

# Developer notes
* Use python3.9 (since there's a Tellurium problem with 3.10)
* Some i[configuration may be required to use Jupyter](https://stackoverflow.com/questions/67679019/jupyter-lab-not-opening-on-ubuntu).
* To get plots, ``sudo apt install python3.9-tk``
* `git clone --recurse-submodules https://github.com/ModelEngineering/smarte.git
* To get tkinter, ``sudo apt-get install python3.6-tk``.

# Versions
