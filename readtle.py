#!/usr/bin/env python3

# набор функций для чтения тле-каталогов
# ЧЕРНОВИК!!!
# затем для структуры спутников сделать поля ВРЕМЯ и НОМЕРнорад

#    def __init__(self):
#    def ReadTLE_sat(self, catalog_file, SatName):
#    def ReadFullTLE(self, catalog_file):
#    def GetLine1(self, name):
#    def GetLine2(self, name):
#    def GetJD(year, mon, day):
#    def calcJD(self, name):

# обработать исключение, если задано несуществующее имя ИСЗ!!!!

class CatalogTLE:

    def __init__(self):
        ''' Инициализация, создание пустых полей
        '''
        
        print('readtle: инициализация')
        self.name   = []
        self.line1  = []
        self.line2  = []
        self.date   = []


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
            if (line_name == -1):
                close(fid)
                break

            if len(line_name) == 0:
                print('***  Неверное задание имени ИСЗ, либо имени файла!')
                return 0

            # главное условие на соответствие спутника и чтение двух строк
            if  length(findstr(tline_name, ISZname)):
                num_sat += 1
                
                f.name.append(line_name[2:-1])
                l1 = f.readline()   
                l2 = f.readline()
                self.line1.append(l1[2:-1])
                self.line2.append(l2[2:-1])
                self.JD = self.CalcJD(l1)
  
 


    def ReadFullTLE(self, catalog_file):
        ''' Полное чтение каталога TLE
        '''    
        f = open('zarya_2018_01_01_15.txt', 'r')
    
    
        print(' ');
        print('Чтение каталога FULL:');
        print(f)
    
        while 1:
            line_name = f.readline()
            if len(line_name) == 0:
                # достигли коца файла
                f.close()
                break
       
            self.name.append(line_name[2:-1])
            l1 = f.readline()
            l2 = f.readline()
            self.line1.append(l1[2:-1])
            self.line2.append(l2[2:-1])

            self.JD = self.CalcJD(l1)
  
  
    def GetLine1(self, name):
        ''' По названию аппарата возвращать первую строку параметров его орбиты
        '''    
        num = name.index(name)
        print(num)
        return self.line1[num]   


    def GetLine2(self, name):
        ''' По названию аппарата возвращать вторую строку параметров его орбиты
        '''    
        num = name.index(name)
        return self.line2[num]   


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



