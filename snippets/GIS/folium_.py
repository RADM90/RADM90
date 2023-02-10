import folium
from folium import plugins
import time

start_time = time.time()

# ======================================================================================================================
"""
###
### Background Tile
###
"""
# 해양조사원 개방海 오픈API 서비스 키 (민간, http://localhost/)
mapAuthKey = "4BF227C8708FD6DD148E68DBD"
geoInfoAuthKey = "7F44901F325BC0CC036BFE52D"

# Background Tile 셋 정의
map_set = {"BASEMAP_3857": "기본수준면", "BASEMAP_DLENG3857": "영문주기", "BASEMAP_USR3857": "일반사용자",
           "BASEMAP_PERIOD3857": "Only 주기", "BASEMAP_NPERIOD3857": "Else 주기",
           "BASEMAP_TOPO3857": "정사영상 & 해저지형기복도"}

# Folium Map 객체 생성
m = folium.Map(location=[35.1750, 129.1251], tiles='Stamen Toner', zoom_start=13, max_zoom=16, min_zoom=5)

# Map 객체에 Background Tile 수 만큼 Layer 추가
for key, value in map_set.items():
    folium.TileLayer(zoom_start=13, max_zoom=16, min_zoom=5,
                     tiles='http://www.khoa.go.kr/oceanmap/' + mapAuthKey + '/' + key + '/{z}/{y}/{x}/basemapWMTS.do',
                     # name=value + ' (' + key + ')',
                     name=value,
                     attr="<a href='http://www.khoa.go.kr/oceanmap/main.do'>국립해양조사원 개방해</a>").add_to(m)

# ======================================================================================================================
"""
###
### AIS Data
###
import converters.ais2geojson as cvt
import os

ais_layer = folium.FeatureGroup(name='AIS Data of AUG 24th 2020', show=False)

ais_path = 'data/ais'
ais_filename = '!AIVDM.txt'
ais_date = '20200824'
ais_time = '1045'
ais_interpreted = cvt.ais2dict_datetime(ais_path, ais_filename, ais_date, ais_time)
ais_geojson = folium.GeoJson(cvt.dict2geojson(ais_interpreted))
ais_counter = 0
for feature in ais_geojson.data['features']:
    if feature['geometry']['type'] == 'Point':
        tool_tip_text = '<pre>\n'
        for feature_property in feature['properties']:
            tool_tip_text = tool_tip_text + feature_property + ": " + str(
                feature['properties'][feature_property]) + '\n'
        tool_tip_text = tool_tip_text + '\n</pre>'
        tool_tip = folium.Tooltip(tool_tip_text)

        folium.Marker(location=list(reversed(feature['geometry']['coordinates'])),
                      icon=folium.Icon(
                          icon_color='#FFFFFF',
                          icon='ship',
                          prefix='fa'
                      ), tooltip=tool_tip
                      ).add_to(ais_layer)
    ais_counter += 1
ais_layer.add_to(m)


def ais_json_data():
    return ais_geojson


def ais_count_value():
    return ais_counter
"""

# ======================================================================================================================
"""
###
### Ship Detection
###
"""
import test
import geojson
from converters import coordinates as cvt

ship_detection_layer = folium.FeatureGroup(name='Ship Detection Results', show=True)

###### 수신 데이터 형식 변경 시 수정
detected_014534 = test.detected_014535

coordinates_array = [test.detected_014533, test.detected_014534, test.detected_014535]
confidence_level_array = [test.conflev_014533, test.conflev_014534, test.conflev_014535]

####################################
ship_data_collection = []
oldEPSG = 32652
targetEPSG = 4326

# detected_json = open('data/Evaluation/Ship_Detected.json', 'w', encoding='utf-8')
detected_array = []
index = 1
for coord_array, conf_lev_array in zip(coordinates_array, confidence_level_array):
    for coords, conf_lev in zip(coord_array, conf_lev_array):
        y1 = coords[0]
        x1 = coords[1]
        y2 = coords[2]
        x2 = coords[3]

        height = y1 - y2
        width = x2 - x1
        lt = cvt.for_coordinates(oldEPSG, targetEPSG, x1, y1)
        lb = cvt.for_coordinates(oldEPSG, targetEPSG, x1, y2)
        rb = cvt.for_coordinates(oldEPSG, targetEPSG, x2, y2)
        rt = cvt.for_coordinates(oldEPSG, targetEPSG, x2, y1)

        center = cvt.for_coordinates(oldEPSG, targetEPSG, (x1 + x2) / 2, (y1 + y2) / 2)
        detected_array.append(
            {'idx': index, 'lat': round(center[0], 8), 'long': round(center[1], 8), 'confLev': round(conf_lev, 3), "height": height, "width": width})

        polygon_geometry = geojson.Polygon(coordinates=[lt, lb, rb, rt])
        polygon_feature = geojson.Feature(id=None,
                                          geometry=polygon_geometry,
                                          properties={
                                              "name": "Detected Ship",
                                              "stroke": "#FF0000",
                                              "stroke-width": "1",
                                              "stroke-opacity": "1",
                                              "fill": "#FF0000",
                                              "fill-opacity": 0.5})

        ship_data_collection.append(polygon_feature)

        ship_detection_layer.add_child(folium.Marker(location=center,
                                                     icon=folium.DivIcon(
                                                         html=f"""<div style="font-family: monospace; color: white; font-size: 20px; text-shadow: 1px 1px 3px gray;">{index}</div>""")
                                                     ))

        index += 1
