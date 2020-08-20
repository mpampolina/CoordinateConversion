from CoordinateConversion import (
    LL2utm,
    utm2LL,
    getLLfromDMS,
    distanceBetweenLL,
    distanceBetweenUTM,
    Datums,
)
from utils import (
    dxfParser,
    kmlParser,
    utm_prompts,
    get_path,
    get_ConversionDirection,
    get_datum,
    get_outputfilename,
)
import csv
import os
import sys


# Main menu for the batch conversions
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
            conv_complete = True

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
                east_out1, north_out1, zone, zone_quad = LL2utm(
                    lat_in1, lon_in1, datum=datum_in
                )
                
                prevIndex = lineCount - 2  # index of previous coord
                if prevIndex >= 0:  # will start on 2nd coord
                    lat_in0 = float(readerList[prevIndex][0])  # previous latitude
                    lon_in0 = float(readerList[prevIndex][1])  # previous longitude
                    
                    east_out0, north_out0, zone, zone_quad = LL2utm(
                    lat_in0, lon_in0, datum=datum_in)
                    distance += distanceBetweenUTM(east_out0, north_out0, east_out1, north_out1)

                writer.writerow(
                    [lat_in1, lon_in1, east_out1, north_out1, zone, zone_quad, elevation, distance]
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
                east_out1, north_out1, zone, zone_quad = LL2utm(
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
                    east_out0, north_out0, zone, zone_quad = LL2utm(
                    lat_in0, lon_in0, datum=datum_in
                    )
                    distance += distanceBetweenUTM(east_out0, north_out0, east_out1, north_out1)
                
                # Write to output csv file
                writer.writerow(
                    [lat_in1, lon_in1, east_out1, north_out1, zone, zone_quad, elevation, distance]
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
            east_out1, north_out1, zone, zone_quad = LL2utm(
                lat_in1, lon_in1, datum=datum_in
            )

            prevIndex = lineCount - 2  # index of previous coord
            if prevIndex >= 0:  # will start on 2nd coord
                lat_in0 = float(KML_dataStructure[prevIndex]['Latitude'])  # previous latitude
                lon_in0 = float(KML_dataStructure[prevIndex]['Longitude'])  # previous longitude
                east_out0, north_out0, zone, zone_quad = LL2utm(
                    lat_in0, lon_in0, datum=datum_in)

                distance += distanceBetweenUTM(east_out0, north_out0, east_out1, north_out1)

            writer.writerow(
                [lat_in1, lon_in1, east_out1, north_out1, zone, zone_quad, elevation, distance]
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
