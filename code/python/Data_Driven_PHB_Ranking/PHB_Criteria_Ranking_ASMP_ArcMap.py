#------------------------------------
# PHB_Criteria_Ranking_ASMP.py
# Processes all the data inputs to populate the ranking for all ASMP street segments in Street_for_PHBs layer
# Created by: Jaime McKeown
# Modified on: 11/10/2020
#------------------------------------

# Import modules
import time
print "Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = True

# Set variables for the environment and input data layers
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\PHB_Data.gdb\\"

# Working data variables
streetSelect = workspace + "Street_Select_PHB"
streetSelectFinal = workspace + "Street_Select_PHB_Final"
# Demand, Risk, Safety
nearLargeRetailFreq = workspace + "Street_Near_Large_Retail_Freq"
nearSchoolFreq = workspace + "Street_Near_School_Freq"
nearChurchFreq = workspace + "Street_Near_Church_Freq"
nearParkFreq = workspace + "Street_Near_Park_Freq"
nearLargeOfficeFreq = workspace + "Street_Near_Large_Office_Freq"
nearMultifamily = workspace + "Street_Near_Multifamily"
nearSocialServiceFreq = workspace + "Street_Near_Social_Service_Freq"
publicTransHin = workspace + "ASMP_Street_Public_Trans_HIN"
hhIncome = workspace + "Block_Group_HH_Income_COA_Dissolve"
popDensity = workspace + "Block_Group_Population_COA_Dissolve"
nearSignalReqPhb = workspace + "Street_Near_Signal_Req_PHB"
nearStreetlight = workspace + "Street_Near_Streetlight"
nearSignal = workspace + "Street_Near_Signal"
nearPedCrash2Freq = workspace + "Street_Near_Ped_Crash_200_Freq"
nearPedCrash4Freq = workspace + "Street_Near_Ped_Crash_400_Freq"

# Make Feature Layer for Street_Select_PHB
arcpy.MakeFeatureLayer_management(streetSelect, "streetSelectLayer", "", "", "")
print "\n", arcpy.GetMessages()

# ***DEMAND CRITERIA***
#----------------------
# Codeblock for calculating Demand fields that sum up to 12 points maximum
max12Codeblock = """
def CalcField(FreqField):
    if FreqField == 1:
        return 3
    elif FreqField == 2:
        return 6
    elif FreqField == 3:
        return 9
    elif FreqField == 4:
        return 12
    else:
        return 0"""

# ****LARGE_RETAIL***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearLargeRetailFreq, "nearLargeRetailFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearLargeRetailFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "LARGE_RETAIL", "CalcField(!Street_Near_Large_Retail_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***SCHOOL***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearSchoolFreq, "nearSchoolFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearSchoolFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "SCHOOL", "CalcField(!Street_Near_School_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***CHURCH***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearChurchFreq, "nearChurchFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearChurchFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "CHURCH", "CalcField(!Street_Near_Church_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***PARK***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearParkFreq, "nearParkFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearParkFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "PARK", "CalcField(!Street_Near_Park_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***LARGE_OFFICE***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearLargeOfficeFreq, "nearLargeOfficeFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearLargeOfficeFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "LARGE_OFFICE", "CalcField(!Street_Near_Large_Office_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***MULTIFAMILY***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearMultifamily, "nearMultifamilyView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearMultifamilyView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock for calculating MULTIFAMILY field
multifamilyCodeblock = """
def CalcField(OID,INFID):
    if OID == INFID:
        return 3
    else:
        return 0"""

