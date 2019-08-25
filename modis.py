# -- coding:utf-8 --

import os
import numpy as np
import pandas as pd

from pyhdf.SD import SD, SDC
from sklearn.neighbors import KDTree
import util

DEFAULT_VALUE = -999999.0

class Modis(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataDF = None
        self.time_arr = None
        self.time_tree = None
        self.time2lnglat_arr = dict()
        self.time2lnglat_tree = dict()

    def load_data(self):
        if not os.path.isdir(self.file_path):
            print('this is not a directory: ' + self.file_path)
            return -1

        files = os.listdir(self.file_path)
        valid_files = [file for file in files if file.endswith('.hdf')]
        result = dict()
        result['timestamp'] = []
        result['pwv_nir'] = []
        result['pwr_ir'] = []
        result['lat'] = []
        result['lng'] = []
        for valid_file in valid_files:
            file_name = valid_file
            date_time_fields = file_name.strip().split('.')
            date_time_str = date_time_fields[1][1:] + '.' + date_time_fields[2]
            timestamp = util.get_timestamp_modis(date_time_str)

            total_file_name = os.path.join(file_path, valid_file)
            file = SD(total_file_name)
            sds_obj1 = file.select('Water_Vapor_Near_Infrared')
            pwv_nir = sds_obj1.get()
            sds_obj2 = file.select('Water_Vapor_Infrared')
            pwv_ir = sds_obj2.get()
            sds_obj3 = file.select('Latitude')
            lat = sds_obj3.get()
            sds_obj4 = file.select('Longitude')
            lng = sds_obj4.get()

            result['timestamp'] += ([timestamp] * len(pwv_nir))
            result['pwv_nir'] += pwv_nir
            result['pwv_ir'] += pwv_ir
            result['lat'] += lat
            result['lng'] += lng

        self.dataDF = pd.DataFrame(result)
        return 0

    def build_kdtree(self):
        self.time_arr = self.dataDF['timestamp'].drop_duplicates().values
        self.time_tree = KDTree(self.time_arr)

        for timestamp in self.time_arr:
            timeDataDF = self.dataDF[self.dataDF['timestamp'] == timestamp]
            lnglat_arr = np.array([point for point in zip(timeDataDF['lng'].values, timeDataDF['lat'].values)])
            lnglat_tree = KDTree(lnglat_arr)
            self.time2lnglat_tree[timestamp] = lnglat_tree
            self.time2lnglat_arr[timestamp] = lnglat_arr

        return 0

    def _buid_all(self):
        res = self.load_data()
        if res != 0:
            print("load modis data fail.")
            return -1
        res = self.build_kdtree()
        if res != 0:
            print("build kdtree fail.")
            return -1

        return 0

    def _get_nearest_data(self, lng, lat, timestamp):
        inds = self.time_tree.query(np.array([timestamp]), k=1, return_distance=False)
        nearest_timestamp = self.time_arr[inds[0]]

        if not self.time2lnglat_tree.has_key(nearest_timestamp):
            print('can not find any timestamp:', timestamp)
            return DEFAULT_VALUE, DEFAULT_VALUE

        lnglat_tree = self.time2lnglat_tree[nearest_timestamp]
        lnglat_arr = self.time2lnglat_arr[nearest_timestamp]
        inds = lnglat_tree.query(np.array([lng, lat]).reshape(1,-1), k=1, return_distance=False)
        nearest_point = lnglat_arr[inds[0]]

        resultDF = self.dataDF[(self.dataDF['timestamp']==nearest_timestamp) \
                    & (self.dataDF['lng']==nearest_point[0]) \
                    & (self.dataDF['lat']==nearest_point[1])]

        if len(resultDF) != 1:
            print('the nearest data is more than 1.')
            return DEFAULT_VALUE, DEFAULT_VALUE

        return resultDF.ix[0]['pwv_nir'], resultDF.ix[0]['pwv_ir']

if __name__ == '__main__':
    modis = Modis(file_path='/Users/didi/Documents/hjy/MODIS-TPW/')
    res = modis._buid_all()
    if res != 0:
        print("build all fail.")
        return -1
    return 0