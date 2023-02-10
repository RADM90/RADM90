import pandas as pd
import json
import geojson

DATA_PATH = "data/BusanVTS"


df = pd.read_csv(f'{DATA_PATH}/BusanVTS.csv')
cols = df.columns

area_names = df['NAME'].unique()

# print(area_names)
print(cols)
# print(df)
item_arr = []
for name in area_names:
    items = df['NAME'] == name
    item_arr.append(df[items])

feature_coll_arr = []
for item in item_arr:
    item_name = item[item['SERIAL'] == 1]['NAME'].item()
    coords_arr = []
    item_length = len(item)
    for i in range(item_length):
        # coords_arr.append(item['SERIAL'] == i)
        idx_loc = item['SERIAL'] == i+1
        lat_decimal = float(item[idx_loc]['LAT_DECIMAL'])
        lon_decimal = float(item[idx_loc]['LON_DECIMAL'])
        coords_arr.append((lon_decimal, lat_decimal))
    origin_item = item['SERIAL'] == 1
    lat_origin = float(item[origin_item]['LAT_DECIMAL'])
    lon_origin = float(item[origin_item]['LON_DECIMAL'])
    if item_length != 1:
        coords_arr.append((lon_origin, lat_origin))
        poloygon = geojson.Polygon(coordinates=[coords_arr])
        gj = geojson.Feature(geometry=poloygon, properties={"areaName": item_name})
        # with open(item_name+'.geojson', 'w+') as f:
        #     geojson.dump(gj, f)
        feature_coll_arr.append(gj)
    elif item_length == 1:
        point = geojson.Point((lon_origin, lat_origin))
        gj = geojson.Feature(geometry=point, properties={"areaName": item_name})
        feature_coll_arr.append(gj)
    print(coords_arr)


with open(f'{DATA_PATH}/BusanVTS_All.geojson', 'w+') as f:
    geojson.dump(geojson.FeatureCollection(feature_coll_arr), f)
