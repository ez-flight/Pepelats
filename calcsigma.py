#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from math import sqrt


from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4

from readtle import CatalogTLE

from KeplerOrbit import KeplerOrbit

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import inset_axes
# import numpy as np

# from pylab import show


def _openFile():
    '''  Открытие файла -- каталога TLE. Для тестовых функций.
    '''
    catalog = CatalogTLE()
    catalog.ReadFullTLE('catalogs/zarya_2018_01_01_15.txt')
    
    return catalog


def fullSigma(x1, x2):
    '''  Вычисление полной ошибки между двумя положениями спутников
    '''
    sigma = sqrt( (x1[0] - x2[0])**2 + (x1[1] - x2[1])**2 + (x1[2] - x2[2])**2 )
    
    return sigma
    
    
def orbitSigma(x1, v1, x2, v2):
    ''' Вычисление трёх составляющих ошибки 
        -- radial, 
        -- in-track
        -- cross-track
    '''
    x = x2[0]     # координаты точки, до которой вычисляем расстояние
    y = x2[1]
    z = x2[2]

    # радиальная ошибка
    A = x1[0]
    B = x1[1]
    C = x1[2]
    D = - A * x1[0] - B * x1[1] - C * x1[2]
    sigma1 = (A*x + B*y + C*z + D) / sqrt(A**2 + B**2 + C**2)

    # ошибка по треку (опережение прогноза)
    A = v1[0]
    B = v1[1]
    C = v1[2]        
    D = - A * x1[0] - B * x1[1] - C * x1[2]
    sigma2 = (A*x + B*y + C*z + D) / sqrt(A**2 + B**2 + C**2)

    # кросс-трек, над плоскостью прогноза
    A = + x1[1] * v1[2] - v1[1] * x1[2]
    B = - x1[0] * v1[2] + v1[0] * x1[2]
    C = + x1[0] * v1[1] - v1[0] * x1[1]
    D = 0
    sigma3 = (A*x + B*y + C*z + D) / sqrt(A**2 + B**2 + C**2)
 
    return sigma1, sigma2, sigma3


def ephemSigma(x1, v1, x2, v2, ephem):
    ''' Вычисление ошибки по конкретному элементу орбиты
    '''

    orbit1 = KeplerOrbit()
    orbit1.xyz2ephem(x1[0], x1[1], x1[2], v1[0], v1[1], v1[2])
    orbit2 = KeplerOrbit()
    orbit2.xyz2ephem(x2[0], x2[1], x2[2], v2[0], v2[1], v2[2])

    if ephem == 'a':
        delta = orbit2.semimajor_axis - orbit1.semimajor_axis

    elif ephem == 'e':
        delta = orbit2.eccentricity - orbit1.eccentricity

    elif ephem == 'i':
        delta =  orbit2.inclination - orbit1.inclination

    elif ephem == 'd':
        delta = orbit2.draco - orbit1.draco

    elif ephem == 'w':
        delta = orbit2.omega - orbit1.omega

    else:
        delta = orbit2.M_0 - orbit1.M_0

    return delta



def calcShort_R(catalog):
    '''  Возвращает массив полных ошибок "коротких интервалов"
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

        sig.append(fullSigma(x1, x2))

    return sig


def calcLong_R(catalog, number = 0):
    ''' Возвращает массив полных ошибок "длинных интервалов"
    '''
    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    sig = []
    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        sig.append( fullSigma(x1, x2) )

    return sig


def calcShort_3(catalog):
    '''    Возвращает три массива орбитальных ошибок "коротких интервалов"
    '''

    sig1 = []
    sig2 = []
    sig3 = []

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

        s1, s2, s3 = orbitSigma(x1, v1, x2, v2)

        sig1.append( s1 )
        sig2.append( s2 )
        sig3.append( s3 )

    return sig1, sig2, sig3


def calcLong_3(catalog, number = 0):
    ''' Возвращает три массива орбитальных ошибок "длинных интервалов"
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
        x2, v2 = sgp4(sat2, 0)

        s1, s2, s3 = orbitSigma(x1, v1, x2, v2)

        sig1.append( s1 )
        sig2.append( s2 )
        sig3.append( s3 )

    return sig1, sig2, sig3


