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
    
TODO: Complete documentation; include examples in the documentation?
"""


# Standard library imports

# Third-party imports

# SageMath imports
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
    
    Iterates over partitions up to (not including) size `max_p_size`, group size `r` up to (not including) `max_r`.
    There are $\phi(r)$ nondegenerate actions of $\mathbb{Z}_{r}$ on $\mathbb{C}^{2}$.
    """
    print(f"Reconstructing all partitions of size less than {max_p_size} from their G-core-quotient decomposition")
    print(f"For nondegenerate actions of a cyclic group G of size r up to {max_r}")
    test_success = True
    for r in range(1, max_r): # Iterate over size of cyclic group
        r_subtest_pass = True
        for b in range(1, r): # Iterate over specific group action
            if gcd(r,b) != 1: # Skip non-coprime pairs (r,b)
                continue
            for n in range(max_p_size): # Iterate over partition sizes
                for p in [PartitionExt(mu) for mu in Partitions(n)]: # Iterate over partitions of fixed size
                    # Test bijection between partitions and core-quotient decomposition for given example
                    if p == from_G_core_and_quotient(p.G_core(r,b), p.G_quotient(r,b), r, b):
                        pass
                    else: # Test failure case
                        print("Reconstruction of p from core c and quotient q over group action of type (r,b) failed!")
                        print("p = {}, c = {}, q = {}, (r,b) = ({},{})".format(p, p.G_core(r,b), p.G_quotient(r,b), r, b))
                        r_subtest_pass = False
        if r_subtest_pass:
            print(f"Test passed for r = {r}")
        else:
            test_success = False
    return test_success


def test_from_G_abacus(max_r=15, max_p_size=20):
    r"""
    Tests the bijection between partitions and their minimal G-abacus for a range of partition sizes and cyclic G-actions.
    
    Iterates over partitions up to (not including) size `max_p_size`, group size `r` up to (not including) `max_r`.
    There are $\phi(r)$ nondegenerate actions of $\mathbb{Z}_{r}$ on $\mathbb{C}^{2}$.
    """
    print(f"Reconstructing all partitions of size less than {max_p_size} from their minimal G-abacus")
    print(f"For nondegenerate actions of a cyclic group G of size r up to {max_r}")
    test_success = True
    for r in range(1, max_r): # Iterate over size of cyclic group
        r_subtest_pass = True
        for b in range(1, r): # Iterate over specific group action
            if gcd(r,b) != 1: # Skip non-coprime pairs (r,b)
                continue
            for n in range(max_p_size): # Iterate over partition sizes
                for p in [PartitionExt(mu) for mu in Partitions(n)]: # Iterate over partitions of fixed size
                    # Test bijection between partitions and core-quotient decomposition for given example
                    if p == from_G_abacus(p.G_abacus(r,b), r, b):
                        pass
                    else: # Test failure case
                        print("Reconstruction of `p` from (r,b)-abacus `a` based on minimal border path sequence `s` failed!")
                        print("p = {}, s = {}, a = {}, (r,b) = ({},{})".format(p, invert_zero_one(p.zero_one_sequence()), 
                                                                               p.G_abacus(r,b), r, b))
                        r_subtest_pass = False
        if r_subtest_pass:
            print(f"Test passed for r = {r}")
        else:
            test_success = False
    return test_success


def test_special_core(max_r=15, max_p_size=20):
    r"""
    Tests that the 'classical' $r$-core of a partition coincides with the generalized $(r,b)$-core
    in the special case when $b = r - 1 \equiv -1 (\mathrm{mod}\ r)$ by comparing the existing `Partition.core` method
    with the `PartitionExt.G_core` method for a range of partition sizes and values of the modulus $r$.
    
    Iterates over partitions up to (not including) size `max_p_size`, and moduli `r` up to (not including) `max_r`.
    """
    return all(PartitionExt(p).G_core(r) == p.core(r) for n in range(max_p_size) for p in Partitions(n) for r in range(1,max_r))


def test_special_quotient(max_r=15, max_p_size=20):
    r"""
    Tests that the 'classical' $r$-quotient of a partition coincides with the generalized $(r,b)$-quotient
    in the special case when $b = r - 1 \equiv -1 (\mathrm{mod}\ r)$ by comparing the existing `Partition.quotient` method
    with the `PartitionExt.G_quotient` method for a range of partition sizes and values of the modulus $r$.
    
    Iterates over partitions up to (not including) size `max_p_size`, and moduli `r` up to (not including) `max_r`.
    
    Due to differences in conventions effectively swapping xy-coordinates for cell colouring (vs. cell content), the order of partitions 
    in the $r$-quotient and $(r,r-1)$-quotient differ by a reflection of indices. We adjust for this before comparison.
    `Partition.content` -> $j - i$, whilst $(r,-1)$-colour -> $i - j (mod r)$ from $(r,b)$-colour -> $i + bj (mod r)$.
    """
    return all(PartitionExt(p).G_quotient(r, b=-1, label_swap_xy=True) == p.quotient(r) 
               for n in range(max_p_size) for p in Partitions(n) for r in range(1,max_r))


def main():
    test_from_G_core_and_quotient()
    test_from_G_abacus()
    test_special_core()
    test_special_quotient()
    
    
if __name__ == "__main__":
    main()
    
