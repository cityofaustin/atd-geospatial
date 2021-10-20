#------------------------------------
# Data_to_PHB_Data.py
# Creates new ASMP Street Network layer based on specific Street Levels and clips to City of Austin Full Purpose
# Created by: Jaime McKeown
# Modified on: 12/10/2020
#------------------------------------

# Import modules
import time
print "Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and input data layers
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\"
scratchGdb = workspace + "scratch.gdb\\"
dataCollGdb = workspace + "Data_Collection.gdb\\"
phbDataGdb = workspace + "PHB_Data.gdb\\"

# If FGDB exists, delete and recreate, if not create FGDB
if arcpy.Exists(phbDataGdb):
    arcpy.Delete_management(phbDataGdb, "")
    print "\n", arcpy.GetMessages()
    arcpy.CreateFileGDB_management(workspace, "PHB_Data.gdb", "CURRENT")
    print "\n", arcpy.GetMessages()

else:
    arcpy.CreateFileGDB_management(workspace, "PHB_Data.gdb", "CURRENT")
    print "\n", arcpy.GetMessages()

# Copy Features from scratch FGDB to PHB_Data FGDB
arcpy.MakeFeatureLayer_management(scratchGdb + "Churches_Dissolve", "Church_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Church_Layer", phbDataGdb + "Churches_Dissolve", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(scratchGdb + "Multifamily_Dissolve", "Multifamily_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Multifamily_Layer", phbDataGdb + "Multifamily_Dissolve", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(scratchGdb + "Parks_Dissolve", "Park_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Park_Layer", phbDataGdb + "Parks_Dissolve", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(scratchGdb + "Street_Select_PHB", "Street_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Street_Layer", phbDataGdb + "Street_Select_PHB", "", "", "", "")
print "\n", arcpy.GetMessages()

# Copy Features from Data_Collection FGDB to PHB_Data FGDB
arcpy.MakeFeatureLayer_management(dataCollGdb + "AE_Streetlights", "Streetlight_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Streetlight_Layer", phbDataGdb + "AE_Streetlights", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "ASMP_Street_Public_Trans_HIN", "Asmp_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Asmp_Layer", phbDataGdb + "ASMP_Street_Public_Trans_HIN", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Austin_Major_Employers_Mapping_500", "Employer_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Employer_Layer", phbDataGdb + "Austin_Major_Employers_Mapping_500", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Block_Group_HH_Income_COA_Dissolve", "Income_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Income_Layer", phbDataGdb + "Block_Group_HH_Income_COA_Dissolve", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Block_Group_Population_COA_Dissolve", "Population_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Population_Layer", phbDataGdb + "Block_Group_Population_COA_Dissolve", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Large_Retail_Locations_Final", "Retail_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Retail_Layer", phbDataGdb + "Large_Retail_Locations_Final", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Schools", "Schools_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Schools_Layer", phbDataGdb + "Schools", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Pedestrian_Crashes_SP", "Ped_Crash_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Ped_Crash_Layer", phbDataGdb + "Pedestrian_Crashes_SP", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Signal_Requests_PHB", "Signal_Req_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Signal_Req_Layer", phbDataGdb + "Signal_Requests_PHB", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Signals", "Signals_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Signals_Layer", phbDataGdb + "Signals", "", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(dataCollGdb + "Social_Service_Locations_Final", "Social_Service_Layer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.CopyFeatures_management("Social_Service_Layer", phbDataGdb + "Social_Service_Locations_Final", "", "", "", "")
print "\n", arcpy.GetMessages()

print "\n" + "Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
