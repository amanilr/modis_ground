# -- coding:utf-8 --

import sys
import modis
import ground

#调用modis的KDTree索引，得到时间和空间上最近的modis值
def get_nearest_nir(x, modis):
    nearest_pwv_nir, _ = modis._get_nearest_data(x['lng'], x['lat'], x['timestamp'])
    return nearest_pwv_nir

def get_neareset_ir(x, modis):
    _, nearest_pwv_ir = modis._get_nearest_data(x['lng'], x['lat'], x['timestamp'])
    return nearest_pwv_ir

def parse_all(modis_file_path, ground_file_path, output_file):
    modis = modis.Modis(file_path=modis_file_path)
    res = modis._buid_all()
    if res != 0:
        print('init modis data failed.')
        return -1

    ground = ground.Ground(file_path=ground_file_path)
    res = ground._load_all()
    if res != 0:
        print('init ground data failed.')
        return -1

    ground_df = ground._get_data()
    ground_df['nearest_nir'] = ground_df.apply(lambda x: get_nearest_nir(x, modis), axis=1)
    ground_df['nearest_ir'] = ground_df.apply(lambda x: get_neareset_ir(x, modis), axis=1)

    print(ground_df.head(10))
    ground_df.to_csv(output_file, index=False)

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: python main.py [modis_file_path] [ground_file_path] [output_file]')
        return -1

    res = parse_all(sys.argv[1], sys.argv[2], sys.argv[3])
    if res != 0:
        print('parse all failed.')
        return -1

    return 0