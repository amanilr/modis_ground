# -*- coding: utf-8 -*-
# @File     : gps1.py.py
# @Date     : 2019-09-20
# @Desc     : GPS1(中国时区)数据的处理

import os
import pandas as pd
import util

TIME_RANGE = 25 * 60

class GPS1(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def _get_file_list(self):
        if not os.path.isdir(self.file_path):
            print('this is not a directoy:', self.file_path)
            return []
        files = os.listdir(self.file_path)
        valid_files = [file for file in files if file.endswith('GPSG_vapor.txt')]
        return valid_files

    def _get_timestamp_from_filename(self, file_name):
        fields = file_name.strip().split('_')
        datetime_str = fields[4]
        return util.get_timestamp_ground(datetime_str)

    def _get_time_range_from_filename(self, file_name):
        timestamp = self._get_timestamp_from_filename(file_name)
        from_timestamp = timestamp - TIME_RANGE
        to_timestamp = timestamp + TIME_RANGE
        return from_timestamp, to_timestamp, TIME_RANGE

    def _load_file(self, file_name):
        total_file_name = os.path.join(self.file_path, file_name)

        f = open(total_file_name)
        line = f.readline()
        line = f.readline()
        line = f.readline()

        file_data = dict()
        file_data['sname'] = []
        file_data['sid'] = []
        file_data['lat'] = []
        file_data['lon'] = []
        file_data['elv'] = []
        file_data['P'] = []
        file_data['T'] = []
        file_data['RH'] = []
        file_data['PWV'] = []

        for line in f.readlines():
            slines = line.split(" ")

            file_data['sname'].append(slines[0])
            file_data['sid'].append(slines[1])
            file_data['lat'].append(float(slines[2]))
            file_data['lon'].append(float(slines[3]))
            file_data['elv'].append(float(slines[4]))
            file_data['P'].append(float(slines[6]))
            file_data['T'].append(float(slines[7]))
            file_data['RH'].append(float(slines[8]))
            file_data['PWV'].append(float(slines[9]))

        f.close()
        return pd.DataFrame(file_data)
