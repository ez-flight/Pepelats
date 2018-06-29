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
    catalog.readFullTLE('catalogs/zarya_2018_01_01_15.txt')
    
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
        
    delta = orbit2.get_ephem(ephem) - orbit1.get_ephem(ephem)

    return delta


def calcShort_R(catalog):
    '''  Возвращает массив полных ошибок "коротких интервалов"
    '''

    time = []
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
        
        time.append( (catalog.JD[numsat] - catalog.JD[0]) )
        sig.append(fullSigma(x1, x2))
    return sig, time


def calcLong_R(catalog, number = 0):
    ''' Возвращает массив полных ошибок "длинных интервалов"
    '''
    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    time = []
    sig = []
    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        time.append( (catalog.JD[numsat] - catalog.JD[number]) )
        sig.append( fullSigma(x1, x2) )
    return sig, time


def calcShort_3(catalog):
    '''    Возвращает три массива орбитальных ошибок "коротких интервалов"
    '''

    time = []
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

        time.append( (catalog.JD[numsat] - catalog.JD[0]) )
        sig1.append( s1 )
        sig2.append( s2 )
        sig3.append( s3 )

    return sig1, sig2, sig3, time


def calcLong_3(catalog, number = 0):
    ''' Возвращает три массива орбитальных ошибок "длинных интервалов"
    '''
    
    time = []
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

        time.append( (catalog.JD[numsat] - catalog.JD[number]) )
        sig1.append( s1 )
        sig2.append( s2 )
        sig3.append( s3 )

    return sig1, sig2, sig3, time


def calcShort_ephem(catalog, ephem):
    '''  Возвращает масиив ошибок по конкретному элементу орбиты
    '''

    time = []
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

        time.append( (catalog.JD[numsat] - catalog.JD[0]) )
        sig.append(s)

    return sig, time
    

def calcLong_ephem(catalog, ephem, number = 0):
    '''  Возвращает массив ошибок по конкретному элементу орбиты
    '''
    
    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    time = []
    sig = []
    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat2 = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[number]) * 24 * 60

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        s = ephemSigma(x1, v1, x2, v2, ephem)

        time.append( (catalog.JD[numsat] - catalog.JD[number]) )
        sig.append( s )

    return sig, time


def drawShort_R(catalog):
    '''  Создание графиков для коротких интервалов
    '''
    
    sig, time = calcShort_R(catalog)

    plt.plot(time, sig, 'r-')
    plt.plot(time, sig, 'k+')

    plt.xlabel('Epoсh')
    plt.ylabel(r'$\Delta R$')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawLong_R(catalog, number = 0):
    ''' Создание графиков "длинных" интервалов
    '''
    
    sig, time = calcLong_R(catalog, number)

    plt.plot(time, sig, 'b-')
    plt.plot(time, sig, 'k+')

    plt.plot(0, 0, 'k^')

    plt.xlabel('Epoсh')
    plt.ylabel(r'$\Delta R$')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawShort_3(catalog):
    '''  Создание графиков орбитальных ошибок для коротких интервалов
    '''

    sig1, sig2, sig3, time = calcShort_3(catalog)

    plt.plot(time, sig1, 'b-')
    plt.plot(time, sig2, 'r-')
    plt.plot(time, sig3, 'g-')

    plt.plot(time, sig1, 'k+')
    plt.plot(time, sig2, 'k+')
    plt.plot(time, sig3, 'k+')

    plt.legend( ("radial", "in-track", "cross-track"), loc='upper left' )

    plt.xlabel('Epoсh');
    plt.ylabel(r'$\Delta [km] $');
    plt.title(catalog.name[1]);
    plt.grid(True)
    plt.show()


