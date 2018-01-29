from sgp4.earth_gravity import wgs72 as earth
from sgp4.io import twoline2rv
from datetime import *
from math import *
from matplotlib.pyplot import *
import numpy as np
from manysats import module

def accumulateValues(_dict, _key, _value):
    try:
        _dict[_key]
    except KeyError:
        _dict[_key] = [_value]
    else:
        _dict[_key].append(_value)
    return _dict

class SatelliteSet:
    def __init__(self, tlefile='ALL_TLE.TXT'):
        with open(tlefile, 'r') as fi:
            data = fi.readlines()
        self.tledata = data
        self.satellites = self._convert()
        self.coordinates = self._calc_coordinates()

    def __repr__(self):
        string = ''
        for aKey in self.satellites.keys():
            string += '%s\n' % aKey
        return string
    def __len__(self):
        return len(self.satellites)

    def _convert(self):
        '''конвертация из тле формата в Satellite'''
        data = self.tledata
        names = data[0::3]
        indices = [j for j in range(len(data))][0::3]
        satellites = {}
        for i, badname in enumerate(names):
            if badname.startswith('0 '):
                name = badname[2:-1]
            else:
                name = badname[:-1]
            j = indices[i]
            sat = twoline2rv(data[j + 1], data[j + 2], earth)
            satellites = accumulateValues(satellites, name, sat)
        return satellites

    def _calc_coordinates(self):
        '''получение текущих координат'''
        coordinates = {}
        for name in self.satellites:
            sats = self.satellites[name]
            times = []
            distances = []
            velocities = []
            for sat in sats:
                epoch = sat.epoch
                pos, velo = sat.propagate(*epoch.timetuple()[:-3])
                distances.append(module(pos))
                velocities.append(module(velo))
                times.append(epoch)
            coordinates[name] = (times, distances, velocities, sats)
        return coordinates

    def _getQuickFuture(self):
        '''Экстраполяция на значение соседнего полученного замера'''
        quick_future = {}
        for name in self.coordinates:
            epochs, rs, vs, sats = self.coordinates[name]
            extra_r = []
            extra_v = []
            times = []
            for i in range(len(sats) - 1):
                _time = epochs[i + 1]
                extra_pos, extra_velo = sats[i].propagate(*_time.timetuple()[:-3])
                extra_r.append(module(extra_pos))
                extra_v.append(module(extra_velo))
                times.append(_time)
            quick_future[name] = (times, extra_r, extra_v)
        return quick_future

    def _getProgressiveFuture(self):
        '''Экстраполяция первого замера на времена всех последующих'''
        progressive_future = {}
        for name in self.coordinates:
            epochs, rs, vs, sats = self.coordinates[name]
            extra_r = []
            extra_v = []
            times = []
            progressive = {}
            for sat in sats:
                _time = sat.epoch
                extra_pos, extra_velo = sats[0].propagate(*_time.timetuple()[:-3])
                extra_r.append(module(extra_pos))
                extra_v.append(module(extra_velo))
                times.append(_time)
            progressive_future[name] = (times, extra_r, extra_v)
        return progressive_future

    def getResidual(self, isQuick=True):
        '''Выдача разницы координат текущего замера и предшествующего,
        экстраполированного на момент привязки текущего замера.
        isQuick=True дает быстроменяющуюся разницу между соседними
        замерами, isQuick=False - разницу между всеми и эстраполированным
        первым'''
        if isQuick:
            _future = self._getQuickFuture()
        else:
            _future = self._getProgressiveFuture()
        residuals = {}
        for name in _future:
            current = self.coordinates[name]
            if isQuick:
                r_current = np.array(current[1][1:])
                v_current = np.array(current[2][1:])
            else:
                r_current = np.array(current[1][0])
                v_current = np.array(current[2][0])
            r_future = np.array(_future[name][1])
            v_future = np.array(_future[name][2])
            dr = abs(r_future - r_current)
            dv = abs(v_future - v_current)
            residuals[name] = (_future[name][0], dr, dv)
        return residuals


