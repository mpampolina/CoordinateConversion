from bs4 import BeautifulSoup
import lxml
import re
import csv
import os
import sys


utmRegex = re.compile(r'''(AcDbPoint\n\s10\n(\d+\.\d+)\n\s20\n(\d+\.\d+)\n\s30\n(\d+\.\d+))
''', re.VERBOSE)

# Creates strucutre for the dxf to be converted
def dxfParser(Zone, Path):

    with open(Path, 'r') as myfile:
        data = myfile.read()    # reads in dxf.txt file and returns the data in string form

        data = utmRegex.findall(data)   # returns a list of tuples. Each tuple corresponds to a coordinate set

        coordinateList = []

        for entry in data:
            coordinates = {'utm_e': entry[1], 'utm_n': entry[2], 'utm_z': Zone, 'Elevation (m)': entry[3]}
            coordinateList.append(coordinates)

        return coordinateList   # data structure


# Process the coordinates to the structure
def process_coordinate_string(string):
    # take the coordinate string from the KML file, and break it up into [Lat,Lon,Lat,Lon...] for a CSV row
    comma_split = string.split(',')
    return {'Latitude': comma_split[1], 'Longitude': comma_split[0], 'Elevation (m)': comma_split[2]}

# Parse .kml file creating structure to be converted (csv struct lat,lon,elevation)
def kmlParser(Path):
    # Open the KML. Read the KML. Open a list. Process a coordinate string to be a dictionary item in said list.
    # Make sure "profile.kml" or whatever the file is called is in the same directory
    with open(Path, 'r') as f:
        s = BeautifulSoup(f, 'lxml')

        coordinateList = []

        for coords in s.find_all('coordinates'):
            coordinateList.append(process_coordinate_string(coords.string))

        return coordinateList   # data structure


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


# Gets datum
def get_datum():
    print(
        "\nWhat datum you would like to reference the conversion with (i.e. NAD 83, WGS 84 etc.):\n"
    )
    datum = input("Input: ").lower().replace(" ", "")
    return datum


# Method returns the conversion direction as a string
def get_ConversionDirection():
    print(
        """\nSelect the conversion direction:
    1. Lat/lon to UTM input         -> LL2utm
    2. UTM to lat/lon input         -> utm2LL
    3. Lat/Lon (DMS) to UTM input   -> LLdms2utm
    4. KML (lat/lon) to UTM input   -> kml2utm
    5. DXF (utm) to lat/lon input   -> dxf2LL"""
    )
    conv_dir = str(input("\nInput: ")).lower().replace(" ","")
    return conv_dir


# Method prompts user for inputs when converting from utm to lat/lon returning the results
def utm_prompts():
    print("\nWhat zone are the sets of UTM coordinates in: \n")
    Zone = int(input("Input: "))

    print("\nWhat zone quadrant are the sets of UTM coordinates in? (ex. U)\n")
    zoneQuadrant = str(input("Input: ")).upper()

    print('\nAre the sets of UTM coordinates in the northern or southern hemisphere:')
    print('Enter True for Northern and False for Southern\n')
    isNorth = bool(input('Input: '))

    return Zone, zoneQuadrant, isNorth


# Get the output filename as a strign
def get_outputfilename():
    print("\nWhat would you like to name your output file? (ex. myfile)")
    outputFilename = str(input("\nInput: ")) + '.csv' # Create output file name
    return outputFilename


# Gets the vertical datum and checks if choice is valid
def get_vertical_Datum(verb):
    epoch = False
    print(f'\nSpecify your {verb} orthometric datum: "CGVD28" or "CGVD2013"')
    datum = choiceValidation(["CGVD28", "CGVD2013"], "\nDatum: ")
    if datum == "CGVD2013":
        epoch = True
    return datum, epoch


# method checks to see if the choice is valid
def choiceValidation(choiceList, inputMessage="Input: "):
    while True:
        choice = input(inputMessage).upper().replace(" ", "")
        if choice not in choiceList:
            print("\nInvalid Option. Please Try again.")
        else:
            break
    return choice


# Method checks if the input is a number
def numericValidation(inputMessage="Input: "):
    while True:
        value = input(inputMessage)
        try:
            float(value)
            break
        except ValueError:
            print("Invalid Input. Input is not numeric.")
            continue
    return value


# Method checks if the utm zone is valid
def zoneValidation(inputMessage="Zone: "):
    while True:
        value = input(inputMessage)
        if 1 <= int(float(value)) <= 60:
            break
        else:
            print("Invalid Zone. Please try again.")
            continue
    return value
