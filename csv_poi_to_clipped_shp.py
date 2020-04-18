# -*- coding: utf-8 -*
import os
from os import listdir
from os.path import join, basename, splitext, isfile
import glob
import arcpy

# ArcPy工作路径，之后所有的路径都是这个路径的相对路径
WORKSPACE = r'D:\Document\ArcMapDemo\price_POI_LY'
# arcpy.env.workspace = WORKSPACE

# 行政区划目录
DISTRICT_FOLDER = 'China'
# CSV文件目录
CSV_FOLDER = ['RentPrice_Jan', 'ResoldPrice_Jan']
# POI文件目录
POI_FOLDER = 'POI'

# 临时文件目录
TEMP = 'temp'

# 创建CSV临时目录
for temp in [join(WORKSPACE, TEMP, folder) for folder in CSV_FOLDER]:
    if not os.path.exists(temp):
        os.makedirs(temp)
# 创建POI临时目录
for temp in [join(WORKSPACE, TEMP, POI_FOLDER, folder) for folder in listdir(join(WORKSPACE, POI_FOLDER))]:
    if not os.path.exists(temp):
        os.makedirs(temp)

# 对应X Y坐标字段名称
X_FIELD = 'Lon84'
Y_FIELD = 'Lat84'
X_FIELD_POI = '经度_wgs84'
Y_FIELD_POI = '纬度_wgs84'

# 获取所有SHP文件名及对应路径{Beijing: '...path...'}
feature_paths = {splitext(basename(filepath))[0]: filepath
                 for filepath in glob.glob(join(WORKSPACE, DISTRICT_FOLDER, '*.shp'))}

# 创建WGS84坐标系对象
spatial_ref = arcpy.SpatialReference(4326)

def clip_csv():
    for folder in CSV_FOLDER:
        temp_path = join(WORKSPACE, TEMP, folder)
        for filepath in glob.glob(join(WORKSPACE, folder, '*.csv')):
            
            filename = splitext(basename(filepath))[0]
            print join(temp_path, filename + '.shp')

            arcpy.MakeXYEventLayer_management(
                filepath, X_FIELD, Y_FIELD, filename + 'Event', spatial_ref)

            arcpy.Delete_management(join(temp_path, filename + '.shp'))

            arcpy.Clip_analysis(
                filename + 'Event', feature_paths[filename], join(temp_path, filename + '.shp'))

            arcpy.Delete_management(filename + 'Event')


# 直接保存展点数据的三种方法。后两种在10.3及以下版本存在BUG

# arcpy.FeatureToPoint_management(
#     filename + 'Event', join(temp_path, filename + '.shp'))
# arcpy.DeleteField_management(
#     join(temp_path, filename + '.shp'), 'ORIG_FID')

# arcpy.FeatureClassToFeatureClass_conversion(filename + 'Event', join(WORKSPACE, TEMP), filename)

# arcpy.CopyFeatures_management(filename + 'Event', join(WORKSPACE, TEMP, filename))


def clip_poi():
    for city in listdir(join(WORKSPACE, POI_FOLDER)):
        temp_path=join(WORKSPACE, TEMP, POI_FOLDER, city)
        for filepath in glob.glob(join(WORKSPACE, POI_FOLDER, city, '*.xls*')):

            filename=splitext(basename(filepath))[0]
            print join(temp_path, filename + '.shp')

            arcpy.MakeXYEventLayer_management(
                filepath + '/Sheet1$', X_FIELD_POI, Y_FIELD_POI, filename + 'Event', spatial_ref)

            arcpy.Delete_management(join(temp_path, filename + '.shp'))

            arcpy.Clip_analysis(
                filename + 'Event', feature_paths[city], join(temp_path, filename + '.shp'))

            arcpy.Delete_management(filename + 'Event')


if __name__ == "__main__":
    clip_csv()
    clip_poi()
