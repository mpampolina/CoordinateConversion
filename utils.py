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
    conv_dir = str(input("\nInput: ")).lower().replace(" ", "")
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
    outputFilename = input("\nInput: ").split('.')[0] + '.csv'   # generate output file name as csv regardless of ext
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


def getAlphaSeries(n):
    a1 = ((1 / 2) * n - (2 / 3) * n ** 2 + (5 / 16) * n ** 3 + (41 / 180) * n ** 4 - (127 / 288) * n ** 5 + (
            7891 / 37800) * n ** 6 + (72161 / 387072) * n ** 7
          - (18975107 / 50803200) * n ** 8 + (60193001 / 290304000) * n ** 9 + (134592031 / 1026432000) * n ** 10)
    a2 = ((13 / 48) * n ** 2 - (3 / 5) * n ** 3 + (557 / 1440) * n ** 4 + (281 / 630) * n ** 5 - (
            1983433 / 1935360) * n ** 6 + (13769 / 28800) * n ** 7 +
          (148003883 / 174182400) * n ** 8 - (705286231 / 465696000) * n ** 9 + (
                  1703267974087 / 3218890752000) * n ** 10)
    a3 = ((61 / 240) * n ** 3 - (103 / 140) * n ** 4 + (15061 / 26880) * n ** 5 + (167603 / 181440) * n ** 6 - (
            67102379 / 29030400) * n ** 7 +
          (79682431 / 79833600) * n ** 8 + (6304945039 / 2128896000) * n ** 9 - (
                  6601904925257 / 1307674368000) * n ** 10)
    a4 = ((49561 / 161280) * n ** 4 - (179 / 168) * n ** 5 + (6601661 / 7257600) * n ** 6 + (97445 / 49896) * n ** 7 -
          (40176129013 / 7664025600) * n ** 8 + (138471097 / 66528000) * n ** 9 + (
                  48087451385201 / 5230697472000) * n ** 10)
    a5 = ((34729 / 80640) * n ** 5 - (3418889 / 1995840) * n ** 6 + (14644087 / 9123840) * n ** 7 + (
            2605413599 / 622702080) * n ** 8 -
          (31015475399 / 2583060480) * n ** 9 + (5820486440369 / 1307674368000) * n ** 10)
    a6 = ((212378941 / 319334400) * n ** 6 - (30705481 / 10378368) * n ** 7 + (175214326799 / 58118860800) * n ** 8 +
          (870492877 / 96096000) * n ** 9 - (1328004581729000 / 47823519744000) * n ** 10)
    a7 = ((1522256789 / 1383782400) * n ** 7 - (16759934899 / 3113510400) * n ** 8 + (
            1315149374443 / 221405184000) * n ** 9 +
          (71809987837451 / 3629463552000) * n ** 10)

    return a1, a2, a3, a4, a5, a6, a7


def getBetaSeries(n):
    b1 = ((1 / 2) * n - (2 / 3) * n ** 2 + (37 / 96) * n ** 3 - (1 / 360) * n ** 4 - (81 / 512) * n ** 5 + (
                96199 / 604800) * n ** 6 - (5406467 / 38707200) * n ** 7 +
          (7944359 / 67737600) * n ** 8 - (7378753979 / 97542144000) * n ** 9 + (25123531261 / 804722688000) * n ** 10)
    b2 = ((1 / 48) * n ** 2 + (1 / 15) * n ** 3 - (437 / 1440) * n ** 4 + (46 / 105) * n ** 5 - (
                1118711 / 3870720) * n ** 6 + (51841 / 1209600) * n ** 7 +
          (24749483 / 348364800) * n ** 8 - (115295683 / 1397088000) * n ** 9 + (
                      5487737251099 / 51502252032000) * n ** 10)
    b3 = ((17 / 480) * n ** 3 - (37 / 840) * n ** 4 - (209 / 4480) * n ** 5 + (5569 / 90720) * n ** 6 + (
                9261899 / 58060800) * n ** 7 -
          (6457463 / 17740800) * n ** 8 + (2473691167 / 9289728000) * n ** 9 - (
                      852549456029 / 20922789888000) * n ** 10)
    b4 = ((4397 / 161280) * n ** 4 - (11 / 504) * n ** 5 - (830251 / 7257600) * n ** 6 + (466511 / 2494800) * n ** 7 + (
                324154477 / 7664025600) * n ** 8
          - (937932223 / 3891888000) * n ** 9 - (89112264211 / 5230697472000) * n ** 10)
    b5 = ((4583 / 161280) * n ** 5 - (108847 / 3991680) * n ** 6 - (8005831 / 63866880) * n ** 7 + (
                22894433 / 124540416) * n ** 8 +
          (112731569449 / 557941063680) * n ** 9 - (5391039814733 / 10461394944000) * n ** 10)
    b6 = ((20648693 / 638668800) * n ** 6 - (16363163 / 518918400) * n ** 7 - (2204645983 / 12915302400) * n ** 8 +
          (4543317553 / 18162144000) * n ** 9 + (54894890298749 / 167382319104000) * n ** 10)
    b7 = ((219941297 / 5535129600) * n ** 7 - (497323811 / 12454041600) * n ** 8 - (
                79431132943 / 332107776000) * n ** 9 +
          (4346429528407 / 12703122432000) * n ** 10)

    return b1, b2, b3, b4, b5, b6, b7
