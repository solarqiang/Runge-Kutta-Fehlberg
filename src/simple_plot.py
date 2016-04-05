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
import matplotlib
# Force matplotlib not to use any X server so as to run on servers without X
matplotlib.use('Agg')
from matplotlib import rc
import numpy as np
import matplotlib.pyplot as pl
# import click
import argparse

# TODO:
# Add input parameters for (begin,end,step)
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
# FIXME:
# Using globals().update is problematic,
# while remembering to write *args* **everytime** when using a cmd line argument is SO tedious.
# What's the best solution?
globals().update(vars(args))

def read_data(filename, header):
    return np.loadtxt(filename, dtype=np.longdouble, skiprows=header)
def read_data_bin(filename, header, dt, dc):
    if dt=="float":
        ndt = np.single
    elif dt=="double":
        ndt = np.double
    elif dt=="longdouble":
        ndt = np.longdouble
    data = np.fromfile(filename, dtype=ndt)
    return data.reshape(data.size//dc,dc)
def read_two_col(data, col0, col1, begin=0, end=None, it=1):
    x = data[begin:end:it,col0]
    y = data[begin:end:it,col1]
    return x, y

# TODO: Making plot style more easily configurable
# def plot_fig(datafile, columns, del_header, binary, datatype, count, labels, xlim, ylim,
#              title, figname, sci, equal, show, figtype):
def plot_fig():
    """Read two columns of data from DATAFILE and plot."""
    rc('text', usetex=True)
    if not binary:
        data = read_data(datafile, del_header)
    else:
        data = read_data_bin(datafile, del_header, datatype, count)
    x, y = read_two_col(data, columns[0], columns[1], step)
    pl.rc('font', family='serif')
    fig=pl.figure(figsize=(8, 6))
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
    pl.close(fig)


if __name__ == '__main__':
    plot_fig()
