# Wind-Farm-Site-Suitability-Analysis
Determine the optimal location for a set of new high-efficiency wind turbines in Colorado.

## Criteria 
The selected site must meet several criteria:

* Located in the state of Colorado
* In counties where the population as of 2010 is at least 20,000
* In areas where the wind power class is at least 4 (Annual wind speeds in these areas at 10 meters off the ground are generally at least 5.6 meters per second [12.5 mph], and at 50 meters off the ground are generally 7.0 meters per second [15.7 mph].)
* Within 10 miles of existing power lines that have a capacity of at least 400 kilovolts (kV)
* Within 5 miles of existing wind farms containing turbines where the rotor diameters span at least 100 feet

## Analysis 
* Merge Wind Power Class and Counties using Union tool

![Union_of_WindPowerClass_Counties](https://user-images.githubusercontent.com/66695888/223736746-a297f24d-1127-4d62-8ca3-134e8d1f3d00.png)

* Use the Select tool to query the Transmission Lines data by building the expression "Voltage >= 400"

![Voltage_atleast_400](https://user-images.githubusercontent.com/66695888/223737754-f6d7cfff-c54b-4cad-b535-94900e577148.png)

* Use the Buffer tool to ensure the locations are within 10 miles from the existing power lines by generating a 10-mile buffer zone around the transmission lines and dissolving all output features

![Transmission_Lines_10Mile_Zone](https://user-images.githubusercontent.com/66695888/223738875-809593d2-0dfb-4475-8d8a-745664033b2b.png)

* Use the Select tool to identify Wind Turbines in Colorado whose rotor diameters span at least 100 feet using the query expression "rotor_dia >= 100" 

![Turbine_rot_dia_100](https://user-images.githubusercontent.com/66695888/223740072-813ee740-f8b9-42bb-af3f-e8a86b8f6dcb.png)

* Use the Buffer tool to generate 5-Mile buffer around these turbines and dissolving all outputs

![Turbine_5Mile_Zone](https://user-images.githubusercontent.com/66695888/223740646-1e6c7028-3d98-4a63-9db3-ba02b06a7c6c.png)

There are four turbine clusters, 3 of which has met the criteria so far. To finalise the selction, we will look at the populations of the counties in which these clusers are located.

* Use the Union tool to merge "Turbine_5Mile_Zone", "TransmissionLines_10Mile_Zone" and the "Union_of_WindPowerClass_Counties", with output name "TargetSites"

![TargetSites](https://user-images.githubusercontent.com/66695888/223741961-0ebf8b2a-d464-4b66-b6e2-85c2fb319357.png)

* Use the Intersect tool to find "TargetSites" that are within "Turbine_5Mile_Zone" with output name "TargetSites_Intersect_Turbine"

![TargetSites_Intersect_Turbine](https://user-images.githubusercontent.com/66695888/223743209-cf18cdc4-a034-4e97-b84c-668400777d0e.png)

* Once again, use the Intersect tool to find "TargetSites_Intersect_Turbine" that are within "TransmissionLines_10Mile_Zone" with output name "TargetSites_Intersect_Turbine_TransmissionLines"

![TargetSites_Intersect_Turbine_TransmissionLines](https://user-images.githubusercontent.com/66695888/223743592-2579b689-79da-43e0-a81b-9a607fe2b9ad.png)

## Final Result
* Use the Select tool to identify "TargetSites_Intersect_Turbine_TransmissionLines" whose 2010 population is at least 20000 using the query expression "POP2010 >= 20000", with result output name SuitableSites

![SuitableSites](https://user-images.githubusercontent.com/66695888/223744657-56ae330b-67b0-4157-a590-a3bc01f6cf47.png)
