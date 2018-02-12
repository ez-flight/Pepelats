#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

from sgp4.propagation import sgp4

import readtle
from readtle import *


def test1():
    ''' Тестируем ReadFullTLE
    '''
    print('  ')
    print('Тест номер один.');

    a = CatalogTLE()

    print(a);
    
    a.ReadFullTLE('catalogs/catalog_2016_06_30.txt')
    
    print(a.name[0])    
    print(a.line1[0])
    print(a.line2[0])
    
    print(' * * *     ----------     * * *');
    print(a.name[1])    
    print(a.line1[1])
    print(a.line2[1])
    
    print(' * * *     ----------     * * *');
    print(a.name[2])    
    print(a.line1[2])
    print(a.line2[2])
    

def test2():
    ''' Тестируем ReadTLEsat
    '''
    print('  ')
    print('Тест номер 2.');
    print(' * * *    выбор по имени спутника:     * * *');
    print('Работаем по спутнику ISS:')

    print(' * * *    чтение по имени ИСЗ    * * *');
    print('  ')
    
    b = CatalogTLE()
    b.ReadTLEsat('zarya_2018_01_01_15.txt', 'ISS')
    
    print('Данные по ISS:')
    print(b.GetLine1('ISS'))
    print(b.GetLine2('ISS'))
        
        
def test3():
    ''' Тестируем чтение информации по ИСЗ + вычисление координат
    '''
    print('  ')
    print('Тест 3. Чтение эфемерид и прогноз положения ИСЗ.');        
 
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



def test4():
    ''' Тест прототипа наших вычислений, вычитания положения
        из предыдущих и последущих положений по эфемеридам
    '''

    print(' ')
    print('  Т Е С Т  4  ')
    print(' ')

    catalog = CatalogTLE()
    catalog.ReadTLEsat('zarya_2018_01_01_15.txt', 'ISS')


    line1 = catalog.GetLine1('ISS')
    line2 = catalog.GetLine2('ISS')

    for numsat in range(0, 5):
        # формирование массива данных рассчётов

        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]
        sat1 = twoline2rv(line1, line2, wgs72)

        line1 = catalog.line1[numsat + 1]
        line2 = catalog.line2[numsat + 1]
        sat2 = twoline2rv(line1, line2, wgs72)

        print(numsat)

        print(catalog.JD[numsat])
        print(catalog.name[numsat])
        print(catalog.JD[numsat + 1])
        print(catalog.name[numsat])

        dT = (catalog.JD[numsat + 1] - catalog.JD[numsat])
        print(dT)
        dT = dT * 24*60
        print(dT)

        x1, v1 = sgp4(sat1, dT)
        x2, v2 = sgp4(sat2, 0)

        print(' ')
        print(x1)
        print(x2)

        print('  - - - - - - - - - - - - - - - - - ')
        print(x2[1] - x1[1])
        print('  - - - - - - - - - - - - - - - - - ')


def test5():
    ''' Тест прототипа наших вычислений, вычитания положения
        из первого и последущих положений "большие интервалы"
    '''

    print(' ')
    print('  Т Е С Т  5  ')
    print(' ')

    catalog = CatalogTLE()
    catalog.ReadTLEsat('zarya_2018_01_01_15.txt', 'ISS')


    line1 = catalog.line1[0]
    line2 = catalog.line2[0]

    sat_0 = twoline2rv(line1, line2, wgs72)
    time_0 = catalog.JD[0]

    x_0, v_0 = sgp4(sat_0, 0)

    for numsat in range(1, 10):
        # формирование массива данных рассчётов

        line1 = catalog.line1[numsat]
        line2 = catalog.line2[numsat]

        sat_i = twoline2rv(line1, line2, wgs72)

        print(catalog.JD[numsat])

        dT = (catalog.JD[numsat] - time_0) *24*60

        x_i, v_i = sgp4(sat_i, dT)

        print(dT)
        print(x_i[0] - x_0[0])


def main_test():
    test1()
    test2()
    test3()
    test4()
    test5()




if __name__=="__main__":
    main_test()

