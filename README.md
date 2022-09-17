# SMART ESTIMATION OF PARAMETERS IN REACTION NETWORKS (SMARTE)

# Core Concepts

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
* You should clone the following projects and include them in PYTHONPATH
  *`git clone https://github.com/ModelEngineering/fitterpp.git
  * git clone https://github.com/ModelEngineering/SBMLModel.git
* To get tkinter, ``sudo apt-get install python3.6-tk``.
* Issues with Tellurium make it so that python 3.6 or 3.7 are required. Proceed as follows on macos
  * install homebrew: ``/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"``
  * Use homebrew to install pyenv (manages versions of python): ``brew updae; brew install pyenv``
  * ``pyenv install 3.7.10``
  * make 3.7.10 the default pyenv version: ``pyenv global 3.7.10``
  * creae the virtual environment: ``pyenv exec python -m venv smt``
  * ``source smt/bin/activate``
  * ``pip install --upgrade pip``  # upgrade the version of pip
  * ``pip install -r requirements.txt``

# Versions
