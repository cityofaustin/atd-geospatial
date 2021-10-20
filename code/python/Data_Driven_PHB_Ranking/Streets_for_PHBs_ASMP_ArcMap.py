#------------------------------------
# Streets_for_PHBs_ASMP.py
# Creates new ASMP Street Network layer based on specific Street Levels and clips to City of Austin Full Purpose
# Created by: Jaime McKeown
# Modified on: 11/10/2020
#------------------------------------

# Import modules
import time
print "Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and input data layers
sdeConn = "Database Connections\\GISDM.sde\\"
sdeStreet = sdeConn + "TRANSPORTATION.asmp_street_network"
sdeJuris = sdeConn + "BOUNDARIES.jurisdictions"
sdeCouncil = sdeConn + "BOUNDARIES.single_member_districts"
sdeSigEng = sdeConn + "TRANSPORTATION.signal_engineer_areas"
sdeTransEng = sdeConn + "TRANSPORTATION.engineering_service_areas"
asmpPolys = "g:\\ATD\\ACTIVE TRANS\\Vision Zero\\GIS\\asmp_polygons\\asmp_polygons.gdb\\asmp_polygons"
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\"

# Set environment to scratch workspace and FGDB
if arcpy.Exists(workspace):
    arcpy.env.scratchWorkspace = workspace
    newDataGdb = arcpy.env.scratchGDB + "\\"
