# -*- coding: utf-8 -*-
# @File     : satellite.py.py
# @Date     : 2019-09-20
# @Desc     : 卫星数据的读取及建立索引

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

class Satellite(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_df = None
        self.kd_tree = None

    def _load_data(self, from_timestamp, to_timestamp, time_interval):
        '''
        加载数据,一般需要重写
        :param from_timestamp: 开始时间戳
        :param to_timestamp: 结束时间戳
        :param time_interval: 时间间隔
        :return: 是否加载成功.0: 成功; -1: 不成功
        '''
        return 0

    def build_kdtree(self):
        '''
        构建KDTree
        :return: 是否成功
        '''
        if self.data_df is None or len(self.data_df) == 0:
            return -1

        lnglat_arr = np.array([point for point in zip(self.data_df['lng'].values, self.data_df['lat'].values)])
        self.kd_tree = KDTree(lnglat_arr)
        return 0

    def _get_nearest_data(self, lng, lat):
        '''
        获取最近的数据
        :param lng: 经度
        :param lat: 纬度
        :return: tpw值
        '''
        inds = self.kd_tree.query(np.array([lng, lat]).reshape(1, -1), k=1, return_distance=False)
        result = self.data_df.ix[inds[0]]

        nearest_lng = result['lng']
        nearest_lat = result['lat']

        if util.calc_dist(lng, lat, nearest_lng, nearest_lat) > DIST_THRESHOLD:
            return DEFAULT_VALUE

        return result['tpw']