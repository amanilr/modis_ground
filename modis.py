# -- coding:utf-8 --
import math
import os
import numpy as np
import pandas as pd

from pyhdf.SD import SD, SDC
from pyhdf.error import HDF4Error
from sklearn.neighbors import KDTree
import util

DEFAULT_VALUE = -999999.0
TIME_THRESHOLD = 1800   #时间误差上限30分钟
DIST_THRESHOLD = 10000  #距离误差上限为10km

class Modis(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.time_arr = None
        self.time2dataDF = dict()
        self.time2data_tree = dict()
        self.time2modis_type = dict()
        self.col_num = 0

    def load_data(self):
        if not os.path.isdir(self.file_path):
            print('this is not a directory: ' + self.file_path)
            return -1

        files = os.listdir(self.file_path)
        valid_files = [file for file in files if file.endswith('.hdf')]

        for valid_file in valid_files:
            result = dict()
            file_name = valid_file
            #debug code
            #if '2019152.0610' not in file_name:
            #    continue
            #debug end
            mod_type_fields = file_name.strip().split('_')
            mod_type = mod_type_fields[0][:3]

            date_time_fields = file_name.strip().split('.')
            date_time_str = date_time_fields[1][1:] + '.' + date_time_fields[2]
            timestamp = util.get_timestamp_modis(date_time_str)

            total_file_name = os.path.join(self.file_path, valid_file)
            file = None
            try:
                file = SD(total_file_name)
            except HDF4Error as e:
                print('open file error.', total_file_name)
                continue

            sds_obj1 = file.select('Water_Vapor_Infrared')
            pwv_ir = sds_obj1.get()
            _, n_cols = np.shape(pwv_ir)
            self.col_num = n_cols
            pwv_ir = pwv_ir.flatten()
            sds_obj2 = file.select('Longitude')
            lng = sds_obj2.get().flatten()
            sds_obj3 = file.select('Latitude')
            lat = sds_obj3.get().flatten()

            result['modis_pwv'] = pwv_ir
            result['lng'] = lng
            result['lat'] = lat

            resultDF = pd.DataFrame(result)
            self.time2dataDF[timestamp] = resultDF
            self.time2modis_type[timestamp] = mod_type

        self.time_arr = sorted(self.time2dataDF.keys())
        print("all modis data loaded.")

        return 0

    def build_kdtree(self):
        for timestamp in self.time2dataDF:
            dataDF = self.time2dataDF[timestamp]
            lnglat_arr = np.array([point for point in zip(dataDF['lng'].values, dataDF['lat'].values)])
            lnglat_tree = KDTree(lnglat_arr)
            self.time2data_tree[timestamp] = lnglat_tree

        print('all kdtrees builded.')
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
        index = np.searchsorted(self.time_arr, timestamp)
        if index >= len(self.time_arr):
            index = len(self.time_arr) - 1
        elif index > 0 and math.fabs(self.time_arr[index-1]-timestamp) < math.fabs(self.time_arr[index]-timestamp):
            index -= 1
        nearest_timestamp = self.time_arr[index]

        if math.fabs(nearest_timestamp - timestamp) > TIME_THRESHOLD:
            return DEFAULT_VALUE, DEFAULT_VALUE, ''

        if not self.time2data_tree.has_key(nearest_timestamp):
            print('can not find any timestamp in time2data_tree', nearest_timestamp)
            return DEFAULT_VALUE, DEFAULT_VALUE, ''

        if not self.time2modis_type.has_key(nearest_timestamp):
            print('can not find any timestamp in time2modis_type', nearest_timestamp)
            return DEFAULT_VALUE, DEFAULT_VALUE, ''

        lnglat_tree = self.time2data_tree[nearest_timestamp]
        inds = lnglat_tree.query(np.array([lng, lat]).reshape(1,-1), k=1, return_distance=False)

        modis_type = self.time2modis_type[nearest_timestamp]

        if not self.time2dataDF.has_key(nearest_timestamp):
            print('can not find any timestamp in time2dataDF.', nearest_timestamp)
            return DEFAULT_VALUE, DEFAULT_VALUE, ''

        resultDF = self.time2dataDF[nearest_timestamp]
        resultLine = resultDF.ix[inds[0]]
        nearest_lng = resultLine['lng']
        nearest_lat = resultLine['lat']

        if util.calc_dist(lng, lat, nearest_lng, nearest_lat) > DIST_THRESHOLD:
            return DEFAULT_VALUE, DEFAULT_VALUE, ''

        return resultLine['modis_pwv'].values[0], nearest_timestamp, modis_type

    def _get_col_num(self):
        return self.col_num

if __name__ == '__main__':
    modis = Modis(file_path='/Users/didi/Documents/hjy/MODIS-TPW/')
    res = modis._buid_all()
    if res != 0:
        print("build all fail.")
        exit(-1)