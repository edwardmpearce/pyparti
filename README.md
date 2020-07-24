# PyParti: **Py**thon for **Parti**tions

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edwardmpearce/pyparti/master)

![Test Status](https://github.com/empearce/pyparti/workflows/tests/badge.svg?branch=master)
[![Coverage Status](https://codecov.io/github/empearce/pyparti/coverage.svg?branch=master)](https://codecov.io/gh/empearce/pyparti)

PyParti (**Py**thon for **Parti**tions) is a tool based on Python (3.6+) and 
computational mathematics software [SageMath](https://www.sagemath.org/) (9.0+)
to experiment with [integer partitions](https://en.wikipedia.org/wiki/Partition_(number_theory)), 
[Young diagrams](https://en.wikipedia.org/wiki/Young_tableau#Diagrams), 
and related concepts in [combinatorics](https://en.wikipedia.org/wiki/Combinatorics).
This repository contains:
1. Jupyter/SageMath notebooks for experimenting with partitions and generating functions 
  - [`sage-partitions.ipynb`](https://github.com/edwardmpearce/pyparti/blob/master/sage-partitions.ipynb)
  - [`generating-functions.ipynb`](https://github.com/edwardmpearce/pyparti/blob/master/generating-functions.ipynb)
2. Python/SageMath source code and unit tests to extend the existing `Partition` class with functionality relating to generalised core partitions
  - [`abacus_extension.py`](https://github.com/edwardmpearce/pyparti/blob/master/abacus_extension.py)
  - [`tests.py`](https://github.com/edwardmpearce/pyparti/blob/master/tests.py)
  - [`PartitionExt-demo.ipynb`](https://github.com/edwardmpearce/pyparti/blob/master/PartitionExt-demo.ipynb)
3. Python code/programs to produce LaTeX files which compile to publication-quality labelled diagrams of partitions for educational/research purposes.
  - [`py2tikz.py`](https://github.com/edwardmpearce/pyparti/blob/master/py2tikz.py)
  - [`py2tikz-demo.ipynb`](https://github.com/edwardmpearce/pyparti/blob/master/py2tikz-demo.ipynb)
  - See [this repository](https://github.com/edwardmpearce/tikzpictures) for tools to compile TikZ diagram instructions directly to .png files for portability.

## Installation

Many of the enclosed programs depend on a combination of SageMath and pure Python, and the SageMath distribution contains a Python distribution.
You can use SageMath for computational mathematics in two main ways:
1. Install a copy of the SageMath distribution locally to your machine from https://www.sagemath.org/
2. Create a project in the cloud on [CoCalc](https://doc.cocalc.com/) to run the programs

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

