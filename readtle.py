#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# набор функций для чтения тле-каталогов
# ЧЕРНОВИК!!!
# затем для структуры спутников сделать поля ВРЕМЯ и НОМЕРнорад

#    поля класса:
#    name
#    line1
#    line2
#    JD
#
#    def __init__(self):
#    def ReadTLE_sat(self, catalog_file, SatName):
#    def ReadFullTLE(self, catalog_file):
#    def Status(self):
#    def GetLine1(self, name):
#    def GetLine2(self, name):
#    def GetJD(self, name):
#    def CalcJD(self, name):

# обработать исключение, если задано несуществующее имя ИСЗ!!!!


from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv


class CatalogTLE:

    def __init__(self):
        ''' Инициализация, создание пустых полей
        '''
        print('readtle: инициализация')
        self.name   = []
        self.line1  = []
        self.line2  = []
        self.JD     = []


    def ReadTLEsat(self, catalog_file, SatName):
        ''' Чтение информации из каталога по конкретному аппарату
        '''
        f = open(catalog_file, 'r')

        # количество найденных ИСЗ в каталоге
        num_sat = 0;

        while 1:
            # бесконечное построковое чтение, 
            # пока не найдём нужный нам спутник
            line_name = f.readline();

            # достигли конца файла, завершение чтения
            if len(line_name) == 0:
                f.close()
                if  (len(self.line1) == 0):
                    print('*** Неверное задание имени ИСЗ, либо имени файла!')
                return 0

            # главное условиsе на соответствие спутника и чтение двух строк
            if  line_name.find(SatName) != -1:
                num_sat += 1
                
                l1 = f.readline()   
                l2 = f.readline()
                
                self.name.append(line_name[2:-1])
                self.line1.append(l1)
                self.line2.append(l2)
                self.JD.append(self.CalcJD(l1))
  
 
 
    def ReadFullTLE(self, catalog_file):
        ''' Полное чтение каталога TLE
        '''    
        f = open(catalog_file, 'r')
    
        print(' ');
        print('Полное чтение каталога:');
    
        while 1:
            line_name = f.readline()
            if len(line_name) == 0:
                print('ReadFull: чтение завершено, объектов: ', len(self.line1));
                f.close()
                break
       
            self.name.append(line_name[2:-1])
            l1 = f.readline()
            l2 = f.readline()
            self.line1.append(l1)
            self.line2.append(l2)
            self.JD.append(self.CalcJD(l1))


    def GetName(self, num):
        ''' По номеру записи в массиве возвращать название аппарата
        '''    
        return self.name[num]   
  
  
    def GetLine1(self, name):
        ''' По названию аппарата возвращать первую строку параметров его орбиты
        '''    
        num = name.index(name)
        return self.line1[num]   


    def GetLine2(self, name):
        ''' По названию аппарата возвращать вторую строку параметров его орбиты
        '''    
        num = name.index(name)
        return self.line2[num]   


    def GetJD(self, name):
        ''' По названию аппарата возвращать временнУю привязку его эфемерид
        '''
        num = name.index(name)
        return self.JD[num]


    def CalcJD(self, line_str):
        ''' По данным первой строки вычисляет MJD привязки эфемерид спутника
        '''
        year = float(line_str[19:20])
        if year < 57:
            year =+ 2000
        else:
            year =+ 1900

        n_day = float(line_str[21:32])

        # юлианская дата на 1 января текущего года
        mon = 1
        day = 1
        JD_0 = 1721013.5 + 367*year - int( 7 * (year + int( (mon+9)/12)) / 4) + int(275 * mon / 9) + day;
        
        JD = JD_0 + n_day
        
        return JD


    def Status(self):
        ''' Выводит информацию о текущем состоянии каталога
        '''
        
        print('Объектов в каталоге:', len(self.name));
        # вывести время привязки первого и последней записи в каталоге!!!
        
        print('Аппарат:', self.name[1] );
        
        print('Данные за следующий временной интервал:', self.JD[1], ' -- ', self.JD[-1] );
        

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
    
    
def test():
    test1()
    test2()


if __name__=="__main__":
    test()
