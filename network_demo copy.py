# encoding: utf-8
import arcpy
import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists
import glob

# 覆盖SHP不警告
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'D:\Document\ArcMapDemo\RoadNetwork\roadnet.gdb'
Origins_folder = r'D:\Document\ArcMapDemo\data00_416after\temp\RentPrice_Jan'
Destinations_folder = r'D:\Document\ArcMapDemo\data00_416after\temp\POI'
ODLines_output_folder = r'D:\Document\ArcMapDemo\ODSHP'

# 要素数据集
datasets = arcpy.ListDatasets()
for dataset in datasets:
    origin_filepath = join(Origins_folder, dataset + '.shp')
    origin_filename = dataset

    network = arcpy.na.BuildNetwork(join(dataset, dataset + '_ND'))

    for destination_filepath in glob.glob(join(Destinations_folder, origin_filename, '*.shp')):
        # POI类名
        destination_filename = splitext(basename(destination_filepath))[0]

        od = arcpy.na.MakeODCostMatrixLayer(
            network, dataset + destination_filename + 'OD', u'长度', 1200)
        arcpy.na.AddLocations(od, "Origins",
                              origin_filepath, "Name ID #",
                              '1200 Meters')
        arcpy.na.AddLocations(od, "Destinations",
                              destination_filepath, "",
                              '1200 Meters', append=True)
        arcpy.na.Solve(od)

        odLayerGroup = od.getOutput(0)
        subLayers = dict((lyr.datasetName, lyr)
                         for lyr in arcpy.mapping.ListLayers(odLayerGroup)[1:])
        lineLayer = subLayers['ODLines']
        arcpy.management.CopyFeatures(lineLayer, join(ODLines_output_folder,
                                                      origin_filename + '_' + destination_filename + '.shp'))
        arcpy.Delete_management(od)