ship_feature_collection = geojson.FeatureCollection(ship_data_collection)

# ship_index_layer.add_to(m)

# json.dump(detected_array, detected_json, indent=4)
# detected_json.close()
print(detected_array)

def report_api():
    return detected_array


for feature in ship_feature_collection['features']:
    if feature['geometry']['type'] == 'Polygon':
        folium.Polygon(color=feature['properties']['stroke'],
                       fill=True,
                       locations=list(feature['geometry']['coordinates'])
                       ).add_to(ship_detection_layer)

ship_detection_layer.add_to(m)

"""
###
### Ship Evaluation
###

ship_actual_layer = folium.FeatureGroup(name='Ships (Actual)', show=False)
ship_potential_layer = folium.FeatureGroup(name='Ships (Potential)', show=False)
ship_actual = folium.GeoJson('data/Evaluation/Ship_Actual.geojson', style_function=(lambda x: {'fillColor': '#ff00cc',
                                                                                               'fillOpacity': 0.5,
                                                                                               'color': '#ff00cc',
                                                                                               'weight': 2,
                                                                                               'opacity': 1,
                                                                                               }))

ship_potential = folium.GeoJson('data/Evaluation/Ship_Potential.geojson',
                                style_function=(lambda x: {'fillColor': '#ff9500',
                                                           'fillOpacity': 0.5,
                                                           'color': '#ff9500',
                                                           'weight': 2,
                                                           'opacity': 1,
                                                           }))

ship_actual.add_to(ship_actual_layer)
ship_potential.add_to(ship_potential_layer)

ship_actual_layer.add_to(m)
ship_potential_layer.add_to(m)


def get_actual_num():
    actual_geojson = geojson.load(open('data/Evaluation/Ship_Actual.geojson', encoding='utf-8'))
    num = len(actual_geojson['features'])
    return num


def get_potential_num():
    potential_geojson = geojson.load(open('data/Evaluation/Ship_Potential.geojson', encoding='utf-8'))
    num = len(potential_geojson['features'])
    return num

"""
# Dummy AIS Data // 평가 정보로 활용하기 위해 육안으로 식별한 선박 위치정보를 AIS 라는 명칭으로 대체
eval_layer = folium.FeatureGroup(name='AIS Data', show=False)
eval_014533 = folium.GeoJson('data/Evaluation/014533.geojson')
eval_014534 = folium.GeoJson('data/Evaluation/014534.geojson')
eval_014535 = folium.GeoJson('data/Evaluation/014535.geojson')

eval_array = [eval_014533, eval_014534, eval_014535]
eval_counter = 0
for GeoJSON in eval_array:
    for feature in GeoJSON.data['features']:
        if feature['geometry']['type'] == 'Point':
            folium.Marker(location=list(reversed(feature['geometry']['coordinates'])),
                          icon=folium.Icon(icon_color='#FFFFFF', icon='ship', prefix='fa')
                          ).add_to(eval_layer)
            eval_counter += 1

eval_layer.add_to(m)


def eval_count():
    return eval_counter


# ======================================================================================================================
"""
###
### GeoTiff
###
"""
import rasterio
from rasterio.enums import Resampling
import numpy as np
import os

from skimage import exposure
from image_dehazer import remove_haze


def masking(ndarray):
    mask = np.ndarray(shape=(ndarray.shape[-2], ndarray.shape[-1]), dtype=np.uint8)
    print("mask.shape", mask.shape)

    i = 0
    for items in ndarray[0]:
        j = 0
        for _ in items:
            if ndarray[0][i][j] == 0 & ndarray[1][i][j] == 0 & ndarray[2][i][j] == 0 & ndarray[3][i][j] == 0:
                mask[i][j] = 0
            else:
                mask[i][j] = 255
            j += 1
        i += 1
    return mask


def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()
    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img


