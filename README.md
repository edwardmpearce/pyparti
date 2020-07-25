# PyParti: **Py**thon for **Parti**tions

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master)
![Test Status](https://github.com/edwardmpearce/pyparti/workflows/tests/badge.svg?branch=master)
[![Coverage Status](https://codecov.io/github/edwardmpearce/pyparti/coverage.svg?branch=master)](https://codecov.io/gh/edwardmpearce/pyparti)

PyParti (**Py**thon for **Parti**tions) is a tool based on Python (3.6+) and 
computational mathematics software [SageMath](https://www.sagemath.org/) (9.0+)
to experiment with [integer partitions](https://en.wikipedia.org/wiki/Partition_(number_theory)), 
[Young diagrams](https://en.wikipedia.org/wiki/Young_tableau#Diagrams), 
and related concepts in [combinatorics](https://en.wikipedia.org/wiki/Combinatorics).
This repository contains:
1. Jupyter/SageMath notebooks for experimenting with partitions and generating functions 
  - [`sage-partitions.ipynb`](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master?filepath=sage-partitions.ipynb)
  - [`generating-functions.ipynb`](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master?filepath=generating-functions.ipynb)
2. Python/SageMath source code and unit tests to extend the existing `Partition` class with functionality relating to generalised core partitions
  - [`PartitionExt-demo.ipynb`](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master?filepath=PartitionExt-demo.ipynb)
  - [`abacus_extension.py`](https://github.com/edwardmpearce/pyparti/blob/master/abacus_extension.py)
  - [`test_abacus_extension.py`](https://github.com/edwardmpearce/pyparti/blob/master/test_abacus_extension.py)
3. Python code/programs to produce LaTeX files which compile to publication-quality labelled diagrams of partitions for educational/research purposes.
  - [`py2tikz.py`](https://github.com/edwardmpearce/pyparti/blob/master/py2tikz.py)
  - [`py2tikz-demo.ipynb`](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master?filepath=py2tikz-demo.ipynb)
  - See [this repository](https://github.com/edwardmpearce/tikzpictures) for tools to compile TikZ diagram instructions directly to .png files for portability.

## Getting Started

### Run a preconfigured notebook instance on the cloud using Binder

This repository and individual notebooks can be run online without the need for any local installation and configuration 
by following the links to notebooks above or by clicking on the badge below to launch a Jupyter server accessed in the browser.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master)

This is facilitated by [mybinder.org](https://mybinder.org/), a public instance of the [BinderHub](https://binderhub.readthedocs.io/) service. 
BinderHub allows many users to start Binder sessions: within a session, BinderHub creates a per-session software environment on demand 
on remote hardware (using repo2docker) then starts a Jupyter service within that environment.

As an end user, all you need to start a BinderHub session is
1. The URL of an accessible Git repository that contains a software environment definition 
   (e.g. a Python `requirements.txt` file, Conda `environment.yml` or a Docker `Dockerfile`);
2. The branch, tag or commit that you’d like to access within that repository;
3. (Optional) a relative path within that directory to a Notebook you’d like to run.
These parameters can be supplied via a web form (as at [mybinder.org](https://mybinder.org/)) or as URL parameters 
(allowing someone to just follow a link to start a Binder session).

### Clone the repository to a (cloud-based) CoCalc project

Another way to avoid installing the SageMath distribution dependencies on your local machine is to 
create a project on [CoCalc](https://doc.cocalc.com/) and clone the repository contents there

### Install the SageMath distribution locally

For development purposes, you may wish to install a copy of the SageMath distribution locally to your machine from [sagemath.org](https://www.sagemath.org/).
Multiple download options exist including installers, binaries, compiling from source, Docker containers, and using package managers such as Conda.

## Reporting Issues

If your issue (feature request or bug) has not already been filed in the PyParti GitHub repository ([list of all open issues](https://github.com/DiODeProject/MuMoT/issues))
then please [file a new Issue](https://help.github.com/articles/creating-an-issue) against the [PyParti GitHub repository](https://github.com/edwardmpearce/pyparti).

## Testing

### Automated testing using a GitHub Actions workflow

On each Pull Request or push made to the `master` branch of the [PyParti GitHub repository](https://github.com/edwardmpearce/pyparti)
we trigger a GitHub Actions continuous integration (CI) workflow.

Each invocation of the workflow runs a set of user-defined tasks in an isolated execution environment, 
logs output from those tasks, quits early if an error is encountered and reports the exit status on completion of the job.

The GitHub Actions dashboard for the project shows job exit statuses and logs: https://github.com/edwardmpearce/pyparti/actions

Benefits:
- Tests are run automatically without needing to be manually triggered and the results inspected by developers;
- If pull requests are made from feature branches against the `master` branch then you will be notified that tests fail before you merge any changes into `master`.
- You can concentrate on other things whilst the CI/CD service is running tests on your behalf.

The GitHub Actions CI configuration is in the file [`.github/workflows/test_build.yml`](https://github.com/edwardmpearce/pyparti/blob/master/.github/workflows/test_build.yml). In short, this:
- Spawns a job on a remote machine running a particular operating system (say, the latest version of Ubuntu Linux or MacOS) and version of Python
- Checks out (a.k.a. copies) the repository to the remote machine
- Installs Miniconda to be used as a package management tool
- Uses conda to install the dependencies required for testing, as specified in the [`sage-test-env.yml`](https://github.com/edwardmpearce/pyparti/blob/master/sage-test-env.yml) conda environment file
- Uses `flake8` for code linting, i.e. checking code syntax and style for Python `.py` files in the repository
- Calls `pytest` to search for tests according to [standard Python test discovery](https://docs.pytest.org/en/latest/goodpractices.html#test-discovery)
  procedures, then run them whilst recording code coverage data using `pytest-cov` to produce an `xml` report
  - Informative testing logs should be produced by `pytest` in the case of test failure
- Upload code coverage data (i.e. proportion of the code which is covered by the tests) to CodeCov service (see Coverage badge with link above)

#### Notes on test environment setup
- The `sage` package on conda-forge is only available for Linux and MacOS, but not Windows.
- The `tox` package for further virtual environment and testing configuration was considered, but ultimately not used in the current testing setup.
- The module `sage.all` is imported at the start of Python files relying on SageMath functionality to avoid import errors when using 
  a Python kernel/interpreter, as is the case during the automatic testing workflow. However these import statements are unnecessary when running
  a Sage kernel (for example on CoCalc or in the provided Binder image)
  - Alternative solutions to the SageMath test environment setup problem could include:
    - Move testing functionality into Jupyter notebooks where use of a Sage kernel could be specified in notebook metadata
	- Find a way to run `pytest` from the SageMath shell/interpreter whilst retaining code coverage functionality to fix import issues.
	  - Change file extension to `.sage` and change hashbang `#!` instructions at start of files using `sage` functions and classes
	- Follow the `doctest` framework used by other SageMath modules

## References

### Illustrated explanations of partition combinatorics and SageMath
An introduction to the mathematics of partitions and Young diagrams and relevant existing SageMath functionality
- https://edwardmpearce.github.io/tutorial-partitions/

### Official SageMath documentation
- [Official documentation for `sage.combinat.partition`](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/partition.html#sage-combinat-partition)
- [Source code for `sage.combinat.partition`](https://github.com/sagemath/sage/blob/master/src/sage/combinat/partition.py)
- [Introduction to combinatorics in Sage](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/tutorial.html#partitions-of-integers)

### Producing images from TikZ diagrams
- https://github.com/edwardmpearce/tikzpictures

### Continuous Integration
- [Using Python with GitHub Actions](https://docs.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions)
- [Testing your Python Project with GitHub Actions](https://gist.github.com/mwouts/9842452d020c08faf9e84a3bba38a66f)
- [Example of continuous integration with conda](https://github.com/mwouts/jupytext/blob/master/.github/workflows/continuous-integration-conda.yml)
- [Quickstart continuous integration using predefined workflows](https://medium.com/swlh/automate-python-testing-with-github-actions-7926b5d8a865)
