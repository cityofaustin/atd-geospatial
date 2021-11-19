#------------------------------------
# Streets_for_PHBs_ASMP.py
# Creates new ASMP Street Network layer based on specific Street Levels and clips to City of Austin Full Purpose
# Created by: Jaime McKeown
# Modified on: 10/19/2021
#------------------------------------

# Import modules
import time
print("Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and input data layers
sdeConn = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Maps\\PHB_Pro_Project\\gisdm.sde\\"
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

# CREATE STREETS LAYER
print("\n" + "Make Feature Layer: ASMP Street Network Layer")
arcpy.MakeFeatureLayer_management(sdeStreet, "sdeStreetLayer", "EX_XS_GENERAL <> 'DNE'", "", "")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Jurisdictions Layer")
arcpy.MakeFeatureLayer_management(sdeJuris, "sdeJurisLayer", "CITY_NAME = 'CITY OF AUSTIN' AND JURISDICTION_LABEL = 'AUSTIN FULL PURPOSE'", "", "")
print(arcpy.GetMessages())

print("\n" + "Clip: ASMP Street Network to Jurisdictions")
arcpy.Clip_analysis("sdeStreetLayer", "sdeJurisLayer", newDataGdb + "Street_Clip_COA", "")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Streets Clip COA")
arcpy.MakeFeatureLayer_management(streetClip, "streetClipLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Delete Field: Remove fields that are not needed from Streets Clip COA")
arcpy.DeleteField_management("streetClipLayer", ["PROJECT_TYPE_FINAL","PRIORITY_NETWORK","IMPROVEMENT","EXIST_LANES","SIF_XS_GENERAL","ASSUM_LANES_FUT","ROADWAY_POPUP","BICYCLE_FACILITY","REC_BICYCLE_FACILITY","BICYCLE_POPUP","PED_POPUP","PROJECT_DESCRIPTION","MEAN_ROW","MEDIAN_ROW","MIN_ROW","MAX_ROW","REQ_ROW_NUM","REMARKS","SORT_ORDER","CREATED_BY","CREATED_DATE","MODIFIED_BY","MODIFIED_DATE"])
print(arcpy.GetMessages())

print("\n" + "Add Field: Streets Clip COA for Selecting out required streets")
arcpy.AddField_management("streetClipLayer", "PHB_STREET", "TEXT", "", "", 10, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

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


print("\n" + "Calculate Field: PHB_STREET Field on Streets Clip COA")
arcpy.CalculateField_management("streetClipLayer", "PHB_STREET", "CalcField(!NAME!,!STREET_LEVEL!)", "PYTHON3", streetCodeblock)
print(arcpy.GetMessages())

print("\n" + "Select: Records where PHB_STREET field is Yes")
arcpy.Select_analysis("streetClipLayer", newDataGdb + "Street_Select_ASMP", "PHB_STREET = 'Yes'")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Streets Select")
arcpy.MakeFeatureLayer_management(streetSelect, "streetSelectLayer", "", "", "")
print(arcpy.GetMessages())

# TOTAL RANKING SCORES FIELDS
print("\n" + "Add Fields: For Total Ranking Scores on Street Select")
arcpy.AddField_management("streetSelectLayer", "TOTAL_SCORE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "TOTAL_DEMAND", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "TOTAL_RISK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "TOTAL_SAFETY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

# DEMAND CATEGORY FIELDS
print("\n" + "Add Fields: For Demand Category on Streets Select")
arcpy.AddField_management("streetSelectLayer", "LARGE_RETAIL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "SCHOOL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CHURCH", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "PARK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "LARGE_OFFICE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "MULTIFAMILY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "SOCIAL_SERVICE", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "TOTAL_12MAX", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "PUBLIC_TRANS", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "HH_INCOME", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "POP_DENSITY", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CSR", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_DATE", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_TYPE", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_STATUS", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "CSR_REQUEST_SOURCE", "TEXT", "", "", 50, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

# CENSUS DATA FIELD PREP
print("\n" + "Calculate HH_INCOME and POP_DENSITY to 0 (prep for analysis)")
arcpy.CalculateField_management("streetSelectLayer", "HH_INCOME", 0, "", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 0, "", "")
print(arcpy.GetMessages())

# RISK CATEGORY FIELDS
print("\n" + "Add Fields: For Risk Category on Street Select")
arcpy.AddField_management("streetSelectLayer", "TRAVEL_LANES", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "SPEED", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
##arcpy.AddField_management("streetSelectLayer", "SIDEWALK", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "STREET_LIGHT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "SIGNAL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "MEDIAN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

# SAFETY CATEGORY FIELDS
print("\n" + "Add Fields: For Safety Category on Street Select")
arcpy.AddField_management("streetSelectLayer", "PHIN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "BHIN", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "HIN_ALL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_200", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_400", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "PED_CRASH_ALL", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

# ADDITIONAL DATA FIELDS
print("\n" + "Add Fields: For additional data")
arcpy.AddField_management("streetSelectLayer", "COUNCIL_DISTRICT", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "SIGNAL_ENG_AREA", "TEXT", "", "", 20, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())
arcpy.AddField_management("streetSelectLayer", "TRANS_ENG_AREA", "TEXT", "", "", 20, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

# STREETS LAYER TO ASMP POLYGONS
print("\n" + "Make Feature Layer: ASMP Polygons Layer")
arcpy.MakeFeatureLayer_management(asmpPolys, "asmpPolysLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Identity: Between Street Select and ASMP Polygons")
arcpy.Identity_analysis("streetSelectLayer", "asmpPolysLayer", streetSelectPhb, "ONLY_FID", "", "NO_RELATIONSHIPS")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Street Select PHB")
arcpy.MakeFeatureLayer_management(streetSelectPhb, "streetSelectPhbLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Delete Fields: Extra fields that were created from Identity with ASMP Polygons")
arcpy.DeleteField_management("streetSelectPhbLayer", ["FID_Street_Select_ASMP","PHB_STREET","FID_asmp_polygons"])
print(arcpy.GetMessages())

# COUNCIL DISTRICTS
print("\n" + "Make Feature Layer: Council District Layer")
arcpy.MakeFeatureLayer_management(sdeCouncil, "sdeCouncilLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Council District 1")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 1")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 1, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 2")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 2")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 2, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 3")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 3")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 3, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 4")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 4")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 4, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 5")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 5")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 5, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 6")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 6")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 6, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 7")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 7")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 7, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 8")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 8")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 8, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 9")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 9")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 9, "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Council District 10")
arcpy.SelectLayerByAttribute_management("sdeCouncilLayer", "NEW_SELECTION", "COUNCIL_DISTRICT = 10")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeCouncilLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "COUNCIL_DISTRICT", 10, "PYTHON3", "")
print(arcpy.GetMessages())

