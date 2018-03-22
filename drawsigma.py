#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
from math import sqrt



from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4

from readtle import CatalogTLE

from matplotlib.pyplot import plot
from mpl_toolkits.axes_grid.inset_locator import inset_axes
# import numpy as np

from pylab import show


def OpenFile():
    '''  что-то там открываем
    '''
    catalog = CatalogTLE()
    catalog.ReadFullTLE('zarya_2018_01_01_15.txt')
    
    return catalog


def FullSigma(x1, x2):
    '''  Вычисление полной ошибки между двумя положениями спутников
    '''
    sigma = sqrt( (x1[0] - x2[0])**2 + (x1[1] - x2[1])**2 + (x1[2] - x2[2])**2 )
    
    return sigma
    
    
def OrbitSigma(x1, v1, x2, v2):
    ''' Вычисление трёх составляющих ошибки 
        -- радиальной, 
        -- в-треке
        -- cross-треке
    '''
    x0 = x2[0]
    y0 = x2[1]
    z0 = x2[2]

    # вычисление ошибки 1
    A = x1[0]
    B = x1[1]
    C = x1[2]
    D = - A * x1[0] - B * x1[1] - C * x1[2]
    sigma1 = (A*x0 + B*y0 + C*z0 + D) / sqrt(A**2 + B**2 + C**2)

    # вычисление ошибки 2
    A = v1[0]
    B = v1[1]
    C = v1[2]        
    D = - A * x1[0] - B * x1[1] - C * x1[2]
    sigma2 = (A*x0 + B*y0 + C*z0 + D) / sqrt(A**2 + B**2 + C**2)

    # вычисление ошибки 3
    A = + x1[1] * x2[2] - x2[1] * x1[2]
    B = - x1[0] * x2[2] + x2[0] * x1[2]
    C = + x1[0] * x2[1] - x2[0] * x1[1]
    D = 0
    sigma3 = (A*x0 + B*y0 + C*z0 + D) / sqrt(A**2 + B**2 + C**2)
 
    return sigma1, sigma2, sigma3
    

def DrawShort(catalog):
    '''  Создание графиков на коротких отрезках
    '''

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

        sig.append(FullSigma(x1, x2))

    plot(sig, 'c--')
    plot(sig, 'rx')

    show()


def DrawLong(catalog, number = 0):
    ''' Создание графиков "длинных" отрезков
    '''

    sig = []

    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        sig.append( FullSigma(x1, x2) )

    plot(sig, 'c--')
    plot(sig, 'rx')

    show()


def draw3(catalog, number = 0):
    '''
    '''
    
    sig1 = []
    sig2 = []
    sig3 = []
    
    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, number)

        s1, s2, s3 = orbitSigma(x0, v0, x2, v2)

        sig1.append( s1 )
        sig2.append( s2 )
        sig3.append( s3 )

    plot(sig1, 'c--')
    plot(sig2, 'r--')
    plot(sig3, 'g--')

    show()
    
    


def main():
    print('Ку! 1')
    catalog = OpenFile()
    print('Ку! 2')
    DrawShort(catalog)
    print('Ку! 3')
    DrawLong(catalog)
    print('Ku!!!!')
    draw3(catalog)
    


if __name__ == "__main__":
    main()
