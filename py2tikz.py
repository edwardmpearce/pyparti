#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains string manipulation functions and programs for producing TikZ code, primarily for depicting partitions as Young tableau and Ferrers diagrams, including directly producing .tex files and compiling straight to images.

Producing LaTeX files which compile to publication-quality labelled diagrams of partitions is useful for educational/research purposes,
but writing the code for these by hand can be a labour-intensive task, especially as the partition size increases (where more general behaviour may be observed). 
This module is designed to automate much of this process, making it easy to produce high-quality Young diagrams, with the flexibility to
use Python syntax to iterate the labelling of cells, allowing patterns of interest to be explored.
Partitions can be drawn in a number of different orientations depending on your preferred convention or to emphasise a different pedagogical viewpoint, including 'English', 'French', 'Russian', and 'Cartesian' notations.
    
This module includes the following functions, each returning a string containing TikZ commands for drawing diagrams:
    * tikzline(x1, y1, x2, y2, modifier="") - Draw a line from (x1,y1) to (x2,y2), with optional `modifier` string to set draw style
    * tikznode(x, y, text, modifier="") - Draw a node containing the text at (x,y), with optional `modifier` string to set draw style
    * partition2tikz(p, x0=0, y0=0, notation='English', label_parts=False) - Draw the Young diagram of a partition `p`
    * label_cell(i, j, text, notation='English') - Draw a node containing the text at cell (i,j) in a Young diagram. Indices are 0-based.
    * label_diagram(p, label_function, notation='English') - Label cells (i,j) in Young diagram of `p` according to `label_function(p,i,j)`
    * tikz_ferrers(p, notation = 'English') - Draw the Ferrers diagram of a partition `p`
    * frobenius2tikz(coords, x0=0, y0=0, notation='English', label_parts=False) - Draw annotated Young diagram from Frobenius coordinates
    * label_boundary(seq, col1='blue', col2='orange', notation='English') - Label and colour partition boundary according to a 0-1 sequence
    * writetikz2tex(tikztext, filename) - Write TikZ diagram code to a standalone .tex file
