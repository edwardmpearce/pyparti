#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module defines a class `PartitionExt` which extends the `Partition` class in SageMath with
methods related to the computation of the generalized core and quotient decomposition as described in [Pearce, 2020].
See the docstring of the `PartitionExt` class for a description of the available methods.

This module further includes the following functions related to constructing partitions from generalised core and quotient data
    * from_G_core_and_quotient(core, quotient, r, b=-1) - Create partition from G-core-quotient decomposition w.r.t. $(r,b)$-action
    * from_G_charges_and_quotient(charges, quotient, r, b=-1) - Create partition from $(r,b)$-charge coordinates and quotient
    * from_G_abacus(abacus, r=None, b=-1) - Create partition from a representation of its $(r,b)$-abacus.
"""


# Standard library imports
from collections import deque # deque is list-like container with faster popleft

# SageMath imports
import sage.all # Required to run this module from a Python interpreter/kernel (not required for Sage kernel)
from sage.combinat.partition import Partition, Partitions
from sage.combinat.partition_tuple import PartitionTuple # Used for compatibility with `Partition.quotient` method
from sage.arith.all import gcd

# Local packages


__author__ = 'Edward Pearce'
__copyright__ = 'Copyright 2020, PyParti (Suanpan Project)'
__credits__ = ['Edward Pearce']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Edward Pearce'
__email__ = 'empearce1@sheffield.ac.uk'
__status__ = 'Development'


class PartitionExt(Partition):
    r"""Extends the `Partition` class in SageMath with the following methods:
    
    * G_colour_tableau(self, r, b=-1) - Returns tableau of `self` with cells coloured by $(i,j) \mapsto i + bj \ (\mathrm{mod}\ r)$.
    * G_colour_count(self, r, b=-1) - Counts the number of cells in `self` of each colour under the $(r,b)$-colouring.
    * is_G_core(self, r, b=-1) - Checks whether `self` is a G-core with respect to the $(r,b)$-action
    * G_core(self, r, b=-1) - Returns the G-core partition of `self` with respect to the $(r,b)$-action
    * G_quotient(self, r, b=-1) - Returns the G-quotient of `self` with respect to the $(r,b)$-action, an $r$-tuple of partitions
    * G_abacus(self, r, b=-1) - Returns an $r$-tuple of path sequences {1:N, 0:E} corresponding to `self` and the $(r,b)$-action
    * G_charges(self, r, b=-1) - Returns the charge coordinates of `self` with respect to the $(r,b)$-action, an $r$-tuple of integers
    
    In the default case that only one argument `r` is passed, the action is of type $(r,-1) = (r,r-1)$ which is special linear and 
    yields the same result as the classical `core(r)` and `quotient(r)` methods.
    """
    def __init__(self, mu):
        """
        Initialize `self`.
        """
        assert isinstance(mu, Partition)
        self._list = mu._list
        
        
    __repr__ = Partition._repr_list
    
    
    def G_colour_tableau(self, r, b=-1):
        r"""
        Returns tableau of `self` with cells coloured according to the $(r,b)$-action on monomials over $\mathbb{C}[x,y]$.
        
        Specifically, a cell $(i,j)$ is mapped to colour value $i + bj \ (\mathrm{mod}\ r)$.
        """
        return [[(i + b * j) % r for j in range(self[i])] for i in range(len(self))]
    
    
    def G_colour_count(self, r, b=-1):
        r"""
        Counts the number of cells in `self` of each colour under the $(r,b)$-colouring.
        """
        counts = [0 for _ in range(r)]
        for row in self.G_colour_tableau(r,b):
            for cell_colour in row:
                counts[cell_colour] += 1
        assert sum(counts) == self.size()
        return counts
    
    
    def is_G_core(self, r, b=-1):
        r"""Checks whether `self` is a G-core with respect to the $(r,b)$-action. Returns: Bool
        
        A partition is said to be an $(r,b)$-core if it has no cells satisfying the congruence equation 
        $$\ell(\square) - b(a(\square) + 1) \equiv 0 \ (\mathrm{mod}\ r).$$
        Equivalently, a partition is said to be an $(r,b)$-core if it is its own $(r,b)$-core 
        (where the latter is defined as in `G_core()`).
        """
        return not any(any((cell % r) == 0 for cell in row) for row in self.upper_hook_lengths(-b))
        
        
    def G_abacus(self, r, b=-1, method='fast'):
        r"""
        Converts a partition to a finite representation of its $G$-abacus, where the $G$-action is of type $(r,b)$.
        
        First, a sequence encoding the border path of the partition is calculated, with convention {1:N, 0:E} in English notation
        Next, we separate path segments in the sequence onto $r$ different abacus wires according to their location in the lattice
        $\mathbb{Z}^{2}$ and the lattice colouring defined by the $(r,b)$-action.
        
        Returns: Length $r$ list of path sequences (themselves lists of '0's and '1's)
        Note that every full path sequence starts with infinitely many '1's and ends with infinitely many '0's.
        """
        if method == 'fast': # Reads abacus from minimal zero-one sequence, swapping '0' and '1' to ensure {1:N, 0:E} convention
            seq = invert_zero_one(self.zero_one_sequence())
        elif method == 'slow': # Dyck word is always longer than minimal zero-one sequence, so will take longer to read
            seq = self.to_dyck_word()
        abacus = [deque() for _ in range(r)]    
        wire_num = sum(seq) % r # counts number of '1's modulo r to find the starting wire index
        for code in seq:
            abacus[wire_num].append(code)
            # The next wire to read from depends on the value of the current symbol
            # Add b to the wire index if '0' was read, else subtract 1 if '1' was read, then reduce modulo r
            wire_num = (wire_num + b * (1 - code) - code) % r
        return abacus
    
    
    def G_core(self, r, b=-1):
        r"""
        Calculates the G-core partition of `self` with respect to the $(r,b)$-action, 
        
        First, the G-charge coordinates of `self` are computed via the G-abacus. These are preserved by valid abacus moves.
        Next, we implicitly slide beads on the G-abacus to remove any quotient component whilst preserving charges.
        Finally, the modified abacus is converted back to a partition.
        
        Returns: an instance of the PartitionExt class
        """
        return from_G_charges_and_quotient(self.G_charges(r,b), quotient=None, r=r, b=b)
    
    
    def G_quotient(self, r, b=-1, label_swap_xy=False):
        r"""
        Calculates the G-quotient of `self` with respect to the $(r,b)$-action, 
        
        First, the G-abacus of `self` is computed. Second, the path sequence of each abacus wire is converted back to a partition.
        Note that the abacus uses the convention {1:N, 0:E} in English notation for partition border paths
        
        Due to differences in conventions effectively swapping xy-coordinates for cell colouring (vs. content), the order of partitions 
        in the $(r,r-1)$-quotient ($b=-1$ special case) differs from the classical $r$-quotient by a reflection of indices. 
        This can be accounted for by setting the optional `label_swap_xy` keyword argument to `True`. A cell $(i,j)$ is mapped as
        `Partition.content` -> $j - i$, whilst $(r,-1)$-colour -> $i - j (mod r)$ (as case of $(r,b)$-colour -> $i + bj (mod r)$).
        
        Returns: an $r$-tuple of partitions
        """
        # Sagemath uses the convention {1:E, 0:N} when reading partition from a path sequence, so we have to swap '0's and '1's
        p_list = [Partition(zero_one=invert_zero_one(wire)) for wire in self.G_abacus(r,b)]
        # Reflect the order of partitions in the $b=-1$ case `G_quotient` to account for differences in conventions for cell colouring 
        # for compatibility with `Partition.quotient`.
        if label_swap_xy:
            p_list = [p_list[0]] + p_list[:0:-1]
        # Cast the list of partitions in the quotient as a `PartitionTuple` for compatibility with the `Partition.quotient` method
        return PartitionTuple(p_list)
    
    
    def G_charges(self, r, b=-1):
        r"""
        Calculates the charge coordinates of `self` with respect to the $(r,b)$-action, returning an $r$-tuple of integers.
        
        The charge on each wire of the $(r,b)$-abacus of `self` describes the excess or deficit of electrons ('1' symbols)
        relative to a fixed ground state - the $(r,b)$-abacus of the empty partition (the vacuum). 
        By construction, global charge (i.e. the sum of charge coordinates) is zero.
        """
        abacus = self.G_abacus(r, b)
        total_north_steps = sum(sum(wire) for wire in abacus)
        
        # For reference to a fixed ground state, we calculate the number of north steps ('1' symbols) on each wire that 
        # we would expect if an abacus with the same number of total north steps was generated from the empty partition
        expected = [(total_north_steps // r) + int(0 < i <= (total_north_steps % r)) for i in range(r)]
        assert sum(expected) == total_north_steps
        
        # The charge of a wire on the abacus is defined to be the difference in '1' symbols relative to the reference state
        charges = [expected[i] - sum(wire) for i, wire in enumerate(abacus)]
        
        # As the total number of '1' symbols should be equal in the true and reference abacus, the total excess/defecit is zero
        assert sum(charges) == 0
        return charges


def invert_zero_one(sequence):
    r"""Helper function to swap '0's and '1's in a binary sequence"""
    return [1 - code for code in sequence]


def from_G_core_and_quotient(core, quotient, r, b=-1):
    r"""
    Construct a partition from its generalized core and quotient decomposition with respect to the $(r,b)$-action.
    
    This function checks that the input arguments are valid, in particular that `core` is indeed an $(r,b)$-core partition,
    Then calculates the charge coordinates of `core` to pass to the function `from_G_charges_and_quotient`.
    
    Inputs:
        r, b - Describes G-action. Should have $0 < b < r$ coprime integers, though `b` need only be defined modulo `r`.
                Default value for `b` is $-1 \equiv \ (\mathrm{mod}\ r)$ which describes special linear action.
        core - must be an $(r,b)$-core partition, and must be an instance of PartitionExt
        quotient - an $r$-tuple of Partition instances, or None. If None, returns `core` directly.
    
    Returns: 
        An instance `mu` of PartitionExt such that `mu.G_core(r, b) == core` and `mu.G_quotient(r, b=-1) == quotient`.
    """
    assert isinstance(core, PartitionExt)
    assert core.is_G_core(r, b) # Verifies whether the first argument is a $G$-core with respect to the $(r,b)$-action.
    if quotient is None:
        return core
    else:
        return from_G_charges_and_quotient(core.G_charges(r, b), quotient, r, b)

    
def from_G_charges_and_quotient(charges, quotient, r, b=-1):
    r"""
    Construct a partition from its $(r,b)$-charge coordinates and quotient decomposition.
    
    First, convert the partitions in `quotient` into path sequences to construct a prelimary abacus.
    Next, adjust the abacus according to `charges` to match the associated excess/deficit of '1' symbols in each finite wire segment
    Then pass to the function `from_G_abacus` to flatten and read the path sequence before converting back to a partition.
    
    Inputs:
        r, b - Describes G-action. Should have $0 < b < r$ coprime integers, though `b` need only be defined modulo `r`.
                Default value for `b` is $-1 \equiv \ r-1 (\mathrm{mod}\ r)$ which describes special linear action.
        core - must be an $(r,b)$-core partition, and must be an instance of PartitionExt
        quotient - an $r$-tuple of Partition instances, or None. If None, `quotient` is replaced by an $r$-tuple of empty partitions.
    
    Returns: 
        An instance `mu` of PartitionExt such that `mu.G_core(r, b) == core` and `mu.G_quotient(r, b=-1) == quotient`.
    """
    # Input validation checks
    assert len(charges) == r
    assert sum(charges) == 0
    
    if quotient is None:
        # Initialize an empty abacus
        # Full path sequences start with infinitely many '1's and end with infinitely many '0's, but these are all omitted.
        n = 0
        abacus = [deque() for _ in range(r)]
    else:
        assert len(quotient) == r # Check quotient has correct length
        # Convert partitions in quotient to Dyck words of equal length
        # Each wire begins with 2n symbols: n each of the symbols '0' and '1', describing the path sequence of the partition in `quotient`
        n = max(len(mu.to_dyck_word()) for mu in quotient) // 2
        abacus = [deque(mu.to_dyck_word(n)) for mu in quotient]
    
    # Add a number of excess '1's to the left each wire according to the charge coordinates
    # c_max - charges[i] describes the number of excess 1's on wire i
    # In total, r * c_max many 1's are added since charges sum to zero
    c_max = max(charges)
    for i in range(r):
        abacus[i].extendleft(1 for _ in range(c_max - charges[i]))
    
    # Output validation checks
    assert sum(len(wire) for wire in abacus) == r * (2*n + c_max) # Total number of symbols on whole abacus
    assert sum(sum(wire) for wire in abacus) == r * (n + c_max) # Total number of '1's on whole abacus    
    
    return from_G_abacus(abacus, r, b)
    
    
def from_G_abacus(abacus, r=None, b=-1):
    r"""
    Construct a partition from a representation of its $(r,b)$-abacus. If parameter `r` is not given, can be inferred from `len(abacus)`.
    
    Merges the wires of the abacus back into a single list of '0' and '1' symbols.
    The resulting sequence encodes a partition boundary path by the rule {1:N, 0:E} as for Dyck paths/words.
    After the G_abacus is flattened into a path sequence, the final conversion to a partition.
    
    Returns:
        An instance `mu` of PartitionExt such that `mu.G_abacus(r, b)` is isomorphic to `abacus` (i.e. describe same quotient and charges)
    """
    abacus = [deque(wire) for wire in abacus] # Clean input to cast lists as deque instances to allow use of `popleft` method
    
    if r is None: # Infer `r` from the number of wires in the abacus
        r = len(abacus)
    assert gcd(r,b) == 1 # Check that b is coprime to r to ensure the algorithm will terminate
    
    path_seq = list()
    north_steps_read = 0
    total_north_steps = sum(sum(wire) for wire in abacus)
    wire_num = total_north_steps % r # Starting wire index depends on the total number of '1's in the abacus
    while north_steps_read < total_north_steps: # Loop should terminate after at most r*sum(len(wire) for wire in abacus) steps
        # Read the next symbol from the current wire
        if len(abacus[wire_num]) > 0:
            # return and remove the leftmost item from the wire if not empty, this removes the need to track bead position
            code = abacus[wire_num].popleft()
        else: # To the right of each wire is an infinite sequence of '0's (used when finished reading finite part)
            code = 0
        
        # Add symbol to flattened path sequence
        path_seq.append(code)
        # Increase the number of '1's (north steps) read when appropriate (otherwise adding '0')
        north_steps_read += code
        # The next wire to read from depends on the value of the current symbol
        # Add b to the wire index if '0' was read, else subtract 1 if '1' was read, then reduce ulo r
        wire_num = (wire_num + b*(1 - code) - code) % r
        
    # Sagemath uses the convention {1:E, 0:N} when reading partition from a path sequence, so we have to swap '0's and '1's
    inverted_seq = invert_zero_one(path_seq)
    
    return PartitionExt(Partition(zero_one=inverted_seq))

