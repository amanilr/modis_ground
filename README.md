# FY3_ground
根据真值找到对应的FY3值
1、数据存放目录：
FY-3D:
1)TPW数据：G:\FY-TPW\FY-3D\ORBIT
2）经纬度数据：G:\FY-TPW\FY-3D\GEO1K
GPS1:G:\Ground-TPW\GPS\chinadata
GPS2:G:\Ground-TPW\GPS\SUOMINET\data

2、FY-3D数据集：
1）TPW数据：sds='MERSI_TPW'                 [2000,2048]
2) 经纬度数据：sds='Geolocation/Latitude'   [2000,2048]
              sds='Geolocation/Longitude'  [2000,2048]
3）读取程序：
import h5py as h5
hdf=h5.File(fname,"r")
TPW=hdf[sds]

3、GPS数据：
1）GPS1数据：
  整点数据，如01,02,03时次
  匹配卫星时次：
  如对于01时，卫星匹配时间块数据为0035，0040,0045,0050,0055,0100,0105,0110,0115，0120,0125
2）GPS2数据：
  15分，45分数据，每个文件中同一个站点有两个数据
  匹配卫星时次：
  如对于01时
  15分：0100 0105 0110 0115 0120 0125
  45分：0130 0135 0140 0145 0150 0155
3）读取程序
import readGPS
#读GPS1数据（中国地区）
sname,sid,slat,slon,elv,P,T,RH,PWV=readGPS.getGPSG(fgpath)
#读GPS2数据（北美地区）
sname,YY,MT,DD,HH,MI,lat,lon,elv,PWV=readGPS.getSUOh(fpname)

4、结果存放文件：
年 月 日 时 分 经度 纬度 高程 FY3_TPW GPS_TPW



 

