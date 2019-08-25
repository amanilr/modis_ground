# -- coding:utf-8 --

import os
import pandas as pd

class Ground(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataDF = None

    def load_data(self):
        if not os.path.isdir(path):
            print('this is not a directoy:', self.file_path)
            return -1

        files = os.listdir(self.file_path)
        valid_files = [file for file in files if file.endswith('GPSG_vapor.txt')]
        for valid_file in valid_files:
            file_name = valid_file
            file_name_fields = file_name.strip().split("_")
            date_time_field = file_name_fields[4]
            timestamp = util.get_timestamp_ground(date_time_field)

            total_file_name = os.path.join(file_path, valid_file)
            f = open(total_file_name)
            line = f.readline()
            line = f.readline()
            line = f.readline()

            file_data = dict()
            file_data['sname'] = []
            file_data['sid'] = []
            file_data['lat'] = []
            file_data['lng'] = []
            file_data['elv'] = []
            file_data['P'] = []
            file_data['T'] = []
            file_data['RH'] = []
            file_data['PWV'] = []
            file_data['timestamp'] = []

            for line in f.readlines():
                slines = line.split(" ")
                file_data['sname'].append(slines[0])
                file_data['sid'].append(slines[1])
                file_data['lat'].append(float(slines[2]))
                file_data['lng'].append(float(slines[3]))
                file_data['elv'].append(float(slines[4]))
                file_data['P'].append(float(slines[6]))
                file_data['T'].append(float(slines[7]))
                file_data['RH'].append(float(slines[8]))
                file_data['PWV'].append(float(slines[9]))
                file_data['timestamp'].append(timestamp)
            f.close()

        self.dataDF = pd.DataFrame(file_data)
        return 0

    def _load_all(self):
        res = self.load_data()
        if res != 0:
            print('load all data fail.')
            return -1
        return 0

    def _get_data(self):
        return self.dataDF