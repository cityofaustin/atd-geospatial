#------------------------------------
# Median_HH_Income.py
# Modifies Household Income table from Census Bureau and creates median income per Block Group
# Created by: Jaime McKeown
# Modified on: 10/19/2021
#------------------------------------

# Import modules
import time
print("Started at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
import arcpy
arcpy.env.overwriteOutput = True

# Set variables for the environment and working data
workspace = "g:\\ATD\\ATD_GIS\\Arterial_Management\\56_Pedestrian_Hybrid_Beacon_PHB\\Data_Driven_PHB_Ranking\\DTS\\Data\\"
dataCollGdb = workspace + "Data_Collection.gdb\\"
hhIncome = dataCollGdb + "Block_Group_HH_Income"

# Make Table View for Block_Group_HH_Income"
print("\n" + "Make Table View: Block Group HH Income")
arcpy.MakeTableView_management(hhIncome, "HH_Income_Layer", "", "", "")
print("\n" + arcpy.GetMessages())

# Add Fields to Block_Group_HH_Income for calculating median income
print("\n" + "Add Fields: Block Group HH Income for calculating median income")
arcpy.AddField_management("HH_Income_Layer", "Median_HH_Income", "TEXT", "", "", 25, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Median_Number", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Less_than_10k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_10k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_10k_15k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_15k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_15k_20k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_20k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_20k_25k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_25k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_25k_30k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_30k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_30k_35k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_35k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_35k_40k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_40k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_40k_45k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_45k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_45k_50k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_50k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_50k_60k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_60k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_60k_75k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_75k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_75k_100k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_100k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_100k_125k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_125k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_125k_150k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_150k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Btwn_150k_200k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_less_than_200k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Greater_than_200k", "TEXT", "", "", 5, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "Count_greater_than_200k", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())
arcpy.AddField_management("HH_Income_Layer", "GEOID", "TEXT", "", "", 12, "", "NULLABLE", "NON_REQUIRED", "")
print("\n" + arcpy.GetMessages())

# Calculate Median_Number field on Block_Group_HH_Income
print("\n" + "Calculate Field: Median_Number on Block Group HH Income")
arcpy.CalculateField_management("HH_Income_Layer", "Median_Number", "!HH_Income_Total! / 2", "PYTHON3", "")
print("\n" + arcpy.GetMessages())

# Calculate Count fields for each income level on Block_Group_HH_Income
print("\n" + "Calculate Fields: Count fields for each income level on Block Group HH Income")
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_10k", "!Total_less_than_10k!", "PYTHON_9.3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_15k", "!Count_less_than_10k! + !Total_10k_to_15k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_20k", "!Count_less_than_15k! + !Total_15k_to_20k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_25k", "!Count_less_than_20k! + !Total_20k_to_25k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_30k", "!Count_less_than_25k! + !Total_25k_to_30k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_35k", "!Count_less_than_30k! + !Total_30k_to_35k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_40k", "!Count_less_than_35k! + !Total_35k_to_40k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_45k", "!Count_less_than_40k! + !Total_40k_to_45k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_50k", "!Count_less_than_45k! + !Total_45k_to_50k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_60k", "!Count_less_than_50k! + !Total_50k_to_60k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_75k", "!Count_less_than_60k! + !Total_60k_to_75k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_100k", "!Count_less_than_75k! + !Total_75k_to_100k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_125k", "!Count_less_than_100k! + !Total_100k_to_125k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_150k", "!Count_less_than_125k! + !Total_125k_to_150k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_less_than_200k", "!Count_less_than_150k! + !Total_150k_to_200k!", "PYTHON3", "")
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Count_greater_than_200k", "!Total_200k_or_more!", "PYTHON_9.3", "")
print("\n" + arcpy.GetMessages())

# Codeblock for Less_than_10k field from Block_Group_HH_Income
lessCodeblock = """
def CalcField(Count,Median):
    if Count > Median:
        return 'TRUE'
    else:
        return 'FALSE'"""

# Codeblock for all Btwn... and Greater_than_200k fields from Block_Group_HH_Income
btwnGreaterCodeblock = """
def CalcField(Count1,Median,Count2):
    if Count1 > Median and Median >= Count2:
        return 'TRUE'
    else:
        return 'FALSE'"""

# Calculate True/False fields based on codeblocks
print("\n" + "Calculate Fields: True/False based on codeblocks")
arcpy.CalculateField_management("HH_Income_Layer", "Less_than_10k", "CalcField(!Count_less_than_10k!,!Median_Number!)", "PYTHON3", lessCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_10k_15k", "CalcField(!Count_less_than_15k!,!Median_Number!,!Count_less_than_10k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_15k_20k", "CalcField(!Count_less_than_20k!,!Median_Number!,!Count_less_than_15k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_20k_25k", "CalcField(!Count_less_than_25k!,!Median_Number!,!Count_less_than_20k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_25k_30k", "CalcField(!Count_less_than_30k!,!Median_Number!,!Count_less_than_25k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_30k_35k", "CalcField(!Count_less_than_35k!,!Median_Number!,!Count_less_than_30k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_35k_40k", "CalcField(!Count_less_than_40k!,!Median_Number!,!Count_less_than_35k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_40k_45k", "CalcField(!Count_less_than_45k!,!Median_Number!,!Count_less_than_40k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_45k_50k", "CalcField(!Count_less_than_50k!,!Median_Number!,!Count_less_than_45k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_50k_60k", "CalcField(!Count_less_than_60k!,!Median_Number!,!Count_less_than_50k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_60k_75k", "CalcField(!Count_less_than_75k!,!Median_Number!,!Count_less_than_60k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_75k_100k", "CalcField(!Count_less_than_100k!,!Median_Number!,!Count_less_than_75k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_100k_125k", "CalcField(!Count_less_than_125k!,!Median_Number!,!Count_less_than_100k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_125k_150k", "CalcField(!Count_less_than_150k!,!Median_Number!,!Count_less_than_125k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Btwn_150k_200k", "CalcField(!Count_less_than_200k!,!Median_Number!,!Count_less_than_150k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())
arcpy.CalculateField_management("HH_Income_Layer", "Greater_than_200k", "CalcField(!Count_greater_than_200k!,!Median_Number!,!Count_less_than_200k!)", "PYTHON3", btwnGreaterCodeblock)
print("\n" + arcpy.GetMessages())

# Codeblock for Median_HH_Income field from Block_Group_HH_Income
medianCodeblock = """
def CalcField(Less10,Btwn10to15,Btwn15to20,Btwn20to25,Btwn25to30,Btwn30to35,Btwn35to40,Btwn40to45,Btwn45to50,Btwn50to60,Btwn60to75,Btwn75to100,Btwn100to125,Btwn125to150,Btwn150to200,Greater200):
    if Less10 == 'TRUE':
        return 'Less_than_10k'
    elif Btwn10to15 == 'TRUE':
        return 'Btwn_10k_15k'
    elif Btwn15to20 == 'TRUE':
        return 'Btwn_15k_20k'
    elif Btwn20to25 == 'TRUE':
        return 'Btwn_20k_25k'
    elif Btwn25to30 == 'TRUE':
        return 'Btwn_25k_30k'
    elif Btwn30to35 == 'TRUE':
        return 'Btwn_30k_35k'
    elif Btwn35to40 == 'TRUE':
        return 'Btwn_35k_40k'
    elif Btwn40to45 == 'TRUE':
        return 'Btwn_40k_45k'
    elif Btwn45to50 == 'TRUE':
        return 'Btwn_45k_50k'
    elif Btwn50to60 == 'TRUE':
        return 'Btwn_50k_60k'
    elif Btwn60to75 == 'TRUE':
        return 'Btwn_60k_75k'
    elif Btwn75to100 == 'TRUE':
        return 'Btwn_75k_100k'
    elif Btwn100to125 == 'TRUE':
        return 'Btwn_100k_125k'
    elif Btwn125to150 == 'TRUE':
        return 'Btwn_125k_150k'
    elif Btwn150to200 == 'TRUE':
        return 'Btwn_150k_200k'
    elif Greater200 == 'TRUE':
        return 'Greater_than_200k'
    else:
        return 'N/A'"""

# Calculate Median_HH_Income field from Block_Group_HH_Income
print("\n" + "Calculate Field: Median HH Income")
arcpy.CalculateField_management("HH_Income_Layer", "Median_HH_Income", "CalcField(!Less_than_10k!,!Btwn_10k_15k!,!Btwn_15k_20k!,!Btwn_20k_25k!,!Btwn_25k_30k!,!Btwn_30k_35k!,!Btwn_35k_40k!,!Btwn_40k_45k!,!Btwn_45k_50k!,!Btwn_50k_60k!,!Btwn_60k_75k!,!Btwn_75k_100k!,!Btwn_100k_125k!,!Btwn_125k_150k!,!Btwn_150k_200k!,!Greater_than_200k!)", "PYTHON3", medianCodeblock)
print("\n" + arcpy.GetMessages())

# Calculate GEOID field from Block_Group_HH_Income
print("\n" + "Calculate Field: GEOID Field")
arcpy.CalculateField_management("HH_Income_Layer", "GEOID", "!Geo_ID![-12:]", "PYTHON3", "")
print("\n" + arcpy.GetMessages())

print("Completed at " + time.strftime("%Y/%m/%d %H.%M.%S", time.localtime()))