def drawLong_3(catalog, number = 0):
    ''' Графики орбитальных для длинных интервалов
    '''
    
    sig1, sig2, sig3, time = calcLong_3(catalog, number)   

    plt.plot(time, sig1, 'b-')
    plt.plot(time, sig2, 'r-')
    plt.plot(time, sig3, 'g-')

    plt.plot(time, sig1, 'k+')
    plt.plot(time, sig2, 'k+')
    plt.plot(time, sig3, 'k+')
    
    plt.legend( ("radial", "in-track", "cross-track"), loc='upper left' )

    plt.plot(0, 0, 'k^')

    plt.xlabel('Epoсh');
    plt.ylabel(r'$\Delta [km]$');
    plt.title(catalog.name[1]);
    plt.grid(True)    
    plt.show()


def drawShort_ephem(catalog, ephem):
    '''  Создание графиков для коротких интервалов по элементу орбиты
    '''

    sig, time = calcShort_ephem(catalog, ephem)

    plt.plot(time, sig, 'r-')
    plt.plot(time, sig, 'k+')

    plt.xlabel('Epoсh');
    plt.ylabel(r'$\Delta Ephemeris$');         # СДЕЛАТЬ отображение конкретного элемента орбиты!!!!
    plt.title(catalog.name[1]);
    plt.grid(True)
    plt.show()


def drawLong_ephem(catalog, ephem, number = 0):
    ''' Создание графиков "длинных" интервалов для элемента орбиты
    '''
    
    sig, time = calcLong_ephem(catalog, ephem, number)

    plt.plot(time, sig, 'b-')
    plt.plot(time, sig, 'k+')

    plt.plot(0, 0, 'k^')

    plt.xlabel('Epoсh')
    plt.ylabel(r'$\Delta Ephemeris$')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawEphem_oneSat(catalog, ephem, dT, number = 0):
    ''' Создание графиков эволюции эфемериды в пронозе SGP
    
    catalog -- каталог ТЛЕ
    ephem --   название той эфемериды, что нам надо
    dT --      массив времён, на который строим график (в сутках)
    number --  номер данных в каталоге (по умолчанию 0)
    '''

    line1 = catalog.line1[number]
    line2 = catalog.line2[number]
    sat1 = twoline2rv(line1, line2, wgs72)

    time = []
    val = []
    for t in dT:
        x1, v1 = sgp4(sat1, t /24/60)

        orbit = KeplerOrbit()
        orbit.xyz2ephem(x1[0], x1[1], x1[2], v1[0], v1[1], v1[2])

        time.append(t);        
        val.append( orbit.get_ephem(ephem) )

   
    sig = calcLong_ephem(catalog, ephem, number)

    plt.plot(time, val, 'c-')
    plt.plot(time, val, 'k+')

    plt.xlabel('Epoсh (day)')
    plt.ylabel('Ephemeris')
    plt.title(catalog.name[1])
    plt.grid(True)
    plt.show()


def drawEphem_allcatalog(catalog, ephem):
    ''' Создание графиков эволюции эфемериды на протяжении полученного каталога
    
    catalog -- каталог ТЛЕ
    ephem --   название той эфемериды, что нам надо
    number --  номер данных в каталоге (по умолчанию 0)
    '''
        
    time = []
    val = []
    for numsat in range(0, len(catalog.line1)):
        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat = twoline2rv(line1, line2, wgs72)

        dT = (catalog.JD[numsat] - catalog.JD[0]) * 24 * 60

        x1, v1 = sgp4(sat, dT)
        
        orbit = KeplerOrbit()
        orbit.xyz2ephem(x1[0], x1[1], x1[2], v1[0], v1[1], v1[2])
        
        time.append( catalog.JD[numsat] - catalog.JD[0] )
    
        val.append(orbit.get_ephem(ephem))

    plt.plot(time, val, 'r-')
    plt.plot(time, val, 'k+')

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
    catalog.readTLEsat('catalogs/catalog_2016_06_30.txt', 'ISS')
    
    catalog.status()
    
    line1 = catalog.getLine1('ISS');
    line2 = catalog.getLine2('ISS');

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
    
    print('Эволюция параметров орбиты (на месяц):')
    dT = range(0, 30, 1)
    drawEphem_oneSat(catalog, 'a', dT)
    drawEphem_allcatalog(catalog, 'a')


if __name__ == "__main__":
    _testDraw()
    _testSGP()
