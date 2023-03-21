import arcpy 
from sys import argv
arcpy.env.workspace = "D:/GIS_Data_Analysis/Suitability_Analysis/analysis.gdb"

def Analysis(Platts_Transmission_Lines="Platts_Transmission_Lines", Wind_Power_Class="Wind_Power_Class", Counties="Counties", Wind_Turbines_in_Colorado="Wind_Turbines_in_Colorado", SuitableSites="SuitableSites"):

    # To allow overwriting outputs, change option to True.
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(scratchWorkspace="analysis.gdb", workspace="analysis.gdb"):

        # Process: Select (2) (Select) (analysis)
        Wind_Turbines_in_Colorado_Se = "Wind_Turbines_in_Colorado_Se"
        arcpy.analysis.Select(in_features=Wind_Turbines_in_Colorado, out_feature_class=Wind_Turbines_in_Colorado_Se, where_clause="rotor_dia >= 100")

        # Process: Buffer (2) (Buffer) (analysis)
        Turbine_5Mile_Zone = "Turbine_5Mile_Zone"
        arcpy.analysis.Buffer(in_features=Wind_Turbines_in_Colorado_Se, out_feature_class=Turbine_5Mile_Zone, buffer_distance_or_field="5 Miles", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

        # Process: Select (Select) (analysis)
        Platts_Transmission_Lines_400 = "Platts_Transmission_Lines_400"
        arcpy.analysis.Select(in_features=Platts_Transmission_Lines, out_feature_class=Platts_Transmission_Lines_400, where_clause="VOLTAGE >= 400")

        # Process: Buffer (Buffer) (analysis)
        Transmission_Lines_10Mile_Zone = "Transmission_Lines_10Mile_Zone"
        arcpy.analysis.Buffer(in_features=Platts_Transmission_Lines_400, out_feature_class=Transmission_Lines_10Mile_Zone, buffer_distance_or_field="10 Miles", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

        # Process: Union (Union) (analysis)
        TargetSites = "TargetSites"
        arcpy.analysis.Union(in_features=[[Wind_Power_Class, ""], [Counties, ""], [Turbine_5Mile_Zone, ""], [Transmission_Lines_10Mile_Zone, ""]], out_feature_class=TargetSites, join_attributes="ALL", cluster_tolerance="", gaps="GAPS")

        # Process: Intersect (Intersect) (analysis)
        TargetSites_Turbine = "TargetSites_Turbine"
        arcpy.analysis.Intersect(in_features=[[TargetSites, ""], [Turbine_5Mile_Zone, ""]], out_feature_class=TargetSites_Turbine, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")

        # Process: Intersect (2) (Intersect) (analysis)
        TargetSites_Turbine_TransmissionLine = "TargetSites_Turbine_TransmissionLine"
        arcpy.analysis.Intersect(in_features=[[TargetSites_Turbine, ""], [Transmission_Lines_10Mile_Zone, ""]], out_feature_class=TargetSites_Turbine_TransmissionLine, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")

        # Process: Select (3) (Select) (analysis)
        arcpy.analysis.Select(in_features=TargetSites_Turbine_TransmissionLine, out_feature_class=SuitableSites, where_clause="POP2010 >= 20000")

if __name__ == '__main__':
    Analysis(*argv[1:])
