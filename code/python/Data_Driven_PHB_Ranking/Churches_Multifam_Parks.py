#------------------------------------
# Churches_Schools_Multifam_Parks.py
# Creates new Churches, Schools, and Multifamily layers based land_use_inventory, tcad_property and wcad_owner tables
# Additionally creates dissolved Parks layer
# Created by: Jaime McKeown
# Modified on: 1/3/2022
#------------------------------------

# Import modules
import time
print("Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and data layers
sdeWorkspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Maps\\PHB_Pro_Project\\"
sdeLanduse = sdeWorkspace + "gisdm.sde\\PLANNINGCADASTRE.land_use_inventory"
sdeParks = sdeWorkspace + "gisdm.sde\\BOUNDARIES.city_of_austin_parks"
sdeTcad = sdeWorkspace + "gisdm.sde\\EXTERNAL.tcad_property"
sdeWcad = sdeWorkspace + "gisdm.sde\\EXTERNAL.wcad_owner"
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\"

# Set environment to scratch workspace and FGDB
if arcpy.Exists(workspace):
    arcpy.env.scratchWorkspace = workspace
    newDataGdb = arcpy.env.scratchGDB + "\\"
else:
    arcpy.CreateFolder_management("g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\", "Data")
    arcpy.env.scratchWorkspace = workspace
    newDataGdb = arcpy.env.scratchGDB + "\\"

# ***CREATE CHURCHES LAYER***
print("\n" + "Make Feature Layer: Landuse")
arcpy.MakeFeatureLayer_management(sdeLanduse, "sdeLanduseLayer", "LAND_USE = 650", "", "")
print(arcpy.GetMessages())

print("\n" + "Feature Class to Feature Class: Landuse")
arcpy.FeatureClassToFeatureClass_conversion("sdeLanduseLayer", newDataGdb, "Landuse_Meeting_Assembly", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Landuse Meeting Assembly Layer")
arcpy.MakeFeatureLayer_management(newDataGdb + "Landuse_Meeting_Assembly", "Landuse_Meet_Assem_Layer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Add Index: Parcel ID")
arcpy.AddIndex_management("Landuse_Meet_Assem_Layer", ["PARCEL_ID_10"], "landMeetAssemInd", "UNIQUE", "ASCENDING")
print(arcpy.GetMessages())

print("\n" + "Add Field: TCAD Church Name")
arcpy.AddField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_TCAD", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

print("\n" + "Add Field: WCAD Church Name")
arcpy.AddField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_WCAD", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

print("\n" + "Make Table View: TCAD Church View")
arcpy.MakeTableView_management(sdeTcad, "tcadChurchView", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Add Join: Landuse Meeting Assembly Layer to TCAD Church View")
arcpy.AddJoin_management("Landuse_Meet_Assem_Layer", "PARCEL_ID_10", "tcadChurchView", "GEO_ID", "KEEP_ALL")
print(arcpy.GetMessages())

# Codeblock for CHURCH_NAME_TCAD from tcad_parcels
tcadChurchCodeblock = """
def CalcField(Tchurch, Owner):
    if ('APOSTOLIC' in Owner):
        return Owner
    elif ('BIBLE' in Owner):
        return Owner
    elif ('BAPTIST' in Owner):
        return Owner
    elif ('BNAI BRITH HILLEL' in Owner):
        return Owner
    elif ('BUDDHIST' in Owner):
        return Owner
    elif ('CATHEDRAL' in Owner):
        return Owner
    elif ('CATHOLIC' in Owner):
        return Owner
    elif ('CHAPEL' in Owner):
        return Owner
    elif ('CHRIST' in Owner):
        return Owner
    elif ('CHRISTIAN' in Owner):
        return Owner
    elif ('CHURCH') in Owner:
        return Owner
    elif ('CHURCHES' in Owner):
        return Owner
    elif ('CONGREGATION' in Owner):
        return Owner
    elif ('DHARMADHATU' in Owner):
        return Owner
    elif ('DIOS' in Owner):
        return Owner
    elif ('EPISCOPAL' in Owner):
        return Owner
    elif ('EVANGELICAL' in Owner):
        return Owner
    elif ('FAITH' in Owner):
        return Owner
    elif ('FELLOWSHIP' in Owner):
        return Owner
    elif ('FRANCISCAN' in Owner):
        return Owner
    elif ('GOD' in Owner):
        return Owner
    elif ('IGLESIA' in Owner):
        return Owner
    elif ('ISLAMIC' in Owner):
        return Owner
    elif ('JEWISH' in Owner):
        return Owner
    elif ('LA LUZ DEL MUNDO' in Owner):
        return Owner
    elif ('LIFE FAMILY INC' in Owner):
        return Owner
    elif ('LUTHERAN' in Owner):
        return Owner
    elif ('METHODIST' in Owner):
        return Owner
    elif ('MISION' in Owner):
        return Owner
    elif ('MISSION' in Owner):
        return Owner
    elif ('MISSIONARY' in Owner):
        return Owner
    elif ('MOSQUE' in Owner):
        return Owner
    elif ('MOUNT CALVARY PRIMITIVE' in Owner):
        return Owner
    elif ('ORTHODOX' in Owner):
        return Owner
    elif ('PENTECOSTAL' in Owner):
        return Owner
    elif ('PENTECOSTE' in Owner):
        return Owner
    elif ('PRESBYTERIAN' in Owner):
        return Owner
    elif ('PROTESTANT' in Owner):
        return Owner
    elif ('SAINTS' in Owner):
        return Owner
    elif ('SEVENTH DAY ADVENTISTS' in Owner):
        return Owner
    elif ('SHEPHERD' in Owner):
        return Owner
    elif ('ST JOHNS COLLEGE HEIGHTS' in Owner):
        return Owner
    elif ('TARRYTOWN UNITED' in Owner):
        return Owner
    elif ('TEMPLE' in Owner):
        return Owner
    elif ('TEMPLO' in Owner):
        return Owner
    elif ('TEXAS TRANSPORT COMMISSION' in Owner):
        return Owner
    elif ('VICTORY OUTREACH' in Owner):
        return Owner
    elif ('VOX VENIAE' in Owner):
        return Owner
    elif ('WOODROW STUDIOS LLC' in Owner):
        return Owner
    elif ('ZEN CENTER' in Owner):
        return Owner
    else:
        return Tchurch"""


print("\n" + "Calculate Field: TCAD Church Name")
arcpy.CalculateField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_TCAD", "CalcField(!CHURCH_NAME_TCAD!,!PY_OWNER_NAME!)", "PYTHON3", tcadChurchCodeblock)
print(arcpy.GetMessages())

print("\n" + "Remove Join")
arcpy.RemoveJoin_management("Landuse_Meet_Assem_Layer", "")
print(arcpy.GetMessages())

print("\n" + "Make Table View: WCAD Church View")
arcpy.MakeTableView_management(sdeWcad, "wcadChurchView", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Add Join: Landuse Meeting Assembly Layer to WCAD Church View")
arcpy.AddJoin_management("Landuse_Meet_Assem_Layer", "PROPERTY_ID", "wcadChurchView", "PARCEL_NUMBER", "KEEP_COMMON")
print(arcpy.GetMessages())

# Codeblock for CHURCH_NAME_WCAD from wcad_parcels
wcadChurchCodeblock = """
def CalcField(Church, Owner):
    if ('CHURCH' in Owner):
        return Owner
    elif ('CATHOLIC' in Owner):
        return Owner
    elif ('DIOCESE' in Owner):
        return Owner
    elif ('ISLAMIC' in Owner):
        return Owner
    else:
        return Church"""


print("\n" + "Calculate Field: WCAD Church Name")
arcpy.CalculateField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_WCAD", "CalcField(!CHURCH_NAME_WCAD!,!FULL_NAME!)", "PYTHON3", wcadChurchCodeblock)
print(arcpy.GetMessages())

print("\n" + "Remove Join")
arcpy.RemoveJoin_management("Landuse_Meet_Assem_Layer", "")
print(arcpy.GetMessages())

print("\n" + "Feature Class to Feature Class: Churches")
arcpy.FeatureClassToFeatureClass_conversion("Landuse_Meet_Assem_Layer", newDataGdb, "Churches", "CHURCH_NAME_TCAD IS NOT NULL OR CHURCH_NAME_WCAD IS NOT NULL", "", "")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Churches Layer")
arcpy.MakeFeatureLayer_management(newDataGdb + "Churches", "Churches_Layer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Dissolve: Churches Layer")
arcpy.Dissolve_management("Churches_Layer", newDataGdb + "Churches_Dissolve", "", "", "SINGLE_PART", "")
print(arcpy.GetMessages())

# ***CREATE MULTI-FAMILY HOUSING LAYER***
print("\n" + "Make Feature Layer: Landuse")
arcpy.MakeFeatureLayer_management(sdeLanduse, "sdeLanduse3Layer", "LAND_USE = 220 OR LAND_USE = 230 OR LAND_USE = 330", "", "")
print(arcpy.GetMessages())

print("\n" + "Feature Class to Feature Class: Landuse Multifamily")
arcpy.FeatureClassToFeatureClass_conversion("sdeLanduse3Layer", newDataGdb, "Landuse_Multifamily", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Make Feature Layer: Landuse Multifamily Layer")
arcpy.MakeFeatureLayer_management(newDataGdb + "Landuse_Multifamily", "Landuse_Mfamily_Layer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Add Index: Parcel ID")
arcpy.AddIndex_management("Landuse_Mfamily_Layer", ["PARCEL_ID_10"], "landMfamilyInd", "UNIQUE", "ASCENDING")
print(arcpy.GetMessages())

print("\n" + "Add Field: Owner Name")
arcpy.AddField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print(arcpy.GetMessages())

print("\n" + "Make Table View: TCAD Multifamily View")
arcpy.MakeTableView_management(sdeTcad, "tcadMultifamView", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Landuse Multifamily Layer to TCAD Multifamily View")
arcpy.AddJoin_management("Landuse_Mfamily_Layer", "PARCEL_ID_10", "tcadMultifamView", "GEO_ID", "KEEP_COMMON")
print(arcpy.GetMessages())

print("\n" + "Calculate Field: TCAD Owner Name")
arcpy.CalculateField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "!PY_OWNER_NAME!", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Remove Join")
arcpy.RemoveJoin_management("Landuse_Mfamily_Layer", "")
print(arcpy.GetMessages())

print("\n" + "Make Table View WCAD Multifamily View")
arcpy.MakeTableView_management(sdeWcad, "wcadMultifamView", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Add Join: Landuse Multifamily Layer to WCAD Multifamily View")
arcpy.AddJoin_management("Landuse_Mfamily_Layer", "PROPERTY_ID", "wcadMultifamView", "PARCEL_NUMBER", "KEEP_COMMON")
print(arcpy.GetMessages())

print("\n" + "Calculate Field: WCAD Owner Name")
arcpy.CalculateField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "!FULL_NAME!", "PYTHON3", "")
print(arcpy.GetMessages())

print("\n" + "Remove Join")
arcpy.RemoveJoin_management("Landuse_Mfamily_Layer", "")
print(arcpy.GetMessages())

print("\n" + "Dissolve: Multifamily Layer")
arcpy.Dissolve_management("Landuse_Mfamily_Layer", newDataGdb + "Multifamily_Dissolve", ["OWNER_NAME"], "", "", "")
print(arcpy.GetMessages())

# ***CREATE PARKS LAYER***
print("\n" + "Make Feature Layer: Parks Layer")
arcpy.MakeFeatureLayer_management(sdeParks, "sdeParksLayer", "", "", "")
print(arcpy.GetMessages())

print("\n" + "Dissolve: Parks Layer")
arcpy.Dissolve_management("sdeParksLayer", newDataGdb + "Parks_Dissolve", "", "", "SINGLE_PART", "")
print(arcpy.GetMessages())

print("Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