else:
    arcpy.CreateFolder_management("g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\", "Data")
    arcpy.env.scratchWorkspace = workspace
    newDataGdb = arcpy.env.scratchGDB + "\\"

# Working data variables
streetClip = newDataGdb + "Street_Clip_COA"
streetSelect = newDataGdb + "Street_Select_ASMP"
streetSelectPhb = newDataGdb + "Street_Select_PHB"

# Make Feature Layer for TRANSPORTATION.asmp_street_network
arcpy.MakeFeatureLayer_management(sdeStreet, "sdeStreetLayer", "EX_XS_GENERAL <> 'DNE'", "", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer for BOUNDARIES.jurisdictions
arcpy.MakeFeatureLayer_management(sdeJuris, "sdeJurisLayer", "CITY_NAME = 'CITY OF AUSTIN' AND JURISDICTION_LABEL = 'AUSTIN FULL PURPOSE'", "", "")
print "\n", arcpy.GetMessages()

# Clip asmp_street_network to jurisdictions
arcpy.Clip_analysis("sdeStreetLayer", "sdeJurisLayer", newDataGdb + "Street_Clip_COA", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer for Street_Clip_COA
arcpy.MakeFeatureLayer_management(streetClip, "streetClipLayer", "", "", "")
print "\n", arcpy.GetMessages()

# Delete Fields that are not needed from ASMP Street Network
arcpy.DeleteField_management("streetClipLayer", ["PROJECT_TYPE_FINAL","PRIORITY_NETWORK","IMPROVEMENT","EXIST_LANES","SIF_XS_GENERAL","ASSUM_LANES_FUT","ROADWAY_POPUP","BICYCLE_FACILITY","REC_BICYCLE_FACILITY","BICYCLE_POPUP","PED_POPUP","PROJECT_DESCRIPTION","MEAN_ROW","MEDIAN_ROW","MIN_ROW","MAX_ROW","REQ_ROW_NUM","REMARKS","SORT_ORDER","CREATED_BY","CREATED_DATE","MODIFIED_BY","MODIFIED_DATE"])
print "\n", arcpy.GetMessages()

# Add new field to Street_Clip_COA for Selecting out required streets
arcpy.AddField_management("streetClipLayer", "PHB_STREET", "TEXT", "", "", 10, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()

# Codeblock for PHB_STREET field from Street_Clip_COA
# Added Street Level 1 to the Streets Layer per Renee on 11/10/2020
streetCodeblock = """
def CalcField(StreetName, StreetLevel):
    if StreetLevel == 5:
        return 'No'
    elif 'SVRD' in StreetName:
        return 'No'
    elif 'RAMP' in StreetName:
        return 'No'
    elif 'MOPAC' in StreetName:
        return 'No'
    elif 'SH 45' in StreetName:
        return 'No'
    elif StreetLevel == 1:
        return 'Yes'
    elif StreetLevel == 2:
        return 'Yes'
    elif StreetLevel == 3:
        return 'Yes'
    elif StreetLevel == 4:
        return 'Yes'
    else:
        return 'No'"""


# Calculate PHB_STREET Field on Street_Clip_COA
arcpy.CalculateField_management("streetClipLayer", "PHB_STREET", "CalcField(!NAME!,!STREET_LEVEL!)", "PYTHON_9.3", streetCodeblock)
print "\n", arcpy.GetMessages()

# Select records where PHB_STREET field is Yes
arcpy.Select_analysis("streetClipLayer", newDataGdb + "Street_Select_ASMP", "PHB_STREET = 'Yes'")
print "\n", arcpy.GetMessages()

# Make Feature Layer for Streets_Select_PHB
arcpy.MakeFeatureLayer_management(streetSelect, "streetSelectLayer", "", "", "")
print "\n", arcpy.GetMessages()

# Add Fields for Total Ranking Scores on Street_Select_PHB
arcpy.AddField_management("streetSelectLayer", "TOTAL_SCORE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "TOTAL_DEMAND", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "TOTAL_RISK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "TOTAL_SAFETY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()

# Add Fields for Demand Category on Streets_Select_PHB
arcpy.AddField_management("streetSelectLayer", "LARGE_RETAIL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "SCHOOL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CHURCH", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "PARK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "LARGE_OFFICE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "MULTIFAMILY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "SOCIAL_SERVICE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "TOTAL_12MAX", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "PUBLIC_TRANS", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "HH_INCOME", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "POP_DENSITY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CSR", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_DATE", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_TYPE", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_STATUS", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_SOURCE", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()


# Calculate HH_INCOME and POP_DENSITY to 0 (prep for analysis)
arcpy.CalculateField_management("streetSelectLayer", "HH_INCOME", 0, "", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 0, "", "")
print "\n", arcpy.GetMessages()

# Add Fields for Risk Category on Street_Select_PHB
arcpy.AddField_management("streetSelectLayer", "TRAVEL_LANES", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "SPEED", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
##arcpy.AddField_management("streetSelectLayer", "SIDEWALK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "STREET_LIGHT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "SIGNAL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "MEDIAN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()

# Add Fields for Safety Category on Street_Select_PHB
arcpy.AddField_management("streetSelectLayer", "PHIN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "BHIN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "HIN_ALL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_200", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_400", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_ALL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()

# Add Fields for additional data
arcpy.AddField_management("streetSelectLayer", "COUNCIL_DISTRICT", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "SIGNAL_ENG_AREA", "TEXT", "", "", 20, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("streetSelectLayer", "TRANS_ENG_AREA", "TEXT", "", "", 20, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer for asmp_polygons layer
arcpy.MakeFeatureLayer_management(asmpPolys, "asmpPolysLayer", "", "", "")
print "\n", arcpy.GetMessages()

# Identity between Street_Select_PHB and asmp_polygons
arcpy.Identity_analysis("streetSelectLayer", "asmpPolysLayer", streetSelectPhb, "ONLY_FID", "", "NO_RELATIONSHIPS")
print "\n", arcpy.GetMessages()

# Make Feature Layer for Street_Select_PHB
arcpy.MakeFeatureLayer_management(streetSelectPhb, "streetSelectPhbLayer", "", "", "")
print "\n", arcpy.GetMessages()

# Delete extra field that was created from Identity with asmp_polygons
arcpy.DeleteField_management("streetSelectPhbLayer", ["FID_Street_Select_ASMP","PHB_STREET","FID_asmp_polygons"])
print "\n", arcpy.GetMessages()

# ***COUNCIL_DISTRICT***
# Make Feature Layer, Select Layer by Attributes, Select Layer by Location, Calculate
arcpy.MakeFeatureLayer_management(sdeCouncil, "sdeCouncilLayer", "", "", "")
print "\n", arcpy.GetMessages()
# Council District 1
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 1")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 1, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 2
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 2")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 2, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 3
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 3")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 3, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 4
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 4")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 4, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 5
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 5")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 5, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 6
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 6")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 6, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 7
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 7")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 7, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 8
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 8")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 8, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 9
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 9")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 9, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Council District 10
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 10")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 10, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# ***SIGNAL_ENG_AREA***
# Make Feature Layer, Select Layer by Attributes, Select Layer by Location, Calculate, Clear Selections
arcpy.MakeFeatureLayer_management(sdeSigEng, "sdeSigEngLayer", "", "", "")
print "\n", arcpy.GetMessages()
# Northwest Signal Engineer Area
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'NORTHWEST'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"NORTHWEST\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Northeast Signal Engineer Area
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'NORTHEAST'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"NORTHEAST\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Central Signal Engineer Area
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'CENTRAL'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"CENTRAL\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Southwest Signal Engineer Area
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'SOUTHWEST'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"SOUTHWEST\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Southeast Signal Engineer Area
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'SOUTHEAST'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"SOUTHEAST\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectPhbLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# ***TRANS_ENG_AREA***
# Make Feature Layer, Select Layer by Attributes, Select Layer by Location, Calculate, Clear Selections
arcpy.MakeFeatureLayer_management(sdeTransEng, "sdeTransEngLayer", "", "", "")
print "\n", arcpy.GetMessages()
# North Transportation Engineer Area
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'NORTH'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"NORTH\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# Central Transportation Engineer Area
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'CENTRAL'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"CENTRAL\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
# South Transportation Engineer Area
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'SOUTH'")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"SOUTH\"", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectPhbLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

print "\n" + "Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
