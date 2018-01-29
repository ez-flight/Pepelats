from matplotlib.pyplot import *
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import numpy as np
from fewsats import *
from datetime import *

def getQuickChanges(tlefile, _bins=30, _width=50, _height=2.0, _loc=1):
    '''расчитано на то, что в одном файле будет только один спутник, т.к.
    методика для иных случаев не придумана'''
    sats = SatelliteSet(tlefile)
    residuals = sats.getResidual()
    #если в файле будет больше одного спутника, надо вот на это обратить
    # внимание
    name = list(residuals.keys())[0]
    t, dr, dv = residuals[name]
    fig = figure()
    ax = fig.add_subplot(111)
    plot(t, dr, color='red', linewidth=2)
    xlabel(r'$t$')
    ylabel(r'$\Delta R$, км')
    title(name)
    grid(which='major')
    inset_ = inset_axes(ax, width='%d%%' % _width, height=_height, loc=_loc, borderpad=0.5)
    little=10
    hist(dr, _bins, normed=True)
    tick_params(labelsize=little)
    xlabel(r'$\Delta R$, км', fontsize=little)
    ylabel(r'$P\left(\Delta R\right)$', fontsize=little)
    return fig

def getProgressiveChanges(tlefile):
    sats = SatelliteSet(tlefile)
    residuals = sats.getResidual(False)
    name = list(residuals.keys())[0]
    t, dr, dv = residuals[name]
    fig = figure()
    ax = fig.add_subplot(111)
    plot(t, dr, linewidth=2)
    xlabel(r'$t$')
    ylabel(r'$\Delta R$, км')
    title(name)
    grid(which='major')
    return fig

