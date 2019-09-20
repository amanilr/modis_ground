# -- coding:utf-8 --

from fy_3d import FY_3D
from gps1 import GPS1

import pandas as pd
import util


def parse_all(satellite_file_path, ground_file_path, out_file_path):
    ground = GPS1(file_path=ground_file_path)
    satellite = FY_3D(file_path=satellite_file_path)
    file_list = ground._get_file_list()
    result = dict()
    result['year'] = []
    result['month'] = []
    result['day'] = []
    result['hour'] = []
    result['minute'] = []
    result['lon'] = []
    result['lat'] = []
    result['elv'] = []
    result['FY3_TPW'] = []
    result['GPS_TPW'] = []
    for file_name in file_list:
        print 'parsing gps file:', file_name
        timestamp = ground._get_timestamp_from_filename(file_name)
        from_timestamp, to_timestamp, time_interval = \
            ground._get_time_range_from_filename(file_name)
        ret = satellite._load_data(from_timestamp, to_timestamp, time_interval)
        if ret != 0:
            print 'load satellite data error. ret:', ret
            return ret
        df = ground._load_file(file_name)
        if df is None or len(df) == 0:
            print 'load ground data error. empty data.'
            return -1
        for index, row in df.iterrows():
            lng = row['lon']
            lat = row['lat']
            fy3_tpw = satellite._get_nearest_data(lng, lat)
            if fy3_tpw == DEFAULT_VALUE:
                continue

            result['year'].append(util.get_year(timestamp))
            result['month'].append(util.get_month(timestamp))
            result['day'].append(util.get_day(timestamp))
            result['hour'].append(util.get_hour(timestamp))
            result['minute'].append(util.get_minute(timestamp))
            result['lon'].append(lng)
            result['lat'].append(lat)
            result['elv'].append(row['elv'])
            result['FY3_TPW'].append(fy3_tpw)
            result['GPS_TPW'].append(row['PWV'])
    result_df = pd.DataFrame(result)

    print result_df.head(10)
    print out_file_path
    resultDF.to_csv(out_file_path, index=False)

    print('all done')
    return 0

if __name__ == '__main__':
    '''
    if len(sys.argv) != 3:
        print('usage: python main.py [satellite_file_path] [ground_file_path]')
        exit(-1)
    '''

    satellite_file_path = 'G:\\FY-TPW\\FY-3D'
    ground_file_path = 'G:\\Ground-TPW\\GPS\\chinadata\\201908'
    output_file_path = 'G:\\modis_ground\\output\\result.csv'
    res = parse_all(satellite_file_path, ground_file_path, output_file_path)
    if res != 0:
        print('parse all failed.')
        exit(-1)