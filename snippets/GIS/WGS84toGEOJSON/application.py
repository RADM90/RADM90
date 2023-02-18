import geojson
import pandas as pd
import time
# Read .csv File with Pandas
csv = pd.read_csv('Coordinates.csv')
array = []
for idx in range(len(csv['X1'])):
    x1 = csv['X1'][idx]
    y1 = csv['Y1'][idx]
    x2 = csv['X2'][idx]
    y2 = csv['Y2'][idx]

    geometry = geojson.Polygon(coordinates=[[(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)]])
    polygon = geojson.Feature(id=None, geometry=geometry)

    aoi = open(time.strftime('%y%m%d', time.localtime(time.time())) + '_AOI_'+str(idx+1)+'.geojson', 'w')
    aoi.write(str(polygon))
    print(polygon)
    array.append(polygon)
    aoi.close()

# feat_col = geojson.FeatureCollection(array)
# print(feat_col)


"""
# String-Float Type Casting을 통한 GeoJSONify

import geojson

# Read String Array throw .txt File with open() & readlines()
coords = open('210513_ROI_KARI.txt', 'r+', encoding='utf-8').readlines()

idx = 0
for coord in coords:
    coord = coord.split(', ')
    # Type Casting the Coordinates from String to Float
    x1 = float(coord[0])
    y1 = float(coord[1])
    x2 = float(coord[2])
    y2 = float(coord[3])
    geometry = geojson.Polygon(coordinates=[[(x1, y1), (x1, y2), (x2, y2), (x2, y1)]])
    polygon = geojson.Feature(id=None, geometry=geometry)

    aoi = open('AOI_'+str(idx+1)+'.geojson', 'w')
    aoi.write(str(polygon))
    print(polygon)
    aoi.close()
    idx += 1
"""