def calcShort_ephem(catalog, ephem):
    '''  Возвращает масиив ошибок по конкретному элементу орбиты
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

        s = ephemSigma(x1, v1, x2, v2, ephem)

        sig.append(s)

    return sig
    

def calcLong_ephem(catalog, ephem, number = 0):
    '''  Возвращает массив ошибок по конкретному элементу орбиты
    '''
    
    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    sig = []
    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        s = ephemSigma(x1, v1, x2, v2, ephem)

        sig.append( s )

    return sig


def drawShort_R(catalog):
    '''  Создание графиков для коротких интервалов
    '''
    
    sig = calcShort_R(catalog)

    plt.plot(sig, 'c-')
    plt.plot(sig, 'rx')

    plt.xlabel('Epoсh')
    plt.ylabel(r'$\sigma R$')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawLong_R(catalog, number = 0):
    ''' Создание графиков "длинных" интервалов
    '''
    
    sig = calcLong_R(catalog, number)

    plt.plot(sig, 'c-')
    plt.plot(sig, 'rx')

    plt.plot(number, 0, 'k^')

    plt.xlabel('Epoсh')
    plt.ylabel(r'$\sigma R$')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawShort_3(catalog):
    '''  Создание графиков орбитальных ошибок для коротких интервалов
    '''

    sig1, sig2, sig3 = calcShort_3(catalog)

    plt.plot(sig1, 'c-')
    plt.plot(sig2, 'r-')
    plt.plot(sig3, 'g-')

    plt.plot(sig1, 'kx')
    plt.plot(sig2, 'kx')
    plt.plot(sig3, 'kx')

    plt.xlabel('Epoсh');
    plt.ylabel(r'$\sigma R $');
    plt.title(catalog.name[1]);
    plt.grid(True)
    plt.show()


def drawLong_3(catalog, number = 0):
    ''' Графики орбитальных для длинных интервалов
    '''
    
    sig1, sig2, sig3 = calcLong_3(catalog, number)   

    plt.plot(sig1, 'c-')
    plt.plot(sig2, 'r-')
    plt.plot(sig3, 'g-')

    plt.plot(sig1, 'kx')
    plt.plot(sig2, 'kx')
    plt.plot(sig3, 'kx')

    plt.plot(number, 0, 'k^')

    plt.xlabel('Epoсh');
    plt.ylabel(r'$\sigma R $');
    plt.title(catalog.name[1]);
    plt.grid(True)    
    plt.show()


def drawShort_ephem(catalog, ephem):
    '''  Создание графиков для коротких интервалов по элементу орбиты
    '''

    sig = calcShort_ephem(catalog, ephem)

    plt.plot(sig, 'c-')
    plt.plot(sig, 'rx')

    plt.xlabel('Epoсh');
    plt.ylabel('Ephemeris');         # СДЕЛАТЬ отображение конкретного элемента орбиты!!!!
    plt.title(catalog.name[1]);
    plt.grid(True)
    plt.show()


def drawLong_ephem(catalog, ephem, number = 0):
    ''' Создание графиков "длинных" интервалов для элемента орбиты
    '''
    
    sig = calcLong_ephem(catalog, ephem, number)

    plt.plot(sig, 'c-')
    plt.plot(sig, 'rx')

    plt.plot(number, 0, 'k^')

    plt.xlabel('Epoсh')
    plt.ylabel('Ephemeris')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def _testSGP():
    ''' Тестируем чтение информации по ИСЗ + вычисление координат
    '''
    print('  ')
    print('Тест SGP.');        
 
    catalog = CatalogTLE()  
    catalog.ReadTLEsat('catalogs/catalog_2016_06_30.txt', 'ISS')
    
    catalog.Status()
    
    line1 = catalog.GetLine1('ISS');
    line2 = catalog.GetLine2('ISS');

    satellite = twoline2rv(line1, line2, wgs72)
    
#    position, velocity = satellite.propagate(2016, 6, 30, 12, 0, 0)

    position, velocity = sgp4(satellite, 10.001)

    print('---   error   ---');
    print(satellite.error)    # nonzero on error

    print('---   error_message   ---:');
    print(satellite.error_message)

    print('---   position   ---');
    print(position)

    print('---   velocity   ---');
    print(velocity)
    

def _testDraw():
    print('открытие каталога:')
    catalog = _openFile()

    print('Графики полной ошибки:')
    drawShort_R(catalog)
    drawLong_R(catalog)
    drawLong_R(catalog, 10)

    print('Орбитальные ошибки:')
    drawShort_3(catalog)
    drawLong_3(catalog)
    drawLong_3(catalog, 10)

    print('Ошибки большой полуоси:')
    drawShort_ephem(catalog, 'a')
    drawLong_ephem(catalog, 'a')
    drawLong_ephem(catalog, 'a', 10)


if __name__ == "__main__":
    _testDraw()
    _testSGP()
