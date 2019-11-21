# -*- coding: utf-8 -*
import arcpy
from arcpy import env

env.workspace = r"D:\Document\HousePricing"
arcpy.MakeFeatureLayer_management('excel/中国基础地理要素.gdb/China_perfecture','china')
selection = arcpy.SelectLayerByAttribute_management("china", "NEW_SELECTION", "NAME LIKE '%北京%'")
print(selection)
for row in arcpy.SearchCursor(selection):
    print(row.NAME)
# arcpy.Clip_analysis('POI',selection,'output_file')