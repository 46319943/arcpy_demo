# -*- coding: utf-8 -*
# Python2需要声明源文件编码类型

import arcpy
from arcpy import env

env.workspace = "D:\Document\HousePricing\数据展点——合并\裁切\北京"
arcpy.Copy_management("公司.shp", "D:\Document\公司.shp")