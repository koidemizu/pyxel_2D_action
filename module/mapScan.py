# -*- coding: utf-8 -*-
import pyxel

def map_scan(tile):
    map_data = []
    data_raw = []
    x = 30
    y = 30
    for y1 in range(y):
        for x1 in range(x):
            data = pyxel.tilemap(tile).pget(x1, y1)
            if data == (0, 6):
                d = 0
            elif data == (0, 0) or data == (1, 0):
                d = 1
            else:
                d = 2
            data_raw.append(d)
        map_data.append(data_raw)
        data_raw = []
        
    return map_data
