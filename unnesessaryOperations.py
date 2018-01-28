from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import *
from math import *
from matplotlib.pyplot import *
from quickresult import *

def getDelta(tlefile, prognosis_period = 30):
    '''считаем положение спутника через prognosis_period дней  и выдаем
    разницу полной скорости и дальности по сравнению с положением по
    времени привязки'''
    prognosis_period_sec = prognosis_period * 24 * 3600
    di = getCoordinates(tlefile)
    diFuture = {}
    diDelta = {}
    for satname in di:
        timesec = di[satname][-1] + prognosis_period_sec
        time = datetime.fromtimestamp(timesec)
        sat = di[satname][0]
        oldpos, oldvelo = di[satname][1], di[satname][2]
        timetuple = (time.year, time.month, time.day, time.hour,
            time.minute, time.second + time.microsecond / 1e6)
        pos, velo = sat.propagate(*timetuple)
        newR = module(pos)
        newV = module(velo)
        deltaPos = abs(module(pos) - module(oldpos))
        deltaVelo = abs(module(velo) - module(oldvelo))
        diDelta[satname]  = (deltaPos, deltaVelo, prognosis_period)
    return diDelta

def getDealtas(tlelist, prognosis_period=30):
    '''по списку из тле файлов (и все они должны лежать тут) получаем для
    каждого спутника разницу между текущим положением и прогнозируемым'''
    i = 0
    N = len(tlelist)
    diDeltas = {}
    for tlefile in tlelist:
        i += 1
        print('reading %d of %d files...\r' % (i, N), end='')
        di = getDelta(tlefile, prognosis_period)
        for satname in di:
            r = di[satname][0]
            v = di[satname][1]
            try:
                diDeltas[satname]
            except KeyError:
                diDeltas[satname] = ([r], [v])
            else:
                diDeltas[satname][0].append(r)
                diDeltas[satname][1].append(v)
    return diDeltas
