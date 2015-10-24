import matplotlib
from matplotlib import pyplot
import numpy

def setup():
    pyplot.style.use('bmh')
    matplotlib.rcParams.update({'savefig.dpi': 100,
                                'savefig.bbox': 'tight',
                                'savefig.transparent' : True,

                                'font.sans-serif': ["Helvetica Neue","Helvetica","Segoe UI","Arial","freesans","sans-serif"],

                                'axes.labelsize' : 12,
                                'xtick.labelsize' : 12,
                                'ytick.labelsize' : 12,
                                'legend.fontsize' : 12,

                                'axes.facecolor' : 'white',

                                'axes.edgecolor' : '#bbbbbb',

                                'grid.color' : "#eeeeee",
                                'grid.linestyle' : "-",
                                'grid.alpha' : 0.5,

                                'axes.labelcolor' : "#333333",
                                'xtick.color' : "#333333",
                                'ytick.color' : "#333333",

                                'svg.fonttype' : 'path',

                                'legend.numpoints' : 1})

def plot_function(f, plot_precision, *args, **kwargs):
    xmin, xmax = pyplot.xlim()
    fx = numpy.arange(xmin, xmax, plot_precision)
    fy = [f(xi) for xi in fx]

    ax = pyplot.gca()
    ax.set_autoscale_on(False)
    return ax.plot(fx, fy, *args, **kwargs)

setup()
