#!/usr/bin/env python3

import readtle
from readtle import *

def test1():
    print('Тест номер один.');

    a = CatalogTLE()

    print(a);
    
    a.ReadFullTLE('catalogs/catalog_2016_12_07.txt')
    
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
    print('Тест номер 2.');
    print(' * * *    выбор по имени спутника:     * * *');
    print('Работаем по спутнику ISS:')
    print(a.GetLine1('ede'))
    print(a.GetLine2('323'))


    print(' * * *    чтение по имени ИСЗ    * * *');
    print('  ')
    
    b = CatalogTLE()
    b.ReadTLEsat('zarya_2018_01_01_15.txt', 'ISS')
        

def main_test():
    test1()
    test2()


if __name__=="__main__":
    main_test()