def contrast_stretch_mb(img):
    # Loop over RGB bands
    for b in range(0, img.shape[2]):
        p2, p98 = np.percentile(img[:, :, b], (2, 98))
        img_scaled = exposure.rescale_intensity(img, in_range=(p2, p98))
        img[:, :, b] = img_scaled[:, :, b]
    return img


# geotiff_layer = folium.FeatureGroup(name='GeoTIFF Image of 20200824', show=False)
downsample_rate = 2 ** 8
targetEPSG = 4326
img_dir = 'data/SAT_IMG_SRC/20200824/'
file_names = os.listdir(img_dir)
down_scale_factor = 0.5
img_counter = 0

_byte_array = None

# 마스킹 파일을 제외한 영상 파일 중 마스킹 파일이 있을 경우 스태킹 & 마스킹 과정 생략
for file in file_names:
    skip_stacking = False
    skip_masking = False
    skip_stacking_masking = False
    file_name, extension = file.split('.')

    if file_name + '.stk' in file_names:
        skip_stacking = True
    if file_name + '.msk' in file_names:
        skip_masking = True
    if file_name + '.dst' in file_names:
        skip_stacking_masking = True

    # geotiff_layer = folium.FeatureGroup(name=file[9:15], show=False)
    if extension == 'tif':
        img_counter += 1
        img_src = img_dir + file
        dataset = rasterio.open(img_src, 'r+')
        # dataset.MemoryFile()
        # _byte_array = bytearray

        resampled_dataset = dataset.read(
            out_shape=(dataset.count, int(dataset.height * down_scale_factor), int(dataset.width * down_scale_factor)),
            resampling=Resampling.bilinear
        )
        transform = dataset.transform * dataset.transform.scale((dataset.width / dataset.shape[-1]),
                                                                (dataset.height / dataset.shape[-2]))

        if skip_stacking_masking is not True:
            print(file_name + " : Stakinig / Masking 진행")
            if skip_stacking is not True:
                print("Stakinig")
                # b_band, g_band, r_band, nir_band = dataset.read()
                b_band, g_band, r_band, nir_band = resampled_dataset
                src = np.stack([r_band, g_band, b_band], axis=-1)
                src = convert(src, 0, 255, np.uint8)
                src = contrast_stretch_mb(src)
                src = remove_haze(src)
                src.dump(img_dir + file_name + '.stk')
            else:
                print(file_name + " : Stacking 파일 로드")
                src = np.load(img_dir + file_name + '.stk', allow_pickle=True)
            if skip_masking is not True:
                print(file_name + " : Masking")
                # msk = resampled_dataset.read_masks(1)
                # msk = masking(dataset.read(), msk)
                msk = masking(resampled_dataset)
                msk.dump(img_dir + file_name + '.msk')
            else:
                print(file_name + " : Masking 파일 로드")
                msk = np.load(img_dir + file_name + '.msk', allow_pickle=True)
            print("msk.dtype", msk.dtype)
            print("msk.shape", msk.shape)
            print("len(msk)", len(msk))
            print("len(msk[0])", len(msk[0]))
            src = np.dstack([src, msk])
            src.dump(img_dir + file_name + '.dst')
        else:
            print(file_name + " : Stacking / Masking 생략")
            src = np.load(img_dir + file_name + '.dst', allow_pickle=True)

        # 좌표 변환
        top_left, bottom_right = cvt.for_map(dataset, targetEPSG)
        # FeatureGroupLayer 'geotiff'객체에 스택된 레이어 적재
        folium.raster_layers.ImageOverlay(src, bounds=[top_left, bottom_right], name=file[9:15], show=True).add_to(m)


# Map 객체에 geotiff 레이어 추가
# geotiff_layer.add_to(m)


def img_counting():
    return img_counter


import datetime


def img_date():
    datetime_str = file_names[0].split('_')
    date_str = datetime_str[0]
    time_str = datetime_str[1]
    tzinfo = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]), int(time_str[0:2]),
                           int(time_str[2:4]), int(time_str[4:6]), tzinfo=datetime.timezone.utc)
    new_dt = dt.astimezone(tzinfo)
    return new_dt.strftime('%Y / %b / %d')


def get_byte_array():
    return _byte_array


# ======================================================================================================================
"""
###
### Layer Controller & Full Screen Button
###
"""
# Map 객체에 레이어 컨트롤러 부착 (우측 하단)
folium.LayerControl(position='bottomright', collapsed=False, autoZIndex=True).add_to(m)

# Map 객체에 전체화면 버튼 부착 (우측 상단)
plugins.Fullscreen(position='topright', title='Full Screen', title_cancel='Back', force_separate_button=True).add_to(m)
# ======================================================================================================================
"""
###
### Generate Map
###
"""
# Map 객체 저장
m.save('templates/map.html')

end_time = time.time()
print("Operation time :", end_time - start_time)
