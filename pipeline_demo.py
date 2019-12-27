# -*- coding: utf-8 -*
import arcpy
import os

keywords = [
		"小学", "中学", "高等院校",
		"地铁站", "公交车站",
		"购物中心", "百货商场", "超市", "集市",
		"综合医院",
		"美术馆", "展览馆", "文化宫", "体育场馆", "健身中心",
		"公司", "园区", "厂矿", "农林园艺",
		"动物园", "风景区", "公园", "休闲广场", "文物古迹", "植物园"
	]
citys = ["郑州市","西安市","宁波市","昆明市",
	"北京市","成都市","大连市","东莞市","广州市",
	"杭州市","合肥市","济南市","南京市","青岛市",
	"厦门市","上海市","深圳市","沈阳市","苏州市",
	"天津市","武汉市","烟台市","长沙市","重庆市"]

source_dir = u'D:\Document\亚太杯\POI\input'
poi_file_list  = [os.path.join(source_dir, x) for x in os.listdir(source_dir)]

arcpy.MakeFeatureLayer_management('D:/Document/HousePricing/excel/中国基础地理要素.gdb/China_perfecture','china')


for city in citys:
    for keyword in keywords:
		# 创建展点图层
        event_layer = arcpy.MakeXYEventLayer_management("D:/Document/亚太杯/POI/input/" + city + '.xlsx/' + keyword + '$','经度','纬度',
        out_layer='test_event',spatial_reference=arcpy.SpatialReference(4326))
		# 获取对应城市
        selection = arcpy.SelectLayerByAttribute_management("china", "NEW_SELECTION", "NAME LIKE '%" + city + "%'")
		# 裁切
        arcpy.Clip_analysis(event_layer,selection,'D:/Document/亚太杯/POI/output/' + city + '/' + keyword +'_clip.shp')
		# 载入裁切后的文件
        arcpy.MakeFeatureLayer_management('D:/Document/亚太杯/POI/output/' + city + '/' + keyword +'_clip.shp','test_clip')
		# 进行筛选
        arcpy.SelectLayerByAttribute_management('test_clip',"NEW_SELECTION","二类 LIKE '%" + keyword + "%'")
		# 保存文件
        arcpy.CopyFeatures_management('test_clip', 'D:/Document/亚太杯/POI/output/' + city + '/' + keyword +'_sel.shp')
		# 删除临时图层
        arcpy.Delete_management('test_event')
        arcpy.Delete_management('test_clip')