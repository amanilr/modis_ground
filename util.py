# -- coding:utf-8 --

import time
from datetime import datetime

def get_timestamp_modis(date_time_str):
    dt = datetime.strptime(date_time_str, "%Y%j.%H%M")
    return long(time.mktime(dt.timetuple()))

def get_timestamp_ground(date_time_str):
    date_time_str = date_time_str[:12]
    dt = datetime.strptime(date_time_str, "%Y%m%d%H%M")
    return long(time.mktime(dt.timetuple()))