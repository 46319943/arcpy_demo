# csv_poi_to_clipped_shp.py
- 输入：CSV格式保存的房租点、XLS格式保存的POI点，中国各城市区划SHP
- 过程：展点、裁切
- 输出：TEMP目录下，房租点、POI点对应的SHP文件

## 注意事项
- China目录下，Haikou的SHP文件名错误，请手动去掉“Haikou ”最后的空格字符

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

## WORKSPACE
> 一般而言，只用设置这个参数即可。即目录结构中对应的工作空间

## TEMP
> 输出目录名称