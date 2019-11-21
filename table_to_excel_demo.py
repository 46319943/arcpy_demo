# -*- coding: utf-8 -*
import arcpy
import os

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# arcpy.env.workspace = r"D:\Document\HousePricing"
# os模块的listdir有BUG，不支持中文，需要额外处理，转unicode
source_dir = u"D:\Document\HousePricing\公司"

print(os.listdir(source_dir))

city_dir_list = [os.path.join(source_dir, x) for x in os.listdir(
    source_dir) if os.path.isdir(os.path.join(source_dir, x))]
print(city_dir_list)
for city_dir in city_dir_list:
    try:
        # ArcMap只能导出xls，不能xlsx
        arcpy.TableToExcel_conversion(
            os.path.join(city_dir, u'公司.shp'),
            os.path.join(city_dir, u'公司.xls')
        )
    except Exception as e:
        print(e)
    
