#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module tests the methods and functions defined in the `abacus_extension.py` module. 
In particular, the methods and constructors of the `PartitionExt` class, such as the implementation of bijections 
between partitions and their generalized core and quotient decompositions, are tested here.

This module includes the following functions related to the constructing partitions from generalised core and quotient data
    * test_from_G_core_and_quotient - Tests the implementation of the bijection between partitions and G-core-quotient decomposition
    * test_from_G_abacus - Tests the bijection between partitions and their minimal G-abacus
    * test_from_G_charges_and_quotient - Tests the bijection between partitions and G-charges-quotient decomposition
    * test_special_core - Tests that $(r,r-1)$-core coincides with $r$-core
    * test_special_quotient - Tests that $(r,r-1)$-quotient coincides with $r$-quotient

The filename and functions of this module follow standard Python test discovery structure
as per https://docs.pytest.org/en/latest/goodpractices.html#test-discovery
@todo: Complete documentation; include test examples in documentation as typical practice in SageMath and doctest frameworks
"""


# Standard library imports

# Third-party imports

# SageMath imports
import sage.all # Required to run this module from a Python interpreter/kernel (not required for Sage kernel)
from sage.combinat.partition import Partition, Partitions
from sage.arith.all import gcd

# Local packages
from abacus_extension import PartitionExt, from_G_core_and_quotient, from_G_charges_and_quotient, from_G_abacus, invert_zero_one


__author__ = 'Edward Pearce'
__copyright__ = 'Copyright 2020, PyParti (Suanpan Project)'
__credits__ = ['Edward Pearce']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Edward Pearce'
__email__ = 'empearce1@sheffield.ac.uk'
__status__ = 'Development'


def test_from_G_core_and_quotient(max_r=15, max_p_size=20):
    r"""
    Tests the implementation of the bijection between partitions and G-core-quotient decomposition.
    Specifically, after specifying a group action by parameters $1 \le b < r$ coprime integers,
    we calculate the $(r,b)$-core $c$ and $(r,b)$-quotient $q$ of a partition $p$ using the `G_core` and `G_quotient` methods,
    then reconstruct a partition from $c$ and $q$ using the `from_G_core_and_quotient` function and check that is equal to $p$.

    Iterates over all partitions of size less than `max_p_size`, 
    all nondegenerate cyclic group actions $frac{1}{r}(1,b)$ where $1 \le b < r$ coprime integers
    for all `r` less than `max_r`.
    """
    for r in range(1, max_r): # Iterate over size of cyclic group
        for b in range(1, r): # Iterate over specific group action
            if gcd(r,b) != 1: # Skip non-coprime pairs (r,b)
                continue
            for n in range(max_p_size): # Iterate over partition sizes
                for p in (PartitionExt(mu) for mu in Partitions(n)): # Iterate over partitions of fixed size
                    # Test bijection between partitions and core-quotient decomposition for given example
                    assert p == from_G_core_and_quotient(p.G_core(r,b), p.G_quotient(r,b), r, b)


def test_from_G_abacus(max_r=15, max_p_size=20):
    r"""
    Tests the implementation of the bijection between partitions and their minimal G-abacus.
    Specifically, after specifying a group action by parameters $1 \le b < r$ coprime integers,
    we calculate the minimal $(r,b)$-abacus of a partition $p$ using the `G_abacus` method,
    then reconstruct a partition from this $(r,b)$-abacus using the `from_G_abacus` function and check that is equal to $p$.

    Iterates over all partitions of size less than `max_p_size`, 
    all nondegenerate cyclic group actions $frac{1}{r}(1,b)$ where $1 \le b < r$ coprime integers
    for all `r` less than `max_r`.
    """
    for r in range(1, max_r): # Iterate over size of cyclic group
        for b in range(1, r): # Iterate over specific group action
            if gcd(r,b) != 1: # Skip non-coprime pairs (r,b)
                continue
            for n in range(max_p_size): # Iterate over partition sizes
                for p in (PartitionExt(mu) for mu in Partitions(n)): # Iterate over partitions of fixed size
                    # Test bijection between partitions and abacus representation for given example
                    assert p == from_G_abacus(p.G_abacus(r,b), r, b)


def test_special_core(max_r=15, max_p_size=20):
    r"""
    Tests that the generalized $(r,b)$-core of a partition coincides with its 'classical' $r$-core
    when $b = r - 1 \equiv -1 (\mathrm{mod}\ r)$ by comparing the `PartitionExt.G_core` method
    with the existing `Partition.core` method.
    Iterates over partitions of size less than `max_p_size`, and moduli `r` less than `max_r`.
    """
    assert all(PartitionExt(p).G_core(r) == p.core(r) for n in range(max_p_size) for p in Partitions(n) for r in range(1,max_r))


def test_special_quotient(max_r=15, max_p_size=20):
    r"""
    Tests that the generalized $(r,b)$-quotient of a partition coincides with its 'classical' $r$-quotient
    when $b = r - 1 \equiv -1 (\mathrm{mod}\ r)$ by comparing the `PartitionExt.G_quotient` method
    with the existing `Partition.quotient` method.
    Iterates over partitions of size less than `max_p_size`, and moduli `r` less than `max_r`.
    
    Due to differences in conventions effectively swapping xy-coordinates for cell colouring (vs. cell content), the order of partitions 
    in the $r$-quotient and $(r,r-1)$-quotient differ by a reflection of indices. We adjust for this before comparison.
    `Partition.content` -> $j - i$, whilst $(r,-1)$-colour -> $i - j (mod r)$ from $(r,b)$-colour -> $i + bj (mod r)$.
    """
    assert all(PartitionExt(p).G_quotient(r, b=-1, label_swap_xy=True) == p.quotient(r) 
               for n in range(max_p_size) for p in Partitions(n) for r in range(1,max_r))