# SIGNAL ENGINEER AREAS
print("\n" + "Make Feature Layer: Signal Engineer Areas Layer")
arcpy.MakeFeatureLayer_management(sdeSigEng, "sdeSigEngLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Northwest Signal Engineer Area") 
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'NORTHWEST'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"NORTHWEST\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Northeast Signal Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'NORTHEAST'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"NORTHEAST\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Central Signal Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'CENTRAL'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"CENTRAL\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Southwest Signal Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'SOUTHWEST'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"SOUTHWEST\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Southeast Signal Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "NEW_SELECTION", "SIGNAL_ENG_AREA = 'SOUTHEAST'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeSigEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "SIGNAL_ENG_AREA", "\"SOUTHEAST\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Remove Selections")
arcpy.SelectLayerByAttribute_management("sdeSigEngLayer", "CLEAR_SELECTION", "")
print(arcpy.GetMessages())
arcpy.SelectLayerByAttribute_management("streetSelectPhbLayer", "CLEAR_SELECTION", "")
print(arcpy.GetMessages())

# TRANSPORTATION ENGINEERING AREAS
print("\n" + "Make Feature Layer: Transportation Engineering Areas")
arcpy.MakeFeatureLayer_management(sdeTransEng, "sdeTransEngLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "North Transportation Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'NORTH'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"NORTH\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Central Transportation Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'CENTRAL'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"CENTRAL\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "South Transportation Engineer Area")
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "NEW_SELECTION", "ATD_ENGINEER_AREAS = 'SOUTH'")
print(arcpy.GetMessages())
arcpy.SelectLayerByLocation_management("streetSelectPhbLayer", "HAVE_THEIR_CENTER_IN", "sdeTransEngLayer", "", "NEW_SELECTION", "")
print(arcpy.GetMessages())
arcpy.CalculateField_management("streetSelectPhbLayer", "TRANS_ENG_AREA", "\"SOUTH\"", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Remove Selections")
arcpy.SelectLayerByAttribute_management("sdeTransEngLayer", "CLEAR_SELECTION", "")
print(arcpy.GetMessages())
arcpy.SelectLayerByAttribute_management("streetSelectPhbLayer", "CLEAR_SELECTION", "")
print(arcpy.GetMessages())

print("Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
