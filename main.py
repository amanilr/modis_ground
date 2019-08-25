# -- coding:utf-8 --

import sys
from modis import Modis, DEFAULT_VALUE
from ground import Ground

import pandas as pd
import util

#调用modis的KDTree索引，得到时间和空间上最近的modis值
'''
def get_neareset_pos(x, modis):
    idx, _ = modis._get_nearest_data(x['lng'], x['lat'], x['timestamp'])
    n_row = idx / modis._get_col_num()
    n_col = idx % modis._get_col_num()
    if idx < 0:
        return (DEFAULT_VALUE, DEFAULT_VALUE)
    return (n_row, n_col)
'''

def get_nearest_data(lng, lat, timestamp, modis):
    modis_pwv, modis_timestamp, modis_type = modis._get_nearest_data(lng, lat, timestamp)
    return modis_pwv, modis_timestamp, modis_type

def parse_all(modis_file_path='F:\\MODIS-TPW', ground_file_path='F:\\Ground-TPW\GPS\data', out_file_path='F:\\Ground-TPW\\GPS\\csv_data\\result.csv'):
    modis = Modis(file_path=modis_file_path)
    res = modis._buid_all()
    if res != 0:
        print('init modis data failed.')
        return -1

    ground = Ground(file_path=ground_file_path)
    res = ground._load_all()
    if res != 0:
        print('init ground data failed.')
        return -1

    file_name2df = ground._get_data()
    result = dict()
    result['sname'] = []
    result['slat'] = []
    result['slon'] = []
    result['gps_year'] = []
    result['gps_month'] = []
    result['gps_day'] = []
    result['gps_hour'] = []
    result['gps_minute'] = []
    result['gps_pwv'] = []
    result['modis_year'] = []
    result['modis_month'] = []
    result['modis_day'] = []
    result['modis_hour'] = []
    result['modis_minute'] = []
    result['modis_pwv'] = []
    result['modis_type'] = []
    for file_name in file_name2df:
        ground_df = file_name2df[file_name]
        for index, row in ground_df.iterrows():
            lng = row['slon']
            lat = row['slat']
            timestamp = row['timestamp']
            modis_pwv, modis_timestamp, modis_type = get_nearest_data(lng, lat, timestamp, modis)
            if modis_pwv == DEFAULT_VALUE:
                continue

            result['sname'].append(row['sname'])
            result['slat'].append(row['slat'])
            result['slon'].append(row['slon'])
            result['gps_year'].append(util.get_year(row['timestamp']))
            result['gps_month'].append(util.get_month(row['timestamp']))
            result['gps_day'].append(util.get_day(row['timestamp']))
            result['gps_hour'].append(util.get_hour(row['timestamp']))
            result['gps_minute'].append(util.get_minute(row['timestamp']))
            result['gps_pwv'].append(row['gps_pwv'])
            result['modis_year'].append(util.get_year(modis_timestamp))
            result['modis_month'].append(util.get_month(modis_timestamp))
            result['modis_day'].append(util.get_day(modis_timestamp))
            result['modis_hour'].append(util.get_hour(modis_timestamp))
            result['modis_minute'].append(util.get_minute(modis_timestamp))
            result['modis_pwv'].append(modis_pwv)
            result['modis_type'].append(modis_type)

    resultDF = pd.DataFrame(result)
    print resultDF.head(10)
    print out_file_path
    resultDF.to_csv(out_file_path, index=False)

    print('all done')
    return 0

if __name__ == '__main__':
    '''
    if len(sys.argv) != 3:
        print('usage: python main.py [modis_file_path] [ground_file_path]')
        exit(-1)
    '''

    res = parse_all()
    if res != 0:
        print('parse all failed.')
        exit(-1)