from CoordinateConversion import (
    LL2utm,
    utm2LL,
    getLLfromDMS,
    distanceBetweenLL,
    distanceBetweenUTM,
    Datums,
)
from dxf_to_csv import dxfParser
from kml_to_csv import kmlParser
import csv
import os
import sys


def mainMenu():

    # While there is no valid file or path continuously ask until it is valid or user quits
    path = get_path()

    # While no valid datum continuously ask user until it is valid or user quits
    datum_input = get_datum()
    while datum_input not in Datums.keys():
        print('\nInvalid datum entry. Below are the available datums. If you would like to terminate enter "quit"')
        print(f"Acceptable Datum Entries: {[datum for datum in Datums]}")
        datum_input = get_datum()
        if datum_input == 'quit':
            sys.exit()

    # continuously ask user for valid conversion direction until valid or quits
    conv_dir = get_ConversionDirection()
    conv_complete = False
    while not conv_complete:

        if conv_dir == "ll2utm":
            batch_LL2utm(path, datum_input)
            conv_complete = True

        elif conv_dir == "utm2ll":
            Zone, zoneQuadrant, isNorth = utm_prompts()
            batch_utm2LL(path, datum_input, Zone, zoneQuadrant, isNorth)
            conv_complete = True

        elif conv_dir == "lldms2utm":
            batch_dms2utm(path, datum_input)
            conv_complete = True

        elif conv_dir == "kml2utm":
            batchKML_LL2utm(path, datum_input)
            conv_complete = True

        elif conv_dir == "dxf2ll":
            Zone, zoneQuadrant, isNorth = utm_prompts()
            batchDXF_utm2LL(path, datum_input, Zone, zoneQuadrant, isNorth)

        else:
            print(
                """\nInvalid conversion direction chosen please re-enter your desired direction. If you would
    like to terminate enter "quit" """
            )
            conv_dir = get_ConversionDirection()
            if conv_dir == "quit":
                sys.exit()

    scriptDirectory = os.getcwd()
    print(
        f"Conversion Complete. Please check [{scriptDirectory}] for the converted file."
    )


def utm_prompts():
    print("\nWhat zone are the sets of UTM coordinates in: \n")
    Zone = int(input("Input: "))

    print("\nWhat zone quadrant are the sets of UTM coordinates in? (ex. U)\n")
    zoneQuadrant = str(input("Input: "))

    print('\nAre the sets of UTM coordinates in the northern or southern hemisphere:')
    print('Enter True for Northern and False for Southern\n')
    isNorth = bool(input('Input: '))

    return Zone, zoneQuadrant, isNorth


# Method returns the path or file path both of which are suitable
def get_path():
    while True:
        print(
        "\nPlease enter one of the following options to complete your coordinate conversion:"
        )
        print("\nOption-1: Please enter the path for your .csv file.")
        print(
        """Option-2: Ensure that the selected csv file is located in the same directory as this script and
          please enter the path for your .csv file (example: MyCoordinates.csv).\n"""
        )

        path = str(input("Input: "))
      
        if path == "quit":
            sys.exit()
        elif not os.path.isfile(path):
            print(
                '\nThis path or file does not exist. Please try again or enter "quit" to terminate the system.'
            )
        else:
            break

    return path


# Method returns the conversion direction as a string
def get_ConversionDirection():
    print(
        """\nSelect the conversion direction:\n1. Lat/lon to UTM input -> LL2utm\n2. UTM to lat/lon input -> utm2LL
3. Lat/Lon (DMS) to UTM input -> LLdms2utm\n4. KML (lat/lon) to UTM input -> kml2utm
5. DXF (utm) to lat/lon input -> dxf2LL"""
    )
    conv_dir = str(input("Input: ")).lower()
    return conv_dir


# Gets datum
def get_datum():
    print(
        "\nWhat datum you would like to reference the conversion with (i.e. NAD 83, WGS 84 etc.):\n"
    )
    datum = input("Input: ").lower().replace(" ", "")
    return datum


# Get the output filename as a strign
def get_outputfilename():
    print("\nWhat would you like to name your output file? (ex. myfile)")
    outputFilename = str(input("\nInput: ")) + '.csv' # Create output file name
    return outputFilename