arcpy.CalculateField_management("streetSelectLayer", "MULTIFAMILY", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Multifamily.IN_FID!)", "PYTHON_9.3", multifamilyCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***SOCIAL_SERVICE***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearSocialServiceFreq, "nearSocialServiceFreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearSocialServiceFreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "SOCIAL_SERVICE", "CalcField(!Street_Near_Social_Service_Freq.FREQUENCY!)", "PYTHON_9.3", max12Codeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***TOTAL_12MAX***
# Calculate TOTAL_12MAX field that sums above fields together and remove any values above 12
arcpy.CalculateField_management("streetSelectLayer", "TOTAL_12MAX", "(!LARGE_RETAIL! + !SCHOOL! + !CHURCH! + !PARK! + !LARGE_OFFICE! + !MULTIFAMILY! + !SOCIAL_SERVICE!)", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# Codeblock to remove any values above 12
totalMax12Codeblock = """
def CalcField(TotalMax12):
    if TotalMax12 > 12:
        return 12
    else:
        return TotalMax12"""

arcpy.CalculateField_management("streetSelectLayer", "TOTAL_12MAX", "CalcField(!TOTAL_12MAX!)", "PYTHON_9.3", totalMax12Codeblock)
print "\n", arcpy.GetMessages()

# ***PUBLIC_TRANS***
# Make Feature Layer, Add Join, Calculate, Remove Join
arcpy.MakeFeatureLayer_management(publicTransHin, "publicTransHinLayer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "ASMP_STREET_NETWORK_ID", "publicTransHinLayer", "ASMP_STREET_NETWORK_ID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate PUBLIC_TRANS field
publicTransCodeblock = """
def CalcField(PublicTrans):
    if PublicTrans == 'Yes':
        return 3
    elif PublicTrans == 'Multiple':
        return 5
    else:
        return 0"""
        
arcpy.CalculateField_management("streetSelectLayer", "PUBLIC_TRANS", "CalcField(!ASMP_Street_Public_Trans_HIN.Bus_Routes!)", "PYTHON_9.3", publicTransCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***HH_INCOME***
# Field was calculated to 0 in first script (account for 60k and more and no data)
# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 50k to 60k
arcpy.MakeFeatureLayer_management(hhIncome, "hhIncomeLayer", "Median_HH_Income_Merge = '50k to 60k'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "hhIncomeLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "HH_Income", 3, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Loction, Calculate, Clear Selection for 40k to 50k
arcpy.MakeFeatureLayer_management(hhIncome, "hhIncomeLayer", "Median_HH_Income_Merge = '40k to 50k'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "hhIncomeLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "HH_Income", 6, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 40k and below
arcpy.MakeFeatureLayer_management(hhIncome, "hhIncomeLayer", "Median_HH_Income_Merge = '40k and below'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "hhIncomeLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "HH_Income", 10, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# ***POP_DENSITY***
# Field was calculated to 0 in first script (accounts for < median and no data)
# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 0% - 25%
arcpy.MakeFeatureLayer_management(popDensity, "popDensityLayer", "Pop_Density_Rank = '0% - 25%'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "popDensityLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 1, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 25% - 50%
arcpy.MakeFeatureLayer_management(popDensity, "popDensityLayer", "Pop_Density_Rank = '25% - 50%'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "popDensityLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 2, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 50% - 75%
arcpy.MakeFeatureLayer_management(popDensity, "popDensityLayer", "Pop_Density_Rank = '50% - 75%'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "popDensityLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 3, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for 75% - 100%
arcpy.MakeFeatureLayer_management(popDensity, "popDensityLayer", "Pop_Density_Rank = '75% - 100%'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "popDensityLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 4, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# Make Feature Layer, Select Layer by Location, Calculate, Clear Selection for > 100%
arcpy.MakeFeatureLayer_management(popDensity, "popDensityLayer", "Pop_Density_Rank = '> 100%'", "", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByLocation_management("streetSelectLayer", "INTERSECT", "popDensityLayer", "", "NEW_SELECTION", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "POP_DENSITY", 5, "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "CLEAR_SELECTION", "")
print "\n", arcpy.GetMessages()

# ***CSR***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearSignalReqPhb, "nearSignalReqPhbView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearSignalReqPhbView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate CSR
signalReqPhbCodeblock = """
def CalcField(OID,FID,Status):
    if OID == FID and Status <> 'RECOMMENDED':
        return 3
    elif OID == FID and Status == 'RECOMMENDED':
        return -1
    else:
        return 0"""

# Codeblock to calculate REQUEST fields
requestCodeblock = """
def CalcField(OID,FID,Request):
    if OID == FID:
        return Request
    else:
        return None"""
        
arcpy.CalculateField_management("streetSelectLayer", "CSR", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Signal_Req_PHB.IN_FID!,!Street_Near_Signal_Req_PHB.REQUEST_STATUS!)", "PYTHON_9.3", signalReqPhbCodeblock)
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "CSR_REQUEST_TYPE", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Signal_Req_PHB.IN_FID!,!Street_Near_Signal_Req_PHB.REQUEST_TYPE!)", "PYTHON_9.3", requestCodeblock)
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "CSR_REQUEST_STATUS", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Signal_Req_PHB.IN_FID!,!Street_Near_Signal_Req_PHB.REQUEST_STATUS!)", "PYTHON_9.3", requestCodeblock)
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "CSR_REQUEST_DATE", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Signal_Req_PHB.IN_FID!,!Street_Near_Signal_Req_PHB.REQUEST_DATE!)", "PYTHON_9.3", requestCodeblock)
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "CSR_REQUEST_SOURCE", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Signal_Req_PHB.IN_FID!,!Street_Near_Signal_Req_PHB.REQUEST_SOURCE!)", "PYTHON_9.3", requestCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# Calculate TOTAL_DEMAND field
arcpy.CalculateField_management("streetSelectLayer", "TOTAL_DEMAND", "!TOTAL_12MAX! + !PUBLIC_TRANS! + !HH_INCOME! + !POP_DENSITY! + !CSR!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# ***RISK CRITERIA***
#--------------------
# ***TRAVEL_LANES***
# Codeblock to calculate TRAVEL_LANES field and Caculate Field
travelLaneCodeblock = """
def CalcField(CrossSection):
    if '1' in CrossSection:
        return 0
    elif '2' in CrossSection:
        return 2
    elif '3' in CrossSection:
        return 2
    elif '4' in CrossSection:
        return 5
    elif '5' in CrossSection:
        return 5
    elif '6' in CrossSection:
        return 8
    elif '7' in CrossSection:
        return 8
    elif '8' in CrossSection:
        return 8
    elif '9' in CrossSection:
        return 8
    else:
        return 0"""

arcpy.CalculateField_management("streetSelectLayer", "TRAVEL_LANES", "CalcField(!EX_XS_GENERAL!)", "PYTHON_9.3", travelLaneCodeblock)
print "\n", arcpy.GetMessages()

# ***SPEED***
# Make Feature Layer, Add Join, Calculate, Remove Join
arcpy.MakeFeatureLayer_management(publicTransHin, "speedLayer", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "ASMP_STREET_NETWORK_ID", "speedLayer", "ASMP_STREET_NETWORK_ID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate SPEED field
speedCodeblock = """
def CalcField(SpeedLimit):
    if SpeedLimit < 30:
        return 0
    elif SpeedLimit == 30:
        return 2
    elif SpeedLimit == 35:
        return 4
    elif SpeedLimit == 40:
        return 7
    elif SpeedLimit > 40:
        return 10
    else:
        return -1"""
        
arcpy.CalculateField_management("streetSelectLayer", "SPEED", "CalcField(!ASMP_Street_Public_Trans_HIN.Speed_Limit_City_Code!)", "PYTHON_9.3", speedCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()


## ***SIDEWALK***
## Calculate to Zero for now until this piece can possibly be added
##arcpy.CalculateField_management("streetSelectLayer", "SIDEWALK", 0, "PYTHON_9.3", "")
##print "\n", arcpy.GetMessages()

# ***STREET_LIGHT***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearStreetlight, "nearStreetlightView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearStreetlightView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate STREET_LIGHT field
streetlightCodeblock = """
def CalcField(OID,INFID):
    if OID == INFID:
        return 0
    else:
        return 5"""

arcpy.CalculateField_management("streetSelectLayer", "STREET_LIGHT", "CalcField(!Street_Select_PHB.OBJECTID!,!Street_Near_Streetlight.IN_FID!)", "PYTHON_9.3", streetlightCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***SIGNAL***
# Make Table View, Add Join, Calculate, Remove Join
arcpy.MakeTableView_management(nearSignal, "nearSignalView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearSignalView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate SIGNAL field
signalCodeblock = """
def CalcField(Distance):
    if Distance > 1200:
        return 12
    elif Distance > 1020 and Distance <= 1200:
        return 10
    elif Distance > 840 and Distance <= 1020:
        return 8
    elif Distance > 660 and Distance <= 840:
        return 6
    elif Distance > 480 and Distance <= 660:
        return 4
    elif Distance > 300 and Distance <= 480:
        return 2
    elif Distance <= 300:
        return -1"""

arcpy.CalculateField_management("streetSelectLayer", "SIGNAL", "CalcField(!Street_Near_Signal.NEAR_DIST!)", "PYTHON_9.3", signalCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# ***MEDIAN***
# Codeblock to calculate MEDIAN field and Calculate Field
medianCodeblock = """
def CalcField(CrossSection):
    if 'D' in CrossSection:
        return 0
    else:
        return 5"""

arcpy.CalculateField_management("streetSelectLayer", "MEDIAN", "CalcField(!EX_XS_GENERAL!)", "PYTHON_9.3", medianCodeblock)
print "\n", arcpy.GetMessages()

# Calculate TOTAL_RISK field
arcpy.CalculateField_management("streetSelectLayer", "TOTAL_RISK", "!TRAVEL_LANES! + !SPEED! + !STREET_LIGHT! + !SIGNAL! + !MEDIAN!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# ***SAFETY CRITERIA***
#----------------------
# ***PHIN, BHIN, HIN_ALL***
# Feature layer for Street_Public_Trans_HIN was created above under PUBLIC_TRANS section
# Add Join, Calculate PHIN & BHIN, Remove Join, Calculate HIN_ALL
arcpy.AddJoin_management("streetSelectLayer", "ASMP_STREET_NETWORK_ID", "publicTransHinLayer", "ASMP_STREET_NETWORK_ID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to Calculate PHIN/BHIN
hinCodeblock = """
def CalcField(HIN):
    if HIN == 'Yes':
        return 5
    else:
        return 0"""

arcpy.CalculateField_management("streetSelectLayer", "PHIN", "CalcField(!ASMP_Street_Public_Trans_HIN.PHIN!)", "PYTHON_9.3", hinCodeblock)
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "BHIN", "CalcField(!ASMP_Street_Public_Trans_HIN.BHIN!)", "PYTHON_9.3", hinCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "HIN_ALL", "(!PHIN! + !BHIN!)", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# ***PED_CRASH_200, PED_CRASH_400, PED_CRASH_ALL***
# Make Table View, Add Join, Calculate, Remove Join for PED_CRASH_200
arcpy.MakeTableView_management(nearPedCrash2Freq, "nearPedCrash2FreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearPedCrash2FreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()

# Codeblock to calculate PED_CRASH_200 / PED_CRASH_400 field
pedCrashCodeblock = """
def CalcField(Frequency):
    if Frequency is None:
        return 0
    else:
        return Frequency"""

arcpy.CalculateField_management("streetSelectLayer", "PED_CRASH_200", "CalcField(!Street_Near_Ped_Crash_200_Freq.FREQUENCY!)", "PYTHON_9.3", pedCrashCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# Make Table View, Add Join, Calculate, Remove Join for PED_CRASH_400
arcpy.MakeTableView_management(nearPedCrash4Freq, "nearPedCrash4FreqView", "", "", "")
print "\n", arcpy.GetMessages()
arcpy.AddJoin_management("streetSelectLayer", "OBJECTID", "nearPedCrash4FreqView", "IN_FID", "KEEP_ALL")
print "\n", arcpy.GetMessages()
arcpy.CalculateField_management("streetSelectLayer", "PED_CRASH_400", "CalcField(!Street_Near_Ped_Crash_400_Freq.FREQUENCY!)", "PYTHON_9.3", pedCrashCodeblock)
print "\n", arcpy.GetMessages()
arcpy.RemoveJoin_management("streetSelectLayer", "")
print "\n", arcpy.GetMessages()

# Codeblock to calculate PED_CRASH_ALL and Calculate
pedCrashAllCodeblock = """
def CalcField(PedCrash200, PedCrash400):
    if PedCrash200 == 0 and PedCrash400 > 0:
        return 5
    elif PedCrash200 > 0 and PedCrash400 == PedCrash200:
        return 10
    elif PedCrash200 > 0 and PedCrash400 > PedCrash200:
        return 15
    else:
        return 0"""

arcpy.CalculateField_management("streetSelectLayer", "PED_CRASH_ALL", "CalcField(!PED_CRASH_200!, !PED_CRASH_400!)", "PYTHON_9.3", pedCrashAllCodeblock)
print "\n", arcpy.GetMessages()

# Calculate TOTAL_SAFETY field
arcpy.CalculateField_management("streetSelectLayer", "TOTAL_SAFETY", "!HIN_ALL! + !PED_CRASH_ALL!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# Calculate TOTAL_RANK based on all criteria calculated above
arcpy.CalculateField_management("streetSelectLayer", "TOTAL_SCORE", "!TOTAL_DEMAND! + !TOTAL_RISK! + !TOTAL_SAFETY!", "PYTHON_9.3", "")
print "\n", arcpy.GetMessages()

# Select segments that are not Recommended PHBs / Signals, then select segments that are > 300' from an active Signal
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "NEW_SELECTION", "CSR >= 0")
print "\n", arcpy.GetMessages
arcpy.SelectLayerByAttribute_management("streetSelectLayer", "SUBSET_SELECTION", "SIGNAL >= 2")
print "\n", arcpy.GetMessages()

# Select to create Street_Select_PHB_Final from above selections
arcpy.Select_analysis("streetSelectLayer", streetSelectFinal, "")
print "\n", arcpy.GetMessages()

print "\n" + "Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime())
