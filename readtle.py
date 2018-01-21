#!/usr/bin/env python3

# набор функций для чтения тле-каталогов
# ЧЕРНОВИК!!!
# затем для структуры спутников сделать поля ВРЕМЯ и НОМЕРнорад

class CatalogTLE

    def __init__(self):
    ''' Инициализация, создание пустых полей
    '''
        self.name   = []
        self.line1  = []
        self.line2  = []
        self.date   = []


    def ReadTLE_sat(self, catalog_file, SatName)
    ''' Чтение информации из каталога по конкретному аппарату
    '''
        fid = fopen(catalog_file);
    
        # количество найденных ИСЗ в каталоге
        num_sat = 0;
        
        while true:
            # бесконечное построковое чтение, 
            # пока не найдём нужный нам спутник
            tline_name = f.readline(fid);
           
            # достигли конца файла, авершение чтения
            if (line_name == -1):
                fclose(fid)
                break
                
            if len(line_name) == 0
                print('***  Неверное задание имени ИСЗ, либо имени файла!']);
                return 0
            
            # главное условие на соответствие спутника и чтение двух строк
            if  length(findstr(tline_name, ISZname)):
                num_sat += 1
                      
                self.name.append(line_name(3:-1))            
                self.line1.append(f.readline(fid))
                self.line2.append(f.readline(fid))           
                self.JD = CalcJD(self.line1)
 


    def ReadFullTLE(self, catalog_file)
    ''' Полное чтение каталога TLE
    '''    
        fid = fopen(catalog_file);
    
        # количество найденных ИСЗ в каталоге
        num_sat = 0;
    
        while true:
            num_sat =+ 1
            line_name = f.readline(fid);
       
            # достигли конца файла, завершение чтения
            if (line_name == -1):
                fclose(fid)
                break
         
            self.name.append(line(3:end))            
            self.line1.append(f.readline(fid))
            self.line2.append(f.readline(fid))
            self.JD = CalcJD(self.line1)
 
 
    def getSAT(self, name)
    ''' По названию аппарата возвращать две строки параметров его орбиты
    '''    
        num = name.index(name)
        line1 = self.line1(num)
        line2 = self.line2(num)


    def CalcJD(line_str)
    ''' По данным первой строки вычисляет MJD привязки эфемерид спутника
    '''
        year = float(linestr(19:20))
        if year < 57
            year =+ 2000
        else
            year =+ 1900
            
        n_day = float(linestr(21:32))
        
        # юлианская дата на 1 января
        JD_0 = GetGD(year, 1, 1);
        
        JD = JD_0 + n_day
        
        return JD


    def GetJD(year, mon, day)
    ''' по значению года, месяца и дня определяет Юлианскую дату
    '''
        JD = 1721013.5 + 367*year 
            - int( 7 * (year + int( (mon+9)/12)) / 4) 
            + int(275 * mon / 9) + day;

        return JD

