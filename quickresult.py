from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

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
        di[name[:-1]] = sat
    return di

def getCoordinates(tlefile, timetuple):
    '''по названию тле файла и заданному в timetuple времени экстраполяции
    вычисляет положение и скорости, также выдает время привязки в
    секундах. timetuple надо задавать строго как (yyyy, mm, dd, hh, MM),
    mm - месяц ,MM  - минуты)'''
    di = getSatellites(tlefile)
    for name in di:
        sat = di[name]
        tpriv = sat.jdsatepoch + 17531 * 24 * 3600
        pos, velo = sat.propagate(*timetuple)
        di.update({name: (pos, velo, tpriv)})
    return di

# def getExtroplation(tlefile):
