# Coordinate Conversions
Coordinate conversion tools for processing and modelling drone survey data written in Python3. Coordinates can be converted with reference to numerous different datums between the formats of latitude/longitude (decimal degrees), latitude/longitude (DMS notation), and  UTM (universal transverse mercator). This tookit can handle single coordinate conversions using SingularConversion.py and SingularConversionElevation.py or a set of coordinates using BatchConversion.py and BatchConversionsElevation.py.

### Workflow
------
![CoordinateConversionMap](../media/CoordinateConversionMap.png?raw=true)


### Avaliable Datums
------
WGS 84, NAD83, GRS 80, WGS 72, Australian 1965, Krasovsky 1940, North American 1927, International 1924, Hayford 1909, Clarke 1880, Clarke 1866, Airy 1830, Bessel 1841, Everest 1830

### Input Files - BatchConversion.py
------
All input files must be .csv, .kml, or .dxf formats. The five options for file input are as follows:
1. Latitude (decimal degrees), Longitude (decimal degrees), Elevation (metres)  must occupy the first three columns of your csv file **in that order**.

Latitude (decimal degrees) | Longitude (decimal degrees) | Elevation (metres)
--- | --- | ---
50.88610427 | -121.4797261 | 574.7047903

2. Latitude (degrees, minutes, seconds), Longitude(degrees, minutes, seconds), Elevation (metres) must occupy the first seven columns of your csv file. The order for this must be latitude in columns 1,2,3 respectively while longitude follows in columns 4, 5, and 6. Entries must be **in that order**.

Latitude (D) | Latitude (M) | Latitude (S) | Longitude (D) | Longitude (M) | Longitude (S) | Elevation (metres)
--- | --- | --- | --- | --- | --- | --- |
50 | 53 | 9.975362137 | -121 | 28 | 47.01385705 | 574.7047903

3. UTM (easting, northing, zone, elevation) must occupy the first two columns of your csv file **in that order**.

Easting (metres) | Northing (metres) | Zone | Elevation (metres)
--- | --- | --- | --- |
606935.4236 | 5638260.254 | 10 | 574.7047903

4. KML just must be formed with a valid set of points.
5. DXF just must be formed with a valid set of points.

**Note that if you're using the KML or DXF to CSV scripts on your original polyline all the input files will be accordingly formatted for further use in the batchConversion.py**

**The first set of coordinates should appear on the 2nd row (the system ignores column headers).**

### Available Conversions - BatchConversion.py
------
Currently, there are three available conversion directions:

### Latitude/Longitude(decimal degrees) to UTM:
To execute this you must input a latiude/longitude(decimal degrees) file. The necessary format is noted in “Input Files Section 1”. With this you will be asked for the path and datum. The conversion will produce your output file in the same directory as the batchConversion.py file.

### Latitude/Longitude(degrees, minutes, seconds) to UTM:
To execute this you must input a latiude/longitude(deg,min,sec) file. The necessary format is noted in “Input Files Section 2”. With this you will be asked for the file path and datum used. The conversion will produce your output file in the same directory as the batchConversion.py file.

### UTM to Latitude/Longitude(decimal degrees):
To execute this you need to input a UTM file. The necessary format is noted in “Input Files Section 3”. Here you will need the file path, zone, either the zone quadrant or the hemisphere of your coordinates, and the datum used. The conversion will produce your output file in the same directory as the batchConversion.py file.

### KML to complete output:
To execute this you need an input .kml file. The resulting output will include the latitude/longitude; the UTM easting, northing and zones; the elevation; and the cumulative distance. The output file will contain all necessary data to execute the BatchConversionsElevation.py.

### DXF to complete output:
To execute this you need an input .dxf file. The resulting output will inlcude the latitude/longitude; the UTM easting, northing and zones; the elevation; and the cumulative distance. The output file will contain all necessary data to execute the BatchConversionsElevation.py.

### BatchConversionElevation.py
This script is used to convert between ellipsoidal and orthometric heights as well as between the CGVD28 and CGVD2013 datums. Using one of the output files from the batchConversion.py script you use these as inputs and it will upload it to  https://webapp.geod.nrcan.gc.ca/geod/tools-outils/gpsh.php and automatically download the webapp's output file as a csv with the input data as well as the new transformed heights (common conversion direction will be "3").
Note that your file must have these 4 critical headings: UTM Easting, UTM Northing, Zone, elevation

### Errors:
------
The error of the conversion seems to be quite accurate.
* Going from Lat/Lon to UTM (profile.kml converted to profile.csv) the average error for the 55 coordinates was roughly 1 micrometre for easting and 0.1mm for northing.
* Going from UTM to Lat/Lon (profile.dxf converted to profile.csv) the average error for the 54 coordinates was roughly 1 nanometre for latitude, zero for longitude.

Geodetic control monuments with known Latitude and Longitude + UTM values were also compared against the system:
* Going from Lat/Lon (deg,min,sec) to UTM the average error for the 9 coordinates was roughly 0.2mm for Easting and 0.4mm for Northing.
* For greater detail in the errors see the [Conversion Errors Google sheet](https://docs.google.com/spreadsheets/d/1ji0FxSZ786cPkNk0wIezwoCyrZBmFLjxTOtS8qBjaK8/edit?usp=sharing, "CoordinateConversion.py").