# Method converts a CSV file of latitude and longitude coordinates to UTM
def batch_LL2utm(path, datum_in):
    outputFilename = get_outputfilename()
    
    with open(path) as f:  # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=",")  # Generate a reader object from file
        with open(outputFilename, "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(
                [
                    "Latitude",
                    "Longitude",
                    "Easting",
                    "Northing",
                    "Zone",
                    "Zone Quadrant",
                    "Elevation",
                    "CumDistance (m)",
                ],
            )  # header
            next(reader)  # Skip the reader object header

            readerList = list(reader)
            distance = 0
            for lineCount, coords in enumerate(readerList, start=1):
                lat_in1 = float(coords[0])
                lon_in1 = float(coords[1])
                elevation = float(coords[2])
                east_out, north_out, zone, zone_quad = LL2utm(
                    lat_in1, lon_in1, datum=datum_in
                )

                prevIndex = lineCount - 2  # index of previous coord
                if prevIndex >= 0:  # will start on 2nd coord
                    lat_in0 = float(readerList[prevIndex][0])  # previous latitude
                    lon_in0 = float(readerList[prevIndex][1])  # previous longitude
                    distance += distanceBetweenLL(lat_in0, lon_in0, lat_in1, lon_in1)

                writer.writerow(
                    [lat_in1, lon_in1, east_out, north_out, zone, zone_quad, elevation, distance]
                )

    print(f"\nConverted {lineCount} coordinates")
    print(f"\nTotal polyline distance travelled: {distance} metres\n")


# Method converts CSV file of latitude longitude coordinates in deg,min,sec (dms) notation to UTM
def batch_dms2utm(path, datum_in):
   
    outputFilename = get_outputfilename()

    with open(path) as f:  # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=",")  # Generate a reader object from file
        with open(outputFilename, "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(
                [
                    "Latitude",
                    "Longitude",
                    "Easting",
                    "Northing",
                    "Zone",
                    "Zone Quadrant",
                    "Elevation",
                    "CumDistance (m)"
                ],
            )  # Write header
            next(reader)  # Skip the reader object header

            readerList = list(reader)
            distance = 0
            for lineCount, coords in enumerate(readerList, start=1):
                # Retrieve data and convert to decimal degrees
                lat_in1, lon_in1 = getLLfromDMS(
                    float(coords[0]),
                    float(coords[1]),
                    float(coords[2]),
                    float(coords[3]),
                    float(coords[4]),
                    float(coords[5]),
                )
                elevation = float(coords[6])
                # Convert Lat/Lon to utm
                east_out, north_out, zone, zone_quad = LL2utm(
                    lat_in1, lon_in1, datum=datum_in
                )
                # Calculate cumulative distance
                prevIndex = lineCount - 2  # index of previous coord
                if prevIndex >= 0:  # will start on 2nd coord
                    lat_in0, lon_in0 = getLLfromDMS(
                        float(readerList[prevIndex][0]),
                        float(readerList[prevIndex][1]),
                        float(readerList[prevIndex][2]),
                        float(readerList[prevIndex][3]),
                        float(readerList[prevIndex][4]),
                        float(readerList[prevIndex][5]),
                    )
                    distance += distanceBetweenLL(lat_in0, lon_in0, lat_in1, lon_in1)
                
                # Write to output csv file
                writer.writerow(
                    [lat_in1, lon_in1, east_out, north_out, zone, zone_quad, elevation, distance]
                )
   
    print(f"\nConverted {lineCount} coordinates")
    print(f"\nTotal polyline distance travelled: {distance} metres\n")


