# -- coding:utf-8 --

import os
import numpy as np
import pandas as pd

from pyhdf.SD import SD, SDC
from sklearn.neighbors import KDTree
import util

class Modis(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataDF = None
        self.kdtree = None

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
        X = np.array([point for point in zip(df['lng'].values, df['lat'].values, df['timestamp'].values)])
        self.kdtree = KDTree(X)

    def _buid_all(self):
        res = self.load_data()
        if res == -1:
            print("load modis data fail.")
            return -1
        self.build_kdtree()

        return 0

    def _get_nearest_data(lng, lat, timestamp):
        dist, inds = self.kdtree.query(np.array([lng, lat, timestamp]).reshape(1, -1), k=1)
        return self.dataDF.ix[inds[0]]

if __name__ == '__main__':
    modis = Modis(file_path='/Users/didi/Documents/hjy/MODIS-TPW/')
    res = modis._buid_all()
    if res != 0:
        print("build all fail.")
        return -1
    return 0