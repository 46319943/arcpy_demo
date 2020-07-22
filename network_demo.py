# encoding: utf-8
import arcpy
import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists
import glob
import traceback
import pickle

# 覆盖SHP不警告
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'D:\Document\ArcMapDemo\AllData\roadnet.gdb'
Origins_folder = r'D:\Document\ArcMapDemo\AllData\RentPrice_Jan'
Destinations_folder = r'D:\Document\ArcMapDemo\AllData\POI'
ODLines_output_folder = r'D:\Document\ArcMapDemo\ODSHP'

if exists('result_list.pkl'):
    with open('result_list.pkl', 'rb') as f:
        result_list = pickle.load(f)
else:
    result_list = []


def add_result(output_filepath):
    result_list.append(output_filepath)
    with open('result_list.pkl', 'wb') as f:
        pickle.dump(result_list, f)


# 要素数据集
datasets = arcpy.ListDatasets()
for dataset in datasets:
    origin_filepath = join(Origins_folder, dataset + '.shp')
    origin_filename = dataset
    print(origin_filepath)

    # 如果所有的Destination都已经计算，则不要构建网络，避免重复运行

    # 构建网络
    network = arcpy.na.BuildNetwork(join(dataset, dataset + '_ND'))

    # 创建OD成本矩阵的分析层
    od = arcpy.na.MakeODCostMatrixLayer(
        network, dataset + 'OD', u'长度', 1200)

    # 将房租点添加到OD的Origins子层
    arcpy.na.AddLocations(od, "Origins",
                          origin_filepath, "Name ID #",
                          '1200 Meters')

    for destination_filepath in glob.glob(join(Destinations_folder, origin_filename, '*.shp')):
        # POI类名
        destination_filename = splitext(basename(destination_filepath))[0]
        print(destination_filepath)

        # 判断是否已经生成shp
        output_filepath = join(ODLines_output_folder,
                               origin_filename + '_' + destination_filename + '.shp')
        if exists(output_filepath) or output_filepath in result_list:
            print('exist')
            continue

        # 判断当前shp文件中，是否存在要素（存在裁剪之后，要素为空的情况）
        if int(arcpy.GetCount_management(destination_filepath).getOutput(0)) == 0:
            print('null feature')
            continue

        # 将POI点添加到OD的Destinations子层，同时覆盖之前的点
        arcpy.na.AddLocations(od, "Destinations",
                              destination_filepath, "",
                              '1200 Meters', append=False)
        try:
            arcpy.na.Solve(od)
        except Exception as e:
            # 没找到解
            if 'ERROR 030212' in e.message:
                print('no solution')
                continue
            # print(e)
            traceback.print_exc()

        # 获取图层组
        odLayerGroup = od.getOutput(0)
        # 按名称生成图层组字典
        subLayers = dict((lyr.datasetName, lyr)
                         for lyr in arcpy.mapping.ListLayers(odLayerGroup)[1:])
        # 获取线状子图层
        lineLayer = subLayers['ODLines']
        # 导出线状图层
        arcpy.management.CopyFeatures(lineLayer, output_filepath)

        # 调用脚本处理生成的OD矩阵SHP
        script_path = r'D:\Document\GeoPython\geopandas\od_matrix_demo.py'
        python_path = r'python'
        script_result = os.system(
            'activate && ' + python_path + ' ' + script_path)
        # 脚本返回结果不为零说明执行失败
        if script_result != 0:
            print('exec script failed')
            continue

        # 处理后，删除shp文件
        arcpy.Delete_management(output_filepath)

        # 记录结果
        add_result(output_filepath)

    # 删除当前房租点生成的OD成本矩阵（其实AddLoc时可以进行Clear，也不用删除）
    arcpy.Delete_management(od)
