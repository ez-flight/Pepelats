#!/usr/bin/env python3

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

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
    
    position, velocity = satellite.propagate(2016, 6, 30, 12, 0, 0)

    print('---   error   ---');
    print(satellite.error)    # nonzero on error

    print('---   error_message   ---:');
    print(satellite.error_message)

    print('---   position   ---');
    print(position)

    print('---   velocity   ---');
    print(velocity)
 
    

def main_test():
#    test1()
#    test2()
    test3()
    
     


if __name__=="__main__":
    main_test()

