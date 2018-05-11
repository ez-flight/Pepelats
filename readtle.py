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
#    def readTLE_sat(self, catalog_file, SatName):
#    def readFullTLE(self, catalog_file):
#    def status(self):
#    def getLine1(self, name):
#    def getLine2(self, name):
#    def getJD(self, name):
#    def calcJD(self, name):

# обработать исключение, если задано несуществующее имя ИСЗ!!!!

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4
import logging

from datetime import datetime
from datetime import timedelta


class CatalogTLE:

    def __init__(self):
        ''' Инициализация, создание пустых полей
        '''
        self.logger = logging.getLogger('__main__.' + __name__ )
        self.logger.info('readtle: инициализация')
        self.name   = []
        self.line1  = []
        self.line2  = []
        self.JD     = []
        self.time   = []


    def readTLEsat(self, catalog_file, SatName):
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
                self.JD.append(self.calcJD(l1))
                self.time.append(self.calcTime(l1))


    def readFullTLE(self, catalog_file):
        ''' Полное чтение каталога TLE
        '''
        f = open(catalog_file, 'r')

        self.logger.info('Полное чтение каталога:');
    
        while 1:
            line_name = f.readline()
            if len(line_name) == 0:
                self.logger.info('ReadFull: чтение завершено, объектов: %s' % len(self.line1));
                f.close()
                break
       
            self.name.append(line_name[2:-1])
            l1 = f.readline()
            l2 = f.readline()
            self.line1.append(l1)
            self.line2.append(l2)
            self.JD.append(self.calcJD(l1))
            self.time.append(self.calcTime(l1))


    def getName(self, num):
        ''' По номеру записи в массиве возвращать название аппарата
        '''    
        return self.name[num]   
  
  
    def getLine1(self, name):
        ''' По названию аппарата возвращать первую строку параметров его орбиты
        '''    
        num = name.index(name)
        return self.line1[num]   


    def getLine2(self, name):
        ''' По названию аппарата возвращать вторую строку параметров его орбиты
        '''    
        num = name.index(name)
        return self.line2[num]   


    def getJD(self, name):
        ''' По названию аппарата возвращать временнУю привязку его эфемерид
        '''
        num = name.index(name)
        return self.JD[num]


    def calcJD(self, line_str):
        ''' По данным первой строки вычисляет MJD привязки эфемерид спутника
        '''
        year = float(line_str[18:20])
        if year < 57:
            year = year + 2000
        else:
            year = year + 1900

        n_day = float(line_str[20:32])

        # юлианская дата на 1 января текущего года
        mon = 1
        day = 1
        JD_0 = 1721013.5 + 367*year - int( 7 * (year + int( (mon+9)/12)) / 4) + int(275 * mon / 9) + day;
        
        JD = JD_0 + n_day
        
        return JD
        
        
    def calcTime(self, line_str):
        ''' По данным первой строки вычисляет питоновское время привязки эфемерид спутника
        '''
        year = float(line_str[18:20])

        if year < 57:
            year = year + 2000
        else:
            year = year + 1900

        # дата на 1 января текущего года      mon = 1     day = 1
        time_temp = datetime(int(year), 1, 1)

        # время, прошедшее с первого января
        d_time = timedelta(float(line_str[21:32]))

        time = time_temp + d_time

        return time


    def calcXYZ(self, name, time):
        '''  Вычисление прямоугольных координат.
             на выходе:
             -- кординаты аппарата
             -- скорости
             -- номер использованных эфемерид в каталоге
             -- длительность экстраполяции (в минутах)
        '''

        # поиск ближайшего ИСЗ к этому моменту времени
        d_since = 1e+10
        num = -1
        for i in range(0, len(self.time)):

            if  self.name[i].find(name) == -1:   # не тот спутник, пропускаем
                continue

            d_day = time - self.time[i]
            d_sinceNew = d_day.days *24*60 + d_day.seconds /60

            if  (abs(d_sinceNew) < abs(d_since)):  # более свежие эфемериды
                num = i
                d_since = d_sinceNew

        line1 = self.line1[num]
        line2 = self.line2[num]

        satellite = twoline2rv(line1, line2, wgs72)
        #    position, velocity = satellite.propagate(2016, 6, 30, 12, 0, 0)
        position, velocity = sgp4(satellite, d_since)

        return position, velocity, num, d_since


    def status(self):
        ''' Выводит информацию о текущем состоянии каталога
        '''
        
        self.logger.info('Объектов в каталоге:', len(self.name));
        # вывести время привязки первого и последней записи в каталоге!!!
        
        self.logger.info('Аппарат:', self.name[1] );
        self.logger.info(self.time[1]);
        self.logger.info(self.time[-1]);
        self.logger.info('Данные за следующий временной интервал:', self.JD[1], ' -- ', self.JD[-1] );


def _test1():
    ''' Тестируем ReadFullTLE
    '''
    print('  ')
    print('Тест номер один.');

    a = CatalogTLE()

    print(a);
    
    a.readFullTLE('catalogs/catalog_2016_06_30.txt')

    a.status()

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
   
    
def _test2():
    ''' Тестируем ReadTLEsat
    '''
    print('  ')
    print('Тест номер 2.');
    print(' * * *    выбор по имени спутника:     * * *');
    print('Работаем по спутнику ISS:')

    print(' * * *    чтение по имени ИСЗ    * * *');
    print('  ')
    
    b = CatalogTLE()
    b.readTLEsat('catalogs/zarya_2018_01_01_15.txt', 'ISS')
    
    print('Данные по ISS:')
    print(b.getLine1('ISS'))
    print(b.getLine2('ISS'))
    
    b.status()
        

def _test3():
    ''' тестируем точное вычисление координат по ближайшим эфемеридам
    '''     
    print(' Тест вычисления по ближайшим эфемеридам:')

    b = CatalogTLE()
    b.readTLEsat('catalogs/zarya_2018_01_01_15.txt', 'ISS')
    
    b.status()

    date = datetime.strptime("15/01/18 15:30", "%d/%m/%y %H:%M")

    position, velocity, num, d_since = b.calcXYZ('ISS', date)
    
    print(position)
    print(d_since)    
    print(num)    
   

if __name__=="__main__":
    _test1()
    _test2()
    _test3()
