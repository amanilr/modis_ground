# -- coding:utf-8 --

import math
import time
from datetime import datetime

RAD = math.pi / 180.0
EARTH_RADIUS = 6378.137

def get_timestamp_modis(date_time_str):
    dt = datetime.strptime(date_time_str, "%Y%j.%H%M")
    return long(time.mktime(dt.timetuple()))

def get_timestamp_ground(date_time_str):
    date_time_str = date_time_str[:12]
    dt = datetime.strptime(date_time_str, "%Y%m%d%H%M")
    return long(time.mktime(dt.timetuple()))

def get_timestr(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y%m%d')

def get_datetime_str(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M')

def calc_dist(xa, ya, xb, yb):
    dist_ratio = 100000
    xa = xa * dist_ratio
    ya = ya * dist_ratio
    xb = xb * dist_ratio
    yb = yb * dist_ratio

    dist = math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
    return dist

def calc_spherical_dist(from_lng, from_lat, to_lng, to_lat):
    pt1_lat_rad = from_lat * RAD
    pt2_lat_rad = to_lat *RAD
    dlat = from_lat - to_lat
    dlng = from_lng - to_lng
    sin_lat = math.sin(dlat * RAD / 2.0)
    sin_lng = math.sin(dlng * RAD / 2.0)
    cos_lat1 = math.cos(pt1_lat_rad)
    cos_lat2 = math.cos(pt2_lat_rad)
    dist = 2.0 * 1000.0 * math.asin(math.sqrt(sin_lat * sin_lat + cos_lat1 * cos_lat2 * sin_lng * sin_lng)) * EARTH_RADIUS
    return dist

def get_year(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y')

def get_month(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%m')

def get_day(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d')

def get_hour(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H')

def get_minute(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%M')
