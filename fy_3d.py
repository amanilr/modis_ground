# -*- coding: utf-8 -*-
# @File     : fy_3d.py.py
# @Date     : 2019-09-20
# @Desc     : 风云3D数据处理

from satellite import Satellite
import os
import h5py as h5
import numpy as np
import pandas as pd

ORBIT_PREFIX = '/FY3D_MERSI_ORBT_L2_TPW_MLT_NUL_'
ORBIT_SUFFIX = '_1000M_MS.HDF'
GEO1K_PREFIX = '/FY3D_MERSI_GBAL_L1_'
GEO1K_SUFFIX = '_GEO1K_MS.HDF'

N_ROWS = 2000
N_COLS = 2048

class FY_3D(Satellite):
    def __init__(self, file_path):
        Satellite.__init__(self, file_path)

    def _load_data(self, from_timestamp, to_timestamp, time_interval):
        '''
        按照起止时间加载数据
        :param from_timestamp:
        :param to_timestamp:
        :param time_interval:
        :return:
        '''
        tpw_file_path = self.file_path + '/ORBIT/'
        lnglat_file_path = self.file_path + '/GEO1K/'
        from_date_str = util.get_timestr(from_timestamp)
        to_date_str = util.get_timestr(to_timestamp)

        tpw_data = np.array([])
        lng_data = np.array([])
        lat_data = np.array([])
        result = dict()
        #跨天的处理
        if from_date_str != to_date_str:
            split_timestamp = to_timestamp / 86400 * 86400    #第二天0点
            #处理第一天
            for timestamp in range(from_timestamp, split_timestamp+1, time_interval):
                tpw_file_name = tpw_file_path + from_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + from_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                tpw_data.extend(self.load_file(tpw_file_name, 'MERSI_TPW'))
                lng_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Longitude'))
                lat_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Latitude'))

            #处理第二天
            for timestamp in range(split_timestamp, to_timestamp+1, time_interval):
                tpw_file_name = tpw_file_path + to_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + to_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                tpw_data.extend(self.load_file(tpw_file_name, 'MERSI_TPW'))
                lng_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Longitude'))
                lat_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Latitude'))
        else:
            for timestamp in range(from_timestamp, to_timestamp+1, time_interval):
                tpw_file_name = tpw_file_path + from_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + from_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                tpw_data.extend(self.load_file(tpw_file_name, 'MERSI_TPW'))
                lng_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Longitude'))
                lat_data.extend(self.load_file(lnglat_file_name, 'Geolocation/Latitude'))

        result['tpw'] = tpw_data
        result['lng'] = lng_data
        result['lat'] = lat_data
        self.data_df = pd.DataFrame(result)

        print 'load fy3d data done.'
        ret = self.build_kdtree()
        if ret != 0:
            print 'build kdtree error. ret:', ret
            return ret

        print 'build kdtree done.'
        return 0

    def load_file(self, file_name, file_type='MERSI_TPW'):
        '''
        加载FY3D文件
        :param file_name: 文件名
        :param file_type: 文件类型.'MERSI_TPW', 'Geolocation/Latitude', 'Geolocation/Longitude'
        :return: 结果数组
        '''
        result = np.array([])
        if not os.path.exists(file_name):
            print 'file not exist:', file_name
            return result

        hdf = h5.file(file_name, 'r')
        if file_type not in ['MERSI_TPW', 'Geolocation/Latitude', 'Geolocation/Longitude']:
            print 'invalid file type:', file_type
            return result

        data = hdf[file_type]
        n_rows, n_cols = np.shape(data)
        if n_rows != N_ROWS or n_cols != N_COLS:
            print 'data shape error. n_rows:', n_rows, 'n_cols:', n_cols
            return result

        result = data
        return result.flatten()
