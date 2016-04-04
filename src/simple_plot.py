#!/usr/bin/env python3

"""
Usage: simple_plot.py [OPTIONS] DATAFILE

  Read two columns of data from DATAFILE and plot.

Options:
  --columns INTEGER...     Two columns of the data file to plot.
  --del-header INTEGER     Number of header lines to delete.
  --labels <TEXT TEXT>...  Labels of X and Y axes.
  --xlim <FLOAT FLOAT>...  Limit of X axis.
  --ylim <FLOAT FLOAT>...  Limit of Y axis.
  --title TEXT             Title of the figure.
  --figname TEXT           Name of the figure to save (default: simple_plot).
  --figtype TEXT           Format of the figure to save (default: eps).
  --sci                    Apply scientific notation to the axes.
  --equal                  Same aspect for X and Y axes.
  --show                   Show the figure.

Examples:
  $ ./simple_plot.py twobody_output.dat --show --columns 2 3 --equal \
    --del-header 1 --title 'Orbit Trace' --figname 'orbit_trace'
"""

from matplotlib import rc
import numpy as np
import matplotlib.pyplot as pl
# import click
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l','--columns',dest='columns', nargs=2, type=int, default=[0, 1],
              help='Two columns of the data file to plot.')
parser.add_argument('--del-header',dest='del_header', type=int,  default=0,
              help='Number of header lines to delete.')
parser.add_argument('-i','--step',dest='step', type=int, default=1,
              help='Length of step of walking through indices')
parser.add_argument('-lbs','--labels', dest='labels', nargs=2, default=('$x$', '$y$'),
              help='Labels of X and Y axes.')
parser.add_argument('--xlim',dest='xlim', nargs=2, type=float, default=[0, 0],
              help='Limit of X axis.')
parser.add_argument('--ylim',dest='ylim', nargs=2, type=float, default=[0, 0],
              help='Limit of Y axis.')
parser.add_argument('-n','--title',dest='title', default='', help='Title of the figure.')
parser.add_argument('-o','--figname',dest='figname', default='simple_plot',
              help='Name of the figure to save (default: simple_plot).')
parser.add_argument('-ft','--figtype',dest='figtype', default='pdf',
              help='Format of the figure to save (default: pdf).')
parser.add_argument('--sci',dest='sci', action="store_true",
              help='Apply scientific notation to the axes.')
parser.add_argument('--equal',dest='equal', action="store_true",
              help='Same aspect for X and Y axes.')
parser.add_argument('-s','--show',dest='show', action="store_true",
              help='Show the figure.')
parser.add_argument('-b','--binary',dest='binary', action="store_true",
              help='Whether use binary data file')
parser.add_argument('-dt','--datatype',dest='datatype',choices=['float','double','longdouble'], default='longdouble',
              help='Type of Binary data')
parser.add_argument('-c','--count',dest='count', type=int, default=2,
              help="Dimension of for each 'line' of binary data")
parser.add_argument('datafile',
        help='Input data filename')
args = parser.parse_args()
# TODO: Using globals().update is problematic, while remembering to write *args* **everytime** when using a cmd line argument is SO tedious. What's the best solution?
globals().update(vars(args))

# TODO: Seperate these two processes:
# - Reading data from file
# - Extracting desired columns from data

def read_two_col(filename, col0, col1, header,it):
    """Read two columns of data in a file"""
    f = open(filename, 'r')
    if header > 0:
        for i in range(header):
            f.readline()
    x = []
    y = []
    for line in f:
        line = line.strip()
        columns = line.split()
        x.append(np.longdouble(columns[col0]))
        y.append(np.longdouble(columns[col1]))
    f.close()
    return x, y


def read_two_col_bin(filename, col0, col1, header, it, dt, dc):
    if dt=="float":
        ndt = np.single
    elif dt=="double":
        ndt = np.double
    elif dt=="longdouble":
        ndt = np.longdouble
    data = np.fromfile(filename, dtype=ndt)
    data = data.reshape(data.size/dc,dc)
    x = data[::it,col0]
    y = data[::it,col1]
    return x, y

# def plot_fig(datafile, columns, del_header, binary, datatype, count, labels, xlim, ylim,
#              title, figname, sci, equal, show, figtype):
def plot_fig():
    """Read two columns of data from DATAFILE and plot."""
    rc('text', usetex=True)
    if not binary:
        x, y = read_two_col(datafile, columns[0], columns[1], del_header, step)
    else:
        x, y = read_two_col_bin(datafile, columns[0], columns[1], del_header, step, datatype, count)
    pl.rc('font', family='serif')
    pl.figure(figsize=(8, 6))
    pl.plot(x, y, marker='.', markersize=2.0, color='r',
            linestyle='None')
    pl.xlabel(labels[0], fontsize=16)
    pl.ylabel(labels[1], fontsize=16)
    if not (xlim[0] == xlim[1]):
        pl.xlim(xlim)
    if not (ylim[0] == ylim[1]):
        pl.ylim(ylim)
    if sci:
        pl.ticklabel_format(style='sci', scilimits=(0, 0))
    if equal:
        pl.axis('equal')
    if len(title) > 0:
        pl.title(title, fontsize=16)
    fig_name = figname + '.' + figtype
    pl.savefig(fig_name)
    if show:
        pl.show()


if __name__ == '__main__':
    plot_fig()
