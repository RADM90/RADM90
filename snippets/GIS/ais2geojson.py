from ais import stream
import os
import geojson


def ais2dict(filepath, filename):
    src = os.path.join(filepath, filename)
    ais_raw_data = open(src, 'r', encoding='utf-8').readlines()

    msg_array = []
    decoded = stream.decode(ais_raw_data)
    for msg in decoded:
        msg_array.append(msg)

    return msg_array


def ais2dict_datetime(filepath, filename, acquisition_date=str("YYYY"), acquisition_time=str("HHMM")):
    src = os.path.join(filepath, filename)
    ais_raw_data = open(src, 'r', encoding='utf-8').readlines()  # return list of strings
    ais_raw_data.reverse()

    data_array = []
    timestamp_array = []
    switch = False

    for item in ais_raw_data:
        try:
            if item.startswith(acquisition_date + acquisition_time):
                switch = True
            if switch:
                data_array.append(item)
                # print(item[:14])
                timestamp_array.append(item[:14])
        except:
            print("일시 입력이 올바르지 않습니다.")

    msg_array = []
    decoded = stream.decode(data_array)
    seen = []
    for msg in decoded:
        if msg['mmsi'] not in seen:
            msg_array.append(msg)
            seen.append(msg['mmsi'])

    return msg_array


def dict2geojson(dict_array):
    converted_collection = []
    for item in dict_array:
        keys = item.keys()
        mmsi = str(item['mmsi'])
        sog = None
        if 'sog' in keys:
            sog = format(item['sog'], ".2f")
        longitude = None
        if 'x' in keys:
            longitude = item['x']
        latitude = None
        if 'y' in keys:
            latitude = item['y']
        cog = None
        if 'cog' in keys:
            cog = format(item['cog'], ".1f")
        heading = None
        if 'true_heading' in keys:
            heading = item['true_heading']
            if heading == 511:
                heading = False
        time_stamp = None
        if 'timestamp' in keys:
            time_stamp = item['timestamp']
        if (longitude is not None) | (latitude is not None):
            point_geometry = geojson.Point((longitude, latitude))
            point_feature = geojson.Feature(id=None,
                                            geometry=point_geometry,
                                            properties={
                                                "mmsi": mmsi,
                                                "Speed Over Ground": sog,
                                                "Course Over Ground": cog,
                                                "True Heading": heading,
                                                "Timestamp": time_stamp
                                            })

            converted_collection.append(point_feature)
    feature_collection = geojson.FeatureCollection(converted_collection)
    return feature_collection

