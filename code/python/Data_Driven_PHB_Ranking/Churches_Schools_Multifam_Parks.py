#------------------------------------
# Churches_Schools_Multifam_Parks.py
# Creates new Churches, Schools, and Multifamily layers based land_use_inventory, tcad_property and wcad_owner tables
# Additionally creates dissolved Parks layer
# Created by: Jaime McKeown
# Modified on: 11/10/2020
#------------------------------------

# Import modules
import time
print "Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and data layers
sdeLanduse = "Database Connections\\GISDM.sde\\PLANNINGCADASTRE.land_use_inventory"
sdeParks = "Database Connections\\GISDM.sde\\BOUNDARIES.city_of_austin_parks"
sdeTcad = "Database Connections\\GISDM_External.sde\\EXTERNAL.tcad_property"
sdeWcad = "Database Connections\\GISDM_External.sde\\EXTERNAL.wcad_owner"
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
# New Landuse layer, Add Index and new fields, Join to tcad/wcad, Calculate, Remove joins, create new churches layer and dissolve
arcpy.MakeFeatureLayer_management(sdeLanduse, "sdeLanduseLayer", "LAND_USE = 650", "", "")
print "\n", arcpy.GetMessages()
arcpy.FeatureClassToFeatureClass_conversion("sdeLanduseLayer", newDataGdb, "Landuse_Meeting_Assembly", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(newDataGdb + "Landuse_Meeting_Assembly", "Landuse_Meet_Assem_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management("Landuse_Meet_Assem_Layer", ["PARCEL_ID_10"], "landMeetAssemInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_TCAD", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_WCAD", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeTcad, "tcadChurchView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Meet_Assem_Layer", "PARCEL_ID_10", "tcadChurchView", "GEO_ID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock for CHURCH_NAME_TCAD from tcad_parcels
tcadChurchCodeblock = """
def CalcField(Tchurch, Owner):
    if 'CHURCH' in Owner:
        return Owner
    elif 'CONGREGATION' in Owner:
        return Owner
    elif 'PRESBYTERIAN' in Owner:
        return Owner
    elif 'GOD' in Owner:
        return Owner
    elif 'LUTHERAN' in Owner:
        return Owner
    elif 'FELLOWSHIP' in Owner:
        return Owner
    elif 'SHEPHERD' in Owner:
        return Owner
    elif 'CATHOLIC' in Owner:
        return Owner
    elif 'BAPTIST' in Owner:
        return Owner
    elif 'APOSTOLIC' in Owner:
        return Owner
    elif 'TEMPLE' in Owner:
        return Owner
    elif 'IGLESIA' in Owner:
        return Owner
    elif 'ORTHODOX' in Owner:
        return Owner
    elif 'ISLAMIC' in Owner:
        return Owner
    elif 'ZEN CENTER' in Owner:
        return Owner
    elif 'VOX VENIAE' in Owner:
        return Owner
    elif 'PENTCOSTES' in Owner:
        return Owner
    elif 'MISSIONARY' in Owner:
        return Owner
    elif 'BUDDHIST' in Owner:
        return Owner
    elif 'FAITH' in Owner:
        return Owner
    elif 'MEHODIST' in Owner:
        return Owner
    elif 'PENTECOSTAL' in Owner:
        return Owner
    elif 'SAINTS' in Owner:
        return Owner
    elif 'DHARMADHATU' in Owner:
        return Owner
    elif 'ST JOHNS COLLEGE HEIGHTS' in Owner:
        return Owner
    elif 'FRANCISCAN' in Owner:
        return Owner
    elif 'TARRYTOWN UNITED' in Owner:
        return Owner
    elif 'EPISCOPAL' in Owner:
        return Owner
    elif 'MISION' in Owner:
        return Owner
    elif 'VICTORY OUTREACH' in Owner:
        return Owner
    elif 'LA LUZ DEL MUNDO' in Owner:
        return Owner
    elif 'JEWISH' in Owner:
        return Owner
    elif 'EVANGELICAL' in Owner:
        return Owner
    elif 'CHRISTIAN' in Owner:
        return Owner
    elif 'CATHEDRAL' in Owner:
        return Owner
    elif 'TEMPLO' in Owner:
        return Owner
    elif 'MISSION' in Owner:
        return Owner
    elif 'BNAI BRITH HILLEL' in Owner:
        return Owner
    elif 'MOUNT CALVARY PRIMITIVE' in Owner:
        return Owner
    elif 'DIOS' in Owner:
        return Owner
    elif 'LIFE FAMILY INC' in Owner:
        return Owner
    elif 'SEVENTH DAY ADVENTISTS' in Owner:
        return Owner
    elif 'CHAPEL' in Owner:
        return Owner
    elif 'MOSQUE' in Owner:
        return Owner
    else:
        return Tchurch"""


arcpy.CalculateField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_TCAD", "CalcField(!CHURCH_NAME_TCAD!,!PY_OWNER_NAME!)", "PYTHON_9.3", tcadChurchCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Meet_Assem_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeWcad, "wcadChurchView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Meet_Assem_Layer", "PROPERTY_ID", "wcadChurchView", "PARCEL_NUMBER", "KEEP_COMMON")
print "\n", arcpy.GetMessages()

# Codeblock for CHURCH_NAME_WCAD from wcad_parcels
wcadChurchCodeblock = """
def CalcField(Church, Owner):
    if 'CHURCH' in Owner:
        return Owner
    elif 'CATHOLIC' in Owner:
        return Owner
    elif 'DIOCESE' in Owner:
        return Owner
    elif 'ISLAMIC' in Owner:
        return Owner
    else:
        return Church"""


arcpy.CalculateField_management("Landuse_Meet_Assem_Layer", "CHURCH_NAME_WCAD", "CalcField(!CHURCH_NAME_WCAD!,!FULL_NAME!)", "PYTHON_9.3", wcadChurchCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Meet_Assem_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.FeatureClassToFeatureClass_conversion("Landuse_Meet_Assem_Layer", newDataGdb, "Churches", "CHURCH_NAME_TCAD IS NOT NULL OR CHURCH_NAME_WCAD IS NOT NULL", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(newDataGdb + "Churches", "Churches_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.Dissolve_management("Churches_Layer", newDataGdb + "Churches_Dissolve", "", "", "SINGLE_PART", "")
print "\n", arcpy.GetMessages()

# ***CREATE SCHOOLS LAYER***
# New Landuse layer, Add Index and new fields, Join to tcad/wcad, Calculate, Remove joins, create new Schools layer and dissolve
arcpy.MakeFeatureLayer_management(sdeLanduse, "sdeLanduse2Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.FeatureClassToFeatureClass_conversion("sdeLanduse2Layer", newDataGdb, "Landuse_Educational", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(newDataGdb + "Landuse_Educational", "Landuse_Educ_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management("Landuse_Educ_Layer", ["PARCEL_ID_10"], "landEducInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("Landuse_Educ_Layer", "SCHOOL_NAME", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeTcad, "tcadSchoolView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Educ_Layer", "PARCEL_ID_10", "tcadSchoolView", "GEO_ID", "KEEP_COMMON")
print "\n", arcpy.GetMessages()

# Codeblock for SCHOOL_NAME from tcad_parcel
tcadSchoolCodeblock = """
def CalcField(School, Owner, PropertyId):
    if Owner == 'AUSTIN CHRISTIAN EDUCATION':
        return Owner
    if Owner == 'AUSTIN COMMUNITY COLLEGE DISTRICT':
        return Owner
    elif Owner == 'AUSTIN INDEPENDENT SCHOOL':
        return Owner
    elif Owner == 'AUSTIN INDEPENDENT SCHOOL DISTRICT':
        return Owner
    elif Owner == 'AUSTIN MONTESSORI SCHOOL INC':
        return Owner
    elif Owner == 'AUSTIN PUBLIC SCHOOLS':
        return Owner
    elif Owner == 'BOARD OF REGENTS OF THE':
        return Owner
    elif Owner == 'BOARD OF REGENTS OF UNIVERSITY OF TEXAS':
        return Owner
    elif Owner == 'CATHOLIC HIGH SCHOOL FOR AUSTI':
        return Owner
    elif Owner == 'CEDARS MONTESSORI SCHOOL INC':
        return Owner
    elif Owner == 'CONCORDIA UNIVERSITY TEXAS':
        return Owner
    elif Owner == 'DEL VALLE I S D':
        return Owner
    elif Owner == 'DEL VALLE INDEPENDENT SCHOOL DISTRICT':
        return Owner
    elif Owner == 'DEL VALLE ISD':
        return Owner
    elif Owner == 'EANES INDEPENDENT SCHOOL DISTRICT':
        return Owner
    elif Owner == 'ESCUELA MONTESSORI DE':
        return Owner
    elif Owner == 'GIRLS SCHOOL OF AUSTIN THE':
        return Owner
    elif Owner == 'HEADWATERS SCHOOL':
        return Owner
    elif Owner == 'HUSTON-TILLOTSON COLLEGE':
        return Owner
    elif Owner == 'IDEA PUBLIC SCHOOLS':
        return Owner
    elif Owner == 'KIRBY CHARTER SCHOOL INC':
        return Owner
    elif Owner == 'LEANDER INDEPENDENT':
        return Owner
    elif Owner == 'LEANDER ISD BOARD OF TRUSTEES':
        return Owner
    elif Owner == 'LEANDER ISD TRUSTEE':
        return Owner
    elif Owner == 'MANOR I S D':
        return Owner
    elif Owner == 'MANOR INDEPENDENT SCHOOL DIST':
        return Owner
    elif Owner == 'MANOR INDEPENDENT SCHOOL DISTRICT':
        return Owner
    elif Owner == 'NYOS CHARTER SCHOOL INC':
        return Owner
    elif Owner == 'PARAGON PREPARATORY INC':
        return Owner
    elif Owner == 'PFLUGERVILLE I S D':
        return Owner
    elif Owner == 'PFLUGERVILLE ISD':
        return Owner
    elif Owner == 'REGENTS SCHOOL OF AUSTIN INC':
        return Owner
    elif Owner == 'ROUND ROCK I S D':
        return Owner
    elif Owner == 'ROUND ROCK INDEPENDENT SCHOOL':
        return Owner
    elif Owner == 'ROUND ROCK ISD':
        return Owner
    elif Owner == 'SOUTHWEST AUSTIN CATHOLIC SCHO':
        return Owner
    elif Owner == 'SOUTHWEST KEY PROGRAM INC':
        return Owner
    elif Owner == 'ST ANDREWS EPISCOPAL SCHOOL':
        return Owner
    elif Owner == 'ST ANDREWS EPISOCPAL SCHOOL INC':
        return Owner
    elif Owner == 'ST EDWARDS UNIVERSITY':
        return Owner
    elif Owner == 'STATE OF TEXAS':
        return Owner
    elif Owner == 'TEXAS LANGUAGE LEARNING ALTERN':
        return Owner
    elif Owner == 'TEXAS PUBLIC FINANCE AUTHORITY':
        return Owner
    elif Owner == 'UNIVERSITY OF TEXAS':
        return Owner
    elif Owner == 'UNIVERSITY OF TEXAS BOARD OF REGENTS':
        return Owner
    elif Owner == 'UNIVERSITY OF TEXAS SYSTEM':
        return Owner
    elif Owner == '4100 RED RIVER HOLDINGS LLC':
        return Owner
    elif PropertyId == '123154':
        return 'ST STEPHENS EPISCOPAL SCHOOL'
    else:
        return School"""


arcpy.CalculateField_management("Landuse_Educ_Layer", "SCHOOL_NAME", "CalcField(!SCHOOL_NAME!,!PY_OWNER_NAME!, !PROPERTY_ID!)", "PYTHON_9.3", tcadSchoolCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Educ_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeWcad, "wcadSchoolView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Educ_Layer", "PROPERTY_ID", "wcadSchoolView", "PARCEL_NUMBER", "KEEP_COMMON")
print "\n", arcpy.GetMessages()

# Codeblock for SCHOOL_NAME from wcad_owner
wcadSchoolCodeblock = """
def CalcField(School, Owner):
    if Owner == 'LEANDER ISD':
        return Owner
    elif Owner == 'LEANDER ISD TRUSTEE':
        return Owner
    elif Owner == 'LEANDER ISD TRUSTEES':
        return Owner
    elif Owner == 'ROUND ROCK ISD':
        return Owner
    elif Owner == 'ROUND ROCK ISD & CITY':
        return Owner
    elif Owner == 'ROUND ROCK ISD TRUSTEE':
        return Owner
    else:
        return School"""


arcpy.CalculateField_management("Landuse_Educ_Layer", "SCHOOL_NAME", "CalcField(!SCHOOL_NAME!, !FULL_NAME!)", "PYTHON_9.3", wcadSchoolCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Educ_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.FeatureClassToFeatureClass_conversion("Landuse_Educ_Layer", newDataGdb, "Schools", "((SCHOOL_NAME IS NOT NULL AND GENERAL_LAND_USE = 600) OR (SCHOOL_NAME IS NOT NULL AND GENERAL_LAND_USE = 800))", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(newDataGdb + "Schools", "Schools_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.Dissolve_management("Schools_Layer", newDataGdb + "Schools_Dissolve", "", "", "SINGLE_PART", "")
print "\n", arcpy.GetMessages()

# ***CREATE MULTI-FAMILY HOUSING LAYER***
# New Landuse layer, Add Index and new fields, Join to tcad/wcad, Calculate, Remove joins, and dissolve
arcpy.MakeFeatureLayer_management(sdeLanduse, "sdeLanduse3Layer", "LAND_USE = 220 OR LAND_USE = 230 OR LAND_USE = 330", "", "")
print "\n", arcpy.GetMessages()
arcpy.FeatureClassToFeatureClass_conversion("sdeLanduse3Layer", newDataGdb, "Landuse_Multifamily", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(newDataGdb + "Landuse_Multifamily", "Landuse_Mfamily_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management("Landuse_Mfamily_Layer", ["PARCEL_ID_10"], "landMfamilyInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()
arcpy.AddField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "TEXT", "", "", 255, "", "NULLABLE", "NON_REQUIRED", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeTcad, "tcadMultifamView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Mfamily_Layer", "PARCEL_ID_10", "tcadMultifamView", "GEO_ID", "KEEP_COMMON")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "!PY_OWNER_NAME!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Mfamily_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(sdeWcad, "wcadMultifamView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("Landuse_Mfamily_Layer", "PROPERTY_ID", "wcadMultifamView", "PARCEL_NUMBER", "KEEP_COMMON")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("Landuse_Mfamily_Layer", "OWNER_NAME", "!FULL_NAME!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("Landuse_Mfamily_Layer", "")
print "\n", arcpy.GetMessages()
arcpy.Dissolve_management("Landuse_Mfamily_Layer", newDataGdb + "Multifamily_Dissolve", ["OWNER_NAME"], "", "", "")
print "\n", arcpy.GetMessages()

# ***CREATE PARKS LAYER***
# Make Feature Layer for BOUNDARIES.city_of_austin_parks and Dissolve
arcpy.MakeFeatureLayer_management(sdeParks, "sdeParksLayer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.Dissolve_management("sdeParksLayer", newDataGdb + "Parks_Dissolve", "", "", "SINGLE_PART", "")
print "\n", arcpy.GetMessages()

print "\n" + "Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
