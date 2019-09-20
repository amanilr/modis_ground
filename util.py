# -- coding:utf-8 --

import math
import time
from datetime import datetime

def get_timestamp_modis(date_time_str):
    dt = datetime.strptime(date_time_str, "%Y%j.%H%M")
    return long(time.mktime(dt.timetuple()))

def get_timestamp_ground(date_time_str):
    date_time_str = date_time_str[:12]
    dt = datetime.strptime(date_time_str, "%Y%m%d%H%M")
    return long(time.mktime(dt.timetuple()))

def get_timestr(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y%m%d')

def calc_dist(xa, ya, xb, yb):
    dist_ratio = 100000
    xa = xa * dist_ratio
    ya = ya * dist_ratio
    xb = xb * dist_ratio
    yb = yb * dist_ratio

    dist = math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
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
