import math
from math import sqrt


from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4

from readtle import CatalogTLE

from KeplerOrbit import KeplerOrbit

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from calcsigma import *

class ProcessingCatalog:
    def __init__(self, catalog):
        self.catalog = catalog
        self._sig = []

    def extrapolateShort(self):
        for numsat in range(0, len(self.catalog.line1) - 1):
            # формирование массива данных рассчётов

            line1 = self.catalog.line1[numsat]
            line2 = self.catalog.line2[numsat]
            sat1 = twoline2rv(line1, line2, wgs72)

            line1 = self.catalog.line1[numsat + 1]
            line2 = self.catalog.line2[numsat + 1]
            sat2 = twoline2rv(line1, line2, wgs72)

            dT = (self.catalog.JD[numsat + 1] - self.catalog.JD[numsat]) * 24 * 60

            x1, v1 = sgp4(sat1, dT)
            x2, v2 = sgp4(sat2, 0)

            self._sig.append(FullSigma(x1, x2))
        return self._sig

