# -*- coding: utf-8 -*-
# @File     : fy_3d.py.py
# @Date     : 2019-09-20
# @Desc     : 风云3D数据处理

from satellite import Satellite
import os
import h5py as h5
import numpy as np
import pandas as pd
import struct
import util

ORBIT_PREFIX = '/FY3D_MERSI_ORBT_L2_TPW_MLT_NUL_'
ORBIT_SUFFIX = '_1000M_MS.HDF'
GEO1K_PREFIX = '/FY3D_MERSI_GBAL_L1_'
GEO1K_SUFFIX = '_GEO1K_MS.HDF'

N_ROWS = 2000
N_COLS = 2048
NA_VALUE = 65535

class FY_3D(Satellite):
    def __init__(self, file_path):
        Satellite.__init__(self, file_path)

    def _load_data(self, from_timestamp, to_timestamp, time_interval, lnglat_range):
        '''
        按照起止时间和经纬度范围加载数据
        :param from_timestamp:
        :param to_timestamp:
        :param time_interval:
        :param lnglat_range:
        :return:
        '''
        tpw_file_path = self.file_path + '/ORBIT/'
        lnglat_file_path = self.file_path + '/GEO1K/'
        from_date_str = util.get_timestr(from_timestamp)
        to_date_str = util.get_timestr(to_timestamp)

        #跨天的处理
        if from_date_str != to_date_str:
            split_timestamp = to_timestamp / 86400 * 86400 + 16 * 3600   #第二天0点
            #处理第一天
            for timestamp in range(from_timestamp, split_timestamp, time_interval):
                tpw_file_name = tpw_file_path + from_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + from_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                if not (os.path.exists(tpw_file_name) and os.path.exists(lnglat_file_name)):
                    continue
                print 'loading file:', tpw_file_name, lnglat_file_name
                tpw_data = self.load_file(tpw_file_name, 'MERSI_TPW')
                lng_data = self.load_file(lnglat_file_name, 'Geolocation/Longitude')
                lat_data = self.load_file(lnglat_file_name, 'Geolocation/Latitude')
                result_df = self.get_tpw_df(tpw_data, lng_data, lat_data, lnglat_range)
                self.data_df = pd.concat([self.data_df, result_df]).reset_index(drop=True)

            #处理第二天
            for timestamp in range(split_timestamp, to_timestamp+1, time_interval):
                tpw_file_name = tpw_file_path + to_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + to_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                if not (os.path.exists(tpw_file_name) and os.path.exists(lnglat_file_name)):
                    continue
                print 'loading file:', tpw_file_name, lnglat_file_name
                tpw_data = self.load_file(tpw_file_name, 'MERSI_TPW')
                lng_data = self.load_file(lnglat_file_name, 'Geolocation/Longitude')
                lat_data = self.load_file(lnglat_file_name, 'Geolocation/Latitude')
                result_df = self.get_tpw_df(tpw_data, lng_data, lat_data, lnglat_range)
                self.data_df = pd.concat([self.data_df, result_df]).reset_index(drop=True)
        else:
            for timestamp in range(from_timestamp, to_timestamp+1, time_interval):
                tpw_file_name = tpw_file_path + from_date_str + ORBIT_PREFIX + util.get_datetime_str(
                    timestamp) + ORBIT_SUFFIX
                lnglat_file_name = lnglat_file_path + from_date_str + GEO1K_PREFIX + util.get_datetime_str(
                    timestamp) + GEO1K_SUFFIX
                if not (os.path.exists(tpw_file_name) and os.path.exists(lnglat_file_name)):
                    continue
                print 'loading file:', tpw_file_name, lnglat_file_name
                tpw_data = self.load_file(tpw_file_name, 'MERSI_TPW')
                lng_data = self.load_file(lnglat_file_name, 'Geolocation/Longitude')
                lat_data = self.load_file(lnglat_file_name, 'Geolocation/Latitude')
                result_df = self.get_tpw_df(tpw_data, lng_data, lat_data, lnglat_range)
                self.data_df = pd.concat([self.data_df, result_df]).reset_index(drop=True)

        print 'load fy3d data done.'
        print self.data_df.head(10)
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
        result = np.array([], dtype='float32')

        hdf = h5.File(file_name, 'r')
        if file_type not in ['MERSI_TPW', 'Geolocation/Latitude', 'Geolocation/Longitude']:
            print 'invalid file type:', file_type
            return result

        data = np.array(hdf[file_type])
        n_rows, n_cols = np.shape(data)

        if n_rows != N_ROWS or n_cols != N_COLS:
            print 'data shape error. n_rows:', n_rows, 'n_cols:', n_cols
            return result

        result = data.flatten()

        #经纬度数据要进行大小端转换
        if file_type in ['Geolocation/Latitude', 'Geolocation/Longitude']:
            result = result.byteswap().newbyteorder()
        return result

    def get_tpw_df(self, tpw_data, lng_data, lat_data, lnglat_range):
        result = dict()
        result['tpw'] = tpw_data
        result['lng'] = lng_data
        result['lat'] = lat_data

        result_df = pd.DataFrame(result)
        result_df = self.parse_lnglat_range_and_na(result_df, lnglat_range, NA_VALUE)

        return result_df