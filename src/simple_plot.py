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

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--columns', dest='columns', nargs=2, type=int, default=[0, 1],
                    help='Two columns of the data file to plot.')
parser.add_argument('--del-header', dest='del_header', type=int, default=0,
                    help='Number of header lines to delete.')
parser.add_argument('-i', '--step', dest='step', type=int, default=1,
                    help='Length of step of walking through indices')
parser.add_argument('-p', '--slice', dest='slc', nargs=2, type=int, default=(None, None),
                    help='begin and end of line')
parser.add_argument('-lbs', '--labels', dest='labels', nargs=2, default=('$x$', '$y$'),
                    help='Labels of X and Y axes.')
parser.add_argument('--xlim', dest='xlim', nargs=2, type=float, default=[0, 0],
                    help='Limit of X axis.')
parser.add_argument('--ylim', dest='ylim', nargs=2, type=float, default=[0, 0],
                    help='Limit of Y axis.')
parser.add_argument('-n', '--title', dest='title', default='', help='Title of the figure.')
parser.add_argument('-o', '--figname', dest='figname', default='simple_plot',
                    help='Name of the figure to save (default: simple_plot).')
parser.add_argument('-ft', '--figtype', dest='figtype', default='pdf',
                    help='Format of the figure to save (default: pdf).')
parser.add_argument('--sci', dest='sci', action="store_true",
                    help='Apply scientific notation to the axes.')
parser.add_argument('--equal', dest='equal', action="store_true",
                    help='Same aspect for X and Y axes.')
parser.add_argument('-s', '--show', dest='show', action="store_true",
                    help='Show the figure.')
parser.add_argument('-b', '--binary', dest='binary', action="store_true",
                    help='Whether use binary data file')
parser.add_argument('-dt', '--datatype', dest='datatype', choices=['float', 'double', 'longdouble'],
                    default='longdouble',
                    help='Type of Binary data')
parser.add_argument('-c', '--count', dest='count', type=int, default=2,
                    help="Dimension of for each 'line' of binary data")
parser.add_argument('--datafile', dest='datafile', default='data.txt',
                    help='Input data filename')
args = parser.parse_args()


def read_data(filename, header=None):
    return np.loadtxt(filename, dtype=np.longdouble, skiprows=header)


def read_data_bin(filename, dc, header=None, dt='longdouble'):
    ndt = np.longdouble
    if dt == "float":
        ndt = np.single
    elif dt == "double":
        ndt = np.double
    elif dt == "longdouble":
        ndt = np.longdouble
    data = np.fromfile(filename, dtype=np.longdouble)
    return data.reshape(data.size // dc, dc)


def read_two_col(data, col0, col1, begin=0, end=None, it=1):
    x = data[begin:end:it, col0]
    y = data[begin:end:it, col1]
    return x, y


def get_cols(datafile, columns=(0,1), del_header=0, begin=0, end=None, step=1,
             binary=True, datatype='longdouble', count=2):
    if not binary:
        data = read_data(datafile, header=del_header)
    else:
        data = read_data_bin(datafile, dc=count, header=del_header, dt=datatype)
    return read_two_col(data, columns[0], columns[1], begin=begin, end=end, it=step)


# TODO: Making plot style more easily configurable
def plot_fig(x, y,
             labels=('$x$', '$y$'), xlim=(0, 0), ylim=(0, 0), title='Figure', sci=True, equal=True, show=False,
             figname='data.txt', figtype='png'):
    """Read two columns of data from DATAFILE and plot."""
    rc('text', usetex=True)
    pl.rc('font', family='serif')
    fig = pl.figure(figsize=(8, 6))
    pl.plot(x, y, marker='.', markersize=1.0, color='r',
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
    x, y = get_cols(datafile=args.datafile, columns=args.columns, del_header=args.del_header,
            begin=args.slc[0], end=args.slc[1], step=args.step,
            binary=args.binary, datatype=args.datatype, count=args.count)
    plot_fig(x, y,
            labels=args.labels, xlim=args.xlim, ylim=args.ylim, title=args.title, sci=args.sci, equal=args.equal,
            show=args.show,
            figname=args.figname, figtype=args.figtype)