"""


__author__ = 'Edward Pearce'
__copyright__ = 'Copyright 2020, PyParti (Py2TikZ)'
__credits__ = ['Edward Pearce']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Edward Pearce'
__email__ = 'empearce1@sheffield.ac.uk'
__status__ = 'Development'


def tikzline(x1, y1, x2, y2, modifier=""):
    """
    Return string for TikZ command to draw a line from (x1,y1) to (x2,y2), with optional `modifier` string to set draw style.
    """
    return f"\\draw{modifier} ({x1},{y1}) -- ({x2},{y2});" if not ((x1 == x2) and (y1 == y2)) else ""


def tikznode(x, y, text, modifier=""):
    """
    Return string for TikZ command to draw a node containing the text at (x,y), with optional `modifier` string to set draw style.
    """
    return f"\\draw ({x}, {y}) {modifier} node{{{text}}};" if not (text == "") else ""


def label_cell(i, j, text, notation='English'):
    """
    Return string for TikZ command to draw a node containing the text at cell (i,j) in a Young diagram. Indices are 0-based.
    """
    if notation == 'English':
        return tikznode(j + 0.5, -i - 0.5, text)
    elif notation == 'French':
        return tikznode(j + 0.5, i + 0.5, text)        
    elif notation == 'Cartesian':
        return tikznode(i + 0.5, j + 0.5, text)        
    elif notation == 'Russian':
        return tikznode(i - j, i + j + 1, text)
    else:
        print(f"{notation} is not a recognised notation. Choose from 'English', 'French', 'Russian', and 'Cartesian'.")
        return ""
    
        
def partition2tikz(p, x0=0, y0=0, notation='English', label_parts=False):
    r"""
    Return string for a TikZ command to draw the Young diagram of a partition p.
    
    Parameters
    ----------
    p : instance of SageMath `Partition` class
        The partition we want to represent using a Young diagram.
    xshift, yshift : float, optional
        Shift the origin from default (0,0) to (x0, y0).   
    notation : str, optional
        Use the optional parameter `notation` to select the drawing convention 
        from 'English', 'French', 'Russian', and 'Cartesian'. Defaults to 'English'.
    label_parts : Boolean, optional
        If true, labels each row/column corresponding to a part with its size. Defaults to False. 
    
    Returns
    -------
    str
        A string of Tikz draw commands which draw the Young diagram 
        for the input partition p when copied into a tikzpicture.
    """
    if notation == 'English':
        output = tikzline(x0, y0, x0 + p[0], y0)
        for index, item in enumerate(p, 1 - y0):
            output += tikzline(x0, -index, x0 + item, -index)
            if label_parts:
                output += tikznode(x0 - 0.5, 0.5 - index, item)
        output += tikzline(x0, y0, x0, y0 - len(p))            
        for index, item in enumerate(p.conjugate(), x0 + 1):
            output += tikzline(index, y0, index, y0 - item)
    elif notation == 'French':
        output = tikzline(x0, y0, x0 + p[0], y0)
        for index, item in enumerate(p, y0 + 1):
            output += tikzline(x0, index, x0 + item, index)
            if label_parts:
                output += tikznode(x0 - 0.5, index - 0.5, item)
        output += tikzline(x0, y0, x0, y0 + len(p))
        for index, item in enumerate(p.conjugate(), x0 + 1):
            output += tikzline(index, y0, index, y0 + item)
    elif notation == 'Cartesian':
        output = tikzline(x0, y0, x0, y0 + p[0])
        for index, item in enumerate(p, x0 + 1):
            output += tikzline(index, y0, index, y0 + item)
            if label_parts:
                output += tikznode(index - 0.5, y0 - 0.5, item)
        output += tikzline(x0, y0, x0 + len(p), y0)
        for index, item in enumerate(p.conjugate(), y0 + 1):
            output += tikzline(x0, index, x0 + item, index)
    elif notation == 'Russian':
        output = tikzline(x0, y0, x0 - p[0], y0 + p[0])
        for i, part in enumerate(p, 1):
            output += tikzline(x0 + i, y0 + i, x0 + i - part, y0 + i + part)
            if label_parts:
                output += tikznode(x0 + i, y0 - 1 + i, part)
        output += tikzline(x0, y0, x0 + len(p), y0 + len(p))
        for i, part in enumerate(p.conjugate(), 1):
            output += tikzline(x0 - i, y0 + i, x0 - i + part , y0 + i + part)
    else:
        print(f"{notation} is not a recognised notation. Choose from 'English', 'French', 'Russian', and 'Cartesian'.")
        return ""
    return output


def label_diagram(p, label_function, notation='English'):
    r"""
    Return string for TikZ command to label the cells (i,j) of Young diagram of p according to `label_function(p,i,j)`.
        
    Parameters
    ----------
    p : instance of SageMath `Partition` class
        The partition whose Young diagram we wish to annotate with cell labels
    label_function : function (Partition p, int i, int j) -> str
        A function depending on the partition p from cell coordinates (i,j) to the desired label string for that cell
    notation : str, optional
        Use the optional parameter `notation` to select the drawing convention 
        from 'English', 'French', 'Russian', and 'Cartesian'. Defaults to 'English'.
    
    Returns
    -------
    str
        A string of Tikz draw commands which label the cells (i,j) of the Young diagram 
        for the input partition p by the function `label_function(p,i,j)` when copied into a tikzpicture.
    """
    if notation not in ['English', 'French', 'Russian', 'Cartesian']:
        print(f"{notation} is not a recognised notation. Choose from 'English', 'French', 'Russian', and 'Cartesian'.")
        return ""
    output = ""
    for c in p.cells():
        output += label_cell(c[0], c[1], label_function(p, c[0], c[1]))
    return output
        

def tikz_ferrers(p, notation='English'):
    r"""
    Return string for a TikZ command to draw the Ferrers diagram of a partition `p`, with optional `notation` parameter 
    to select the drawing convention from 'English', 'French', 'Russian', and 'Cartesian'. Defaults to 'English'.
    """
    output = ""
    for i, part in enumerate(p):
        for j in range(part):
            if notation == 'English':
                output += "\\filldraw ({1},{0}) circle (.2);".format(-i, j)
            elif notation == 'French':
                output += "\\filldraw ({1},{0}) circle (.2);".format(i, j)
            elif notation == 'Cartesian':
                output += "\\filldraw ({0},{1}) circle (.2);".format(i, j)
            else:
                print(f"{notation} is not a recognised notation. Choose from 'English', 'French', 'Russian', and 'Cartesian'.")
                return output
    return output


def frobenius2tikz(coords, x0=0, y0=0, notation='English', label_parts=False):
    r"""
    Return TikZ command to draw diagram explaining Frobenius coordinates of a partition.
    
    Parameters
    ----------
    coords : 2-tuple of lists of the same length
        The Frobenius coordinates of the partition we want to illustrate.
    xshift, yshift : float, optional
        Shift the origin from default (0,0) to (x0, y0).   
    notation : str, optional
        Use the optional parameter `notation` to select the drawing convention 
        from 'English', 'French', 'Russian', and 'Cartesian'. Defaults to 'English'.
    label_parts : Boolean, optional. Defaults to False. 
        If true, labels each arm/leg of a cell on the diagonal with its size (i.e. the Frobenius coordinates).
    
    Returns
    -------
    str
        A string of Tikz draw commands which draw a diagram relating the Frobenius coordinates
        of a partition with its Young diagram when copied into a tikzpicture.
    """
    p, q = coords
    if notation == 'English':
        output = tikzline(x0, y0, x0 + p[0] + 1, y0)
        output += tikzline(x0, y0, x0, y0 - q[0] - 1)
        for index, item in enumerate(zip(p,q), 1):
            output += tikzline(x0 + index + item[0], y0 - index + 1, x0 + index + item[0], y0 - index)
            output += tikzline(x0 + index - 1, y0 - index, x0 + index + item[0], y0 - index)
            output += tikzline(x0 + index - 1, y0 - index - item[1], x0 + index, y0 - index - item[1])
            output += tikzline(x0 + index, y0 - index + 1, x0 + index, y0 - index - item[1]) 
            if label_parts:
                if item[0] == 0:
                    output += tikznode(x0 + index + 0.5, y0 - index + 0.5, 0)
                else:
                    output += tikznode(x0 + index + 0.5*item[0], y0 - index + 0.5, item[0])
                if item[1] == 0:
                    output += tikznode(x0 + index - 0.5, y0 - index - 0.5, 0)
                else:
                    output += tikznode(x0 + index - 0.5, y0 - index - 0.5*item[1], item[1])
    elif notation == 'French':
        output = tikzline(x0, y0, x0 + p[0] + 1, y0)
        output += tikzline(x0, y0, x0, y0 + q[0] + 1)
        for index, item in enumerate(zip(p,q), 1):
            output += tikzline(x0 + index + item[0], y0 + index - 1, x0 + index + item[0], y0 + index)
            output += tikzline(x0 + index - 1, y0 + index, x0 + index + item[0], y0 + index)
            output += tikzline(x0 + index - 1, y0 + index + item[1], x0 + index, y0 + index + item[1])
            output += tikzline(x0 + index, y0 + index - 1, x0 + index, y0 + index + item[1])
            if label_parts:
                if item[0] == 0:
                    output += tikznode(x0 + index + 0.5, y0 + index - 0.5, 0)
                else:
                    output += tikznode(x0 + index + 0.5*item[0], y0 + index - 0.5, item[0])
                if item[1] == 0:
                    output += tikznode(x0 + index - 0.5, y0 + index + 0.5, 0)
                else:
                    output += tikznode(x0 + index - 0.5, y0 + index + 0.5*item[1], item[1])
    elif notation == 'Cartesian':
        output = tikzline(x0, y0, x0, y0 + p[0] + 1)
        output += tikzline(x0, y0, x0 + q[0] + 1, y0)
        for index, item in enumerate(zip(p,q), 1):
            output += tikzline(x0 + index - 1, y0 + index + item[0], x0 + index, y0 + index + item[0])
            output += tikzline(x0 + index, y0 + index - 1, x0 + index, y0 + index + item[0])
            output += tikzline(x0 + index + item[1], y0 + index - 1, x0 + index + item[1], y0 + index)
            output += tikzline(x0 + index - 1, y0 + index, x0 + index + item[1], y0 + index)
            if label_parts:
                if item[0] == 0:
                    output += tikznode(x0 + index - 0.5, y0 + index + 0.5, 0)
                else:
                    output += tikznode(x0 + index - 0.5, y0 + index + 0.5*item[0], item[0])
                if item[1] == 0:
                    output += tikznode(x0 + index + 0.5, y0 + index - 0.5, 0)
                else:
                    output += tikznode(x0 + index + 0.5*item[1], y0 + index - 0.5, item[1])
    elif notation == 'Russian':
        output = tikzline(x0, y0, x0 - p[0] - 1, y0 + p[0] + 1)
        output += tikzline(x0, y0, x0 + q[0] + 1, y0 + q[0] + 1)
        for index, item in enumerate(zip(p,q), 1):
            output += tikzline(x0 - item[0] - 1, y0 + 2*index + item[0] - 1, x0 - item[0], y0 + 2*index + item[0])
            output += tikzline(x0 + 1, y0 + 2*index - 1, x0 - item[0], y0 + 2*index + item[0])
            output += tikzline(x0 + item[1] + 1, y0 + 2*index + item[1] - 1, x0 + item[1], y0 + 2*index + item[1])
            output += tikzline(x0 - 1, y0 + 2*index - 1, x0 + item[1], y0 + 2*index + item[1])
            if label_parts:
                if item[0] == 0:
                    output += tikznode(x0 - 1, y0 + 2*index, 0)
                else:
                    output += tikznode(x0 - 0.5 - 0.5*item[0], y0 + 2*index + 0.5*item[0] - 0.5, item[0])
                if item[1] == 0:
                    output += tikznode(x0 + 1, y0 + 2*index, 0)
                else:
                    output += tikznode(x0 + 0.5*item[1] + 0.5, y0 + 2*index + 0.5*item[1] - 0.5, item[1])
    return output


def label_boundary(seq, col1='blue', col2='orange', notation='English'):
    r"""
    Return TikZ command to label and colour the boundary of a Young diagram according to a 0-1 sequence,
    based on SageMath's `zero_one_sequence` method for the partition class, which uses English notation 
    with boundary path directions North=0 and East=1, so that part size increases along the boundary path. 
    This leads to reading boundary paths from right to left in Russian and Cartesian notations.
    
    Parameters
    ----------
    seq : a sequence of zeros and ones
        The zero-one sequence of the Young diagram we want to illustrate.
    col1, col2 : str, optional
        Colour name strings used to tell Tikz how to colour the two different kinds of boundary path direction.
    notation : str, optional
        Use the optional parameter `notation` to select the drawing convention 
        from 'English', 'French', 'Russian', and 'Cartesian'. Defaults to 'English'.
    
    Returns
    -------
    str
        A string of Tikz draw commands which draw a coloured boundary path of a Young diagram 
        and labels its edges according to the passed zero-one sequence when copied into a tikzpicture.
    """
    assert set(seq).issubset({0,1}) # Check input is zero-one sequence
    edges, labels = "", ""
    if notation == 'English':
        x, y = 0, sum(seq) - len(seq)
        for code in seq:
            if code == 0:
                edges += tikzline(x, y, x, y+1, modifier=f"[{col2}, ->]")
                labels += tikznode(x, y, code, modifier="[right]")
                y += 1
            elif code == 1:
                edges += tikzline(x, y, x+1, y, modifier=f"[{col1}, ->]")
                labels += tikznode(x, y, code, modifier="[below right]")
                x += 1
    elif notation == 'French':
        x, y = 0, len(seq) - sum(seq)
        for code in seq:
            if code == 0:
                edges += tikzline(x, y, x, y-1, modifier=f"[{col2}, ->]")
                labels += tikznode(x, y, code, modifier="[right]")
                y -= 1
            elif code == 1:
                edges += tikzline(x, y, x+1, y, modifier=f"[{col1}, ->]")
                labels += tikznode(x, y, code, modifier="[above right]")
                x += 1      
    elif notation == 'Cartesian':
        x, y = len(seq) - sum(seq), 0
        for code in seq:
            if code == 0:
                edges += tikzline(x, y, x-1, y, modifier=f"[{col2}, ->]")
                labels += tikznode(x, y, code, modifier="[above]")
                x -= 1
            elif code == 1:
                edges += tikzline(x, y, x, y+1, modifier=f"[{col1}, ->]")
                labels += tikznode(x, y, code, modifier="[above right]")
                y += 1
    elif notation == 'Russian':
        x, y = len(seq) - sum(seq), len(seq) - sum(seq)
        for code in seq:
            if code == 0:
                edges += tikzline(x, y, x-1, y-1, modifier=f"[{col2}, ->]")
                labels += tikznode(x, y, code, modifier="[above left]")
                x -= 1
                y -= 1
            elif code == 1:
                edges += tikzline(x, y, x-1, y+1, modifier=f"[{col1}, ->]")
                labels += tikznode(x, y, code, modifier="[above]")
                x -= 1
                y += 1
    else:
        print(f"{notation} is not a recognised notation. Choose from 'English', 'French', 'Russian', and 'Cartesian'.")
        return ""
    return edges + '\n' + labels


def writetikz2tex(tikztext, filename):
    r"""
    Write TikZ diagram described by `tikztext` to a standalone .tex file with name `<filename>.tex`.
    """
    header = "\\documentclass[tikz]{standalone}\n\\begin{document}\n\\begin{tikzpicture}\n"
    footer = "\n\\end{tikzpicture}\n\\end{document}"
    with open(filename + ".tex", 'w') as f:
        f.write(header + tikztext + footer)
    return True
    
