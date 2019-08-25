# -- coding:utf-8 --

import os
import pandas as pd
import util

class Ground(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name2df = dict()

    def load_data(self):
        if not os.path.isdir(self.file_path):
            print('this is not a directoy:', self.file_path)
            return -1

        files = os.listdir(self.file_path)
        valid_files = [file for file in files if file.endswith('GPSG_vapor.txt')]
        for valid_file in valid_files:
            file_name = valid_file
            #debug code
            #if '20190601060000' not in file_name:
            #    continue
            #debug end
            file_name_fields = file_name.strip().split("_")
            date_time_field = file_name_fields[4]
            timestamp = util.get_timestamp_ground(date_time_field)

            total_file_name = os.path.join(self.file_path, valid_file)
            f = open(total_file_name)
            line = f.readline()
            line = f.readline()
            line = f.readline()

            file_data = dict()
            file_data['sname'] = []
            file_data['slat'] = []
            file_data['slon'] = []
            file_data['gps_pwv'] = []
            file_data['timestamp'] = []

            for line in f.readlines():
                slines = line.split(" ")
                sname = slines[0]
                gps_pwv = float(slines[9])

                #过滤不符合条件的记录
                if not (sname.startswith('SC') or sname.startswith('XZ')):
                    continue
                if gps_pwv <= 0 or gps_pwv >= 100:
                    continue

                file_data['sname'].append(slines[0])
                file_data['slat'].append(float(slines[2]))
                file_data['slon'].append(float(slines[3]))
                file_data['gps_pwv'].append(float(slines[9]))
                file_data['timestamp'].append(timestamp)

            f.close()
            dataDF = pd.DataFrame(file_data)
            self.file_name2df[total_file_name] = dataDF

        print('all ground data loaded.')
        return 0

    def _get_data(self):
        return self.file_name2df

    def _load_all(self):
        res = self.load_data()
        if res != 0:
            print('load ground data fail.')
            return -1
        return 0