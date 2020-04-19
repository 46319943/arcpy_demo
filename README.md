# csv_poi_to_clipped_shp.py
- 输入：CSV格式保存的房租点、XLS格式保存的POI点，中国各城市区划SHP
- 过程：展点、裁切
- 输出：TEMP目录下，房租点、POI点对应的SHP文件

## 注意事项
- China行政区划
    - Haikou的SHP文件名错误，请手动去掉“Haikou ”最后的空格字符
        - 已在生成词典时去除空格，增强健壮性
    - 缺少Laiwu.shp
        - 去掉三个文件夹中的Laiwu，即去掉Laiwu这个城市
- ResoldPrice_Jan
    - Meizhou.csv，“经度_wgs84”改为“Lon84”
    - Mianyang.csv，“经度_wgs84”改为“Lon84”
    - Nanning.csv，“经度_wgs84”改为“Lon84”
    - Nantong.csv，“经度_wgs84”改为“Lon84”
    - Ningbo.csv，“经度_wgs84”改为“Lon84”
    - Qingdao.csv，“经度_wgs84”改为“Lon84”
    - Shenzhen.csv，“经度_wgs84”改为“Lon84”
    - Suzhou.csv，“经度_wgs84”改为“Lon84”
- POI
    - 有的xls文件中，只有列名，不存在点数据。对于这种情况，会跳过此文件，不生成shp
    - 有的xls文件中，表名不为“Sheet1”，而是对应的POI类型名称。对于这种情况，取第一个表的表名进行处理

## 目录结构
- D:\Document\ArcMapDemo\price_POI_LY（工作空间）
    - China（中国各城市区划SHP）
        - Beijing.shp
        - ...
    - POI（XLS格式保存的POI点）
        - Beijing
            - Agricul.xls
            - ...
        - ...
    - RentPrice_Jan（CSV格式保存的房租点）
        - Beijing.csv
        - ...
    - ResoldPrice_Jan（CSV格式保存的房租点）
        - Beijing.csv
        - ...
    - TEMP（输出目录）
        - POI
        - RentPrice_Jan
        - ResoldPrice_Jan

## 使用方法
### 共同点
- 修改WORKSPACE参数以定位文件路径
### 方法一：在ArcMap中使用
- 打开ArcMap，载入脚本
![](./images/ArcMap_Python.png)
- 使用鼠标移动光标，修改WORKSPACE参数
- 将光标移到最后一行，回车运行

## 方法二：在Python IDE中使用
- 打开Python IDE，如VS Code
- 打开脚本，修改为ArcGIS所安装的Python2.7环境
![](./images/VSC_Python.jpg)
- 同样，修改WORKSPACE参数
- 右键，在终端中运行。或点击右上角绿色三角
- 注意：如果未安装Python拓展，在打开py脚本文件的时候会提示安装。

## 参数说明
### WORKSPACE
> 一般而言，只用设置这个参数即可。即目录结构中对应的工作空间

### TEMP
> 输出目录名称

## 程序入口
- clip_csv
    - 处理CSV数据
- clip_poi
    - 处理POI的XLS数据