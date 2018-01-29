from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import *
from math import *
from matplotlib.pyplot import *
import numpy as np

def getSatellites(tlefile):
    '''достает из тле файла имя спутника и создает экземпляр класса
    Satellite, который дальше можно использовать для работы модуля
    экстраполяции'''
    with open(tlefile, 'r') as fi:
        data = fi.readlines()
    satnames = data[0::3]
    indices = [j for j in range(len(data))][0::3]
    sats = []
    di = {}
    for i, name in enumerate(satnames):
        j = indices[i]
        sat = twoline2rv(data[j + 1], data[j + 2], wgs72)
        # if name[0] == '0':
            # name = 
        di[name[:-1]] = sat
    return di

def getCoordinates(tlefile, timetuple = -1):
    '''по названию тле файла и заданному в timetuple времени экстраполяции
    вычисляет положение и скорости, также выдает время привязки в
    секундах. timetuple надо задавать строго как (yyyy, mm, dd, hh, MM),
    mm - месяц ,MM  - минуты). Можно не задавать timetuple, тогда по
    дефолту будyт выдаваться координаты на время привязки'''
    di = getSatellites(tlefile)
    for name in di:
        sat = di[name]
        # TODO: проверить, что время привязки я определяю правильно
        current = sat.jdsatepoch + 17531 * 24 * 3600
        if timetuple == -1:
            time = datetime.fromtimestamp(current)
            timetuple = (time.year, time.month, time.day, time.hour,
                    time.minute, time.second + time.microsecond / 1e6)
        pos, velo = sat.propagate(*timetuple)
        di.update({name: (sat, pos, velo, current)})
    return di

module = lambda vector: sqrt(sum(j ** 2 for j in vector))

def getDelta(oldfile, newfile):
    '''должно выдавать разницу между спрогнозированным по старому файлу и
    плоученными текущими результатми из нового'''
    print(oldfile)
    print(newfile)
    olddict = getCoordinates(oldfile)
    newdict = getCoordinates(newfile)
    diDeltas = {}
    for satname in newdict:
        time = datetime.fromtimestamp(newdict[satname][-1])
        pos, velo = newdict[satname][1], newdict[satname][2]
        timetuple = (time.year, time.month, time.day, time.hour,
                time.minute, time.second + time.microsecond / 1e6)
        try:
            olddict[satname]
        except KeyError:
            pass
        else:
            prognosed_pos, prognosed_velo = olddict[satname][0].propagate(*timetuple)
            deltaR = abs(module(pos) - module(prognosed_pos))
            deltaV = abs(module(velo) - module(prognosed_velo))
            diDeltas[satname] = (deltaR, deltaV)
    return diDeltas

def getImage(diDeltas, isVelocity=False):
    '''рисуем гистограммки'''
    style.use('presentation.mplstyle')
    rax = subplot(111)
    x = [diDeltas[j][isVelocity] for j in diDeltas if np.isfinite(diDeltas[j][isVelocity])]
    rax.hist(np.log10(x), 75, normed=True)
    rax.grid(which='major')
    if isVelocity:
        vax.set_xlabel(r'$\log_{10}\left(\Delta V\right)$')
        vax.set_ylabel(r'$P(\log_{10}\left( \Delta V\right))$')
    else:
        rax.set_xlabel(r'$\log_{10}\left(\Delta R\right)$')
        rax.set_ylabel(r'$P(\log_{10}\left( \Delta R\right))$')
    return rax

