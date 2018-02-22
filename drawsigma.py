#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4

import readtle
from readtle import *

# from tkinter import *
# from tkinter.filedialog import *

from matplotlib.pyplot import plot
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import numpy as np

#from pylab import *


def draw1():
    '''  Создание графиков на коротких отрезках
    '''

    global catalog

    sig = []
    for numsat in range(0, len(catalog.line1) - 1):
        # формирование массива данных рассчётов

        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat1 = twoline2rv(line1, line2, wgs72)

        line1 = catalog.line1[numsat + 1]
        line2 = catalog.line2[numsat + 1]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat + 1] - catalog.JD[numsat]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        sig.append((x2[0] - x1[0]))

    plot(sig, 'c--')
    plot(sig, 'rx')

    show()


def draw2():
    ''' Создание графиков "длинных" отрезков
    '''

    global catalog

    sig = []

    line1 = catalog.line1[0]
    line2 = catalog.line2[0]
    sat0 = twoline2rv(line1, line2, wgs72)

    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[0]) * 24 * 60

        x0, v0 = sgp4(sat0, dT)
        x2, v2 = sgp4(sat2, 0)

        sig.append((x2[0] - x0[0]))

    plot(sig, 'c--')
    plot(sig, 'rx')

    show()


def main():
    openfile()
    draw1()
    draw2()


if __name__ == "__main__":
    main()
