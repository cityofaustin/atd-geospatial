#------------------------------------
# Demand_Risk_Safety_for_PHBs_ASMP.py
# Runs analysis on input Demand, Risk, and Safety Data for use in Streets_for_PHBs Script processing
# Created by: Jaime McKeown
# Modified on: 10/19/2021
#------------------------------------

# Import modules
import time
print "\n" + "Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

# Set variables for the environment and input data layers
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\PHB_Data.gdb\\"
streetSelect = workspace + "Street_Select_PHB"
largeRetail = workspace + "Large_Retail_Locations_Final"
school = workspace + "Schools"
church = workspace + "Churches_Dissolve"
park = workspace + "Parks_Dissolve"
largeOffice = workspace + "Austin_Major_Employers_Mapping_500"
multifamily = workspace + "Multifamily_Dissolve"
socialService = workspace + "Social_Service_Locations_Final"
publicTrans = workspace + "Streets_PublicTrans_HIN"
hhIncome = workspace + "Block_Group_HH_Income_COA_Dissolve"
popDensity = workspace + "Block_Group_Population_COA"
signalReqPhb = workspace + "Signal_Requests_PHB"
streetlight = workspace + "AE_Streetlights"
signal = workspace + "Signals"
pedCrash = workspace + "Pedestrian_Crashes_SP"


# Working data variables
nearLargeRetail = workspace + "Street_Near_Large_Retail"
nearLargeRetailFreq = workspace + "Street_Near_Large_Retail_Freq"
nearSchool = workspace + "Street_Near_School"
nearSchoolFreq = workspace + "Street_Near_School_Freq"
nearChurch = workspace + "Street_Near_Church"
nearChurchFreq = workspace + "Street_Near_Church_Freq"
nearPark = workspace + "Street_Near_Park"
nearParkFreq = workspace + "Street_Near_Park_Freq"
nearLargeOffice = workspace + "Street_Near_Large_Office"
nearLargeOfficeFreq = workspace + "Street_Near_Large_Office_Freq"
nearMultifamily = workspace + "Street_Near_Multifamily"
nearSocialService = workspace + "Street_Near_Social_Service"
nearSocialServiceFreq = workspace + "Street_Near_Social_Service_Freq"
nearSignalReqPhb = workspace + "Street_Near_Signal_Req_PHB"
nearSignalReqPhbFreq = workspace + "Street_Near_Signal_Req_PHB_Freq"
nearStreetlight = workspace + "Street_Near_Streetlight"
nearSignal = workspace + "Street_Near_Signal"
nearPedCrash2 = workspace + "Street_Near_Ped_Crash_200"
nearPedCrash2Freq = workspace + "Street_Near_Ped_Crash_200_Freq"
nearPedCrash4 = workspace + "Street_Near_Ped_Crash_400"
nearPedCrash4Freq = workspace + "Street_Near_Ped_Crash_400_Freq"

# ***LARGE RETAIL***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, largeRetail, nearLargeRetail, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearLargeRetail, nearLargeRetailFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearLargeRetailFreq, ["IN_FID"], "LargeRetailInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***SCHOOLS***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, school, nearSchool, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearSchool, nearSchoolFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearSchoolFreq, ["IN_FID"], "SchoolInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***CHURCHES***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, church, nearChurch, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearChurch, nearChurchFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearChurchFreq, ["IN_FID"], "ChurchInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***PARKS***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, park, nearPark, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearPark, nearParkFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearParkFreq, ["IN_FID"], "ParkInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***LARGE OFFICE***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, largeOffice, nearLargeOffice, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearLargeOffice, nearLargeOfficeFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearLargeOfficeFreq, ["IN_FID"], "LargeOfficeInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***MULTI-FAMILY HOUSING***
# Generate Near Table, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, multifamily, nearMultifamily, "100 feet", "NO_LOCATION", "NO_ANGLE", "CLOSEST", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearMultifamily, ["IN_FID"], "MultiInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***SOCIAL SERVICES***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, socialService, nearSocialService, "100 feet", "NO_LOCATION", "NO_ANGLE", "ALL", 4, "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearSocialService, nearSocialServiceFreq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearSocialServiceFreq, ["IN_FID"], "SocSerInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***PHB REQUESTS - CSR***
# Generate Near Table, Join Field to Signal_Requests_PHB to get additional fields, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, signalReqPhb, nearSignalReqPhb, "60 feet", "NO_LOCATION", "NO_ANGLE", "ALL", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.MakeTableView_management(nearSignalReqPhb, "nearSignalReqPhbView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.MakeFeatureLayer_management(signalReqPhb, "signalReqPhbLayer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.JoinField_management("nearSignalReqPhbView", "NEAR_FID", "signalReqPhbLayer", "OBJECTID", ["REQUEST_TYPE","REQUEST_STATUS","REQUEST_DATE","REQUEST_SOURCE"])
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearSignalReqPhb, ["IN_FID"], "SignalReqPhbInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***STREETLIGHTS***
# Generate Near Table, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, streetlight, nearStreetlight, "60 feet", "NO_LOCATION", "NO_ANGLE", "CLOSEST", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearStreetlight, ["IN_FID"], "StrlightInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***SIGNALS***
# Generate Near Table, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, signal, nearSignal, "", "NO_LOCATION", "NO_ANGLE", "CLOSEST", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearSignal, ["IN_FID"], "SignalInd", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***PEDESTRIAN CRASHES 200'***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, pedCrash, nearPedCrash2, "200 feet", "NO_LOCATION", "NO_ANGLE", "ALL", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearPedCrash2, nearPedCrash2Freq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearPedCrash2Freq, ["IN_FID"], "PedCrash2Ind", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

# ***PEDESTRIAN CRASHES 400'***
# Generate Near Table, Frequency, Add Index
arcpy.GenerateNearTable_analysis(streetSelect, pedCrash, nearPedCrash4, "400 feet", "NO_LOCATION", "NO_ANGLE", "ALL", "", "PLANAR")
print "\n", arcpy.GetMessages()
arcpy.Frequency_analysis(nearPedCrash4, nearPedCrash4Freq, "IN_FID", "")
print "\n", arcpy.GetMessages()
arcpy.AddIndex_management(nearPedCrash4Freq, ["IN_FID"], "PedCrash4Ind", "UNIQUE", "ASCENDING")
print "\n", arcpy.GetMessages()

print "\n" + "Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
