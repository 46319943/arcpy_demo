# Make XY Event Layer

import arcpy
arcpy.env.workspace = "C:/data"
# The layer created by this tool is temporary.
# http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/make-xy-event-layer.htm
arcpy.MakeXYEventLayer_management("firestations.dbf", "POINT_X", "POINT_Y", "firestations_points","", "POINT_Z")