# Method converts a CSV file of UTM coordinates to latitude and longitude
def batch_utm2LL(path, datum_in, zone, zoneQuadrant, is_north):
   
    outputFilename = get_outputfilename()
    
    with open(path) as f:  # Open the UTM file from the dxf_to_csv parser
        reader = csv.reader(f, delimiter=",")  # Generate a reader object from file
        with open(outputFilename, "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(
                [
                    "Latitude",
                    "Longitude",
                    "Easting",
                    "Northing",
                    "Zone",
                    "Elevation (m)",
                    "CumDistance (m)"
                    ],
            )  # Write headers for the writer object
            next(reader)  # Skip the reader object header

            readerList = list(reader)
            distance = 0
            for lineCount, coords in enumerate(readerList, start=1):
                east_in1 = float(coords[0])
                north_in1 = float(coords[1])
                elevation = float(coords[3])
                lat_out, lon_out = utm2LL(
                    east_in1,
                    north_in1,
                    zone,
                    zoneQuadrant=zoneQuadrant,
                    North=is_north,
                    datum=datum_in,
                )

                prevIndex = lineCount - 2  # index of previous coord
                if prevIndex >= 0:  # will start on 2nd coord
                    east_in0 = float(readerList[prevIndex][0])  # previous easting
                    north_in0 = float(readerList[prevIndex][1])  # previous northing
                    distance += distanceBetweenUTM(
                        east_in0, north_in0, east_in1, north_in1
                    )

                writer.writerow([lat_out, lon_out, east_in1, north_in1, zone, elevation, distance])

    print(f"\nConverted {lineCount} coordinates")
    print(f"\nTotal polyline distance travelled: {distance} metres\n")


# Method converts a KML file of latitude and longitude coordinates to UTM
def batchKML_LL2utm(path, datum_in):
    outputFilename = get_outputfilename()

    with open(outputFilename, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(
            [
                "Latitude",
                "Longitude",
                "Easting",
                "Northing",
                "Zone",
                "Zone Quadrant",
                "Elevation",
                "CumDistance (m)",
            ],
        )  # header

        KML_dataStructure = kmlParser(path)
        distance = 0
        for lineCount, coords in enumerate(KML_dataStructure, start=1):
            lat_in1 = float(coords['Latitude'])
            lon_in1 = float(coords['Longitude'])
            elevation = float(coords['Elevation (m)'])
            east_out, north_out, zone, zone_quad = LL2utm(
                lat_in1, lon_in1, datum=datum_in
            )

            prevIndex = lineCount - 2  # index of previous coord
            if prevIndex >= 0:  # will start on 2nd coord
                lat_in0 = float(KML_dataStructure[prevIndex]['Latitude'])  # previous latitude
                lon_in0 = float(KML_dataStructure[prevIndex]['Longitude'])  # previous longitude
                distance += distanceBetweenLL(lat_in0, lon_in0, lat_in1, lon_in1)

            writer.writerow(
                [lat_in1, lon_in1, east_out, north_out, zone, zone_quad, elevation, distance]
            )

    print(f"\nConverted {lineCount} coordinates")
    print(f"\nTotal polyline distance travelled: {distance} metres\n")


# Method converts a DXF file of UTM coordinates to latitude and longitude
def batchDXF_utm2LL(path, datum_in, zone, zoneQuadrant, is_north):
    outputFilename = get_outputfilename()

    with open(outputFilename, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(
            [
                "Latitude",
                "Longitude",
                "Easting",
                "Northing",
                "Zone",
                "Elevation (m)",
                "CumDistance (m)"
            ],
        )  # Write headers for the writer object

        DXF_dataStructure = dxfParser(zone, path)
        distance = 0
        for lineCount, coords in enumerate(DXF_dataStructure, start=1):
            east_in1 = float(coords['utm_e'])
            north_in1 = float(coords['utm_n'])
            elevation = float(coords['Elevation (m)'])
            lat_out, lon_out = utm2LL(
                east_in1,
                north_in1,
                zone,
                zoneQuadrant=zoneQuadrant,
                North=is_north,
                datum=datum_in,
            )

            prevIndex = lineCount - 2  # index of previous coord
            if prevIndex >= 0:  # will start on 2nd coord
                east_in0 = float(DXF_dataStructure[prevIndex]['utm_e'])  # previous easting
                north_in0 = float(DXF_dataStructure[prevIndex]['utm_n'])  # previous northing
                distance += distanceBetweenUTM(
                    east_in0, north_in0, east_in1, north_in1
                )

            writer.writerow([lat_out, lon_out, east_in1, north_in1, zone, elevation, distance])

    print(f"\nConverted {lineCount} coordinates")
    print(f"\nTotal polyline distance travelled: {distance} metres\n")


# main
if __name__ == "__main__":
    Run = True
    print("Welcome to the utm2LL and LL2utm Conversion Tool".center(40, "="))

    # Run main menu until user decides to quit
    while Run:
        mainMenu()
        print(
            '\nTo execute another batch conversion press enter. To terminate submit "quit"\n'
        )
        if input("Input: ") == "quit":
            Run = False
