from CoordinateConversion import LL2utm, utm2LL, getLLfromDMS, distanceBetweenLL, distanceBetweenUTM
import csv
import os
import sys


# Give & get filename for the csv file that needs to be converted, the conversion direction, and desired datum
def mainMenu():
    print('utm2LL and LL2utm  Conversion Tool'.center(40, '='))
    print('\nTo start your conversion, please enter one of the following options:')
    print('\nOption-1: Please enter the path for your .csv file.')
    print('''Option-2: Ensure that the selected csv file is located in the same directory as this script and 
please enter the filename for your .csv file (example: MyCoordinates.csv).\n''')

    filename = input('Input: ')


    while not os.path.isfile(filename):
        print('''\nThe file/path you entered does not exist. Please re-enter your desired file or path. If you would like to exit enter "quit" ''')
        filename = input('Input: ')
        if filename == 'quit':
            os._exit(1)

    print('\nWhat datum you would like to reference the conversion with (i.e. NAD 83, WGS 84 etc.:')
    datum_input = input('Input: ')
    
    print('''\nSelect the conversion direction:\n1. Lat/lon to UTM input -> LL2utm 
2. UTM to lat/lon input -> utm2LL\n3. Lat/Lon (DMS) to UTM input -> LLdms2utm\n''')
    conversionDirection = str(input('Input: '))
    
    conv_complete = False
    while not conv_complete:
        if conversionDirection == 'LL2utm':
            batch_LL2utm(filename, datum_input)
            conv_complete = True

        elif conversionDirection == 'utm2LL':
            print('What zone are the sets of UTM coordinates in: ')
            Zone = int(input('Input: '))

            print('What zone quadrant are the sets of UTM coordinates in? (ex. U) ')
            zoneQuad = str(input('Input: '))

            print('''Are the sets of UTM coordinates in the northern or southern hemisphere: Enter True for Northern 
    and False for Southern''')
            isNorth = bool(input('Input: '))

            batch_utm2LL(filename, datum_input, Zone, zoneQuad, isNorth)
            conv_complete = True

        elif conversionDirection == 'LLdms2utm':
            batch_dms2utm(filename, datum_input)
            conv_complete = True

        else:
            print('''\nNo valid conversion direction chosen please re-enter your desired direction. If you would like to terminate enter "quit" \n''')
            conversionDirection = str(input('Input: '))
            if conversionDirection == 'quit':
                os._exit(1)
            conv_complete = False

    if conv_complete:
        scriptDirectory = os.getcwd()
        print(f'Conversion Complete. Please check [{scriptDirectory}] for the converted file.')

    print("Press Enter to continue ...")
    input()


# Convert a CSV file of latitude and longitude coordinates to UTM
def batch_LL2utm(filename, datum_in):
    with open(filename) as f:                                                   # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=',')                                   # Generate a reader object from file
        with open('LL2utm_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude', 'Easting', 'Northing', 'Zone', 'Zone Quadrant'],)  # Write header
            next(reader)                                                                # Skip the reader object header

            readerList = list(reader)
            distance = 0
            for lineCount, coords in enumerate(readerList, start=1):
                lat_in1 = float(coords[0])
                lon_in1 = float(coords[1])
                east_out, north_out, zone, zone_quad = LL2utm(lat_in1, lon_in1, datum=datum_in)

                if lineCount < len(readerList):
                    lat_in2 = float(readerList[lineCount][0])   # next latitude
                    lon_in2 = float(readerList[lineCount][1])   # next longitude
                    distance += distanceBetweenLL(lat_in1, lon_in1, lat_in2, lon_in2)

                writer.writerow([lat_in1, lon_in1, east_out, north_out, zone, zone_quad])

            writer.writerow(['TotalDistance(km)', distance])
    print(f'\nConverted {lineCount} coordinates')
    print(f'\nTotal polyline distance travelled: {distance}km\n')


# Convert CSV file of latitude longitude coordinates in deg,min,sec (dms) notation to UTM
def batch_dms2utm(filename, datum_in):
    with open(filename) as f:                                                   # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=',')                                   # Generate a reader object from file
        with open('dms2utm_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude', 'Easting', 'Northing', 'Zone', 'Zone Quadrant'],)  # Write header
            next(reader)                                                                # Skip the reader object header

            for lineCount, coords in enumerate(reader, start=1):

                lat_in, lon_in = getLLfromDMS(float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3]),
                                              float(coords[4]), float(coords[5]))

                east_out, north_out, zone, zone_quad = LL2utm(lat_in, lon_in, datum=datum_in)

                writer.writerow([lat_in, lon_in, east_out, north_out, zone, zone_quad])
    print(f'\nConverted {lineCount} coordinates') 


# Convert a CSV file of UTM coordinates to latitude and longitude
def batch_utm2LL(filename, datum_in, zone, zoneQuadrant, is_north):
    with open(filename) as f:                                           # Open the UTM file from the dxf_to_csv parser
        reader = csv.reader(f, delimiter=',')                           # Generate a reader object from file
        with open('utm2LL_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude'],)                 # Write headers for the writer object
            next(reader)                                                # Skip the reader object header

            readerList = list(reader)
            distance = 0
            for lineCount, coords in enumerate(readerList, start=1):
                east_in1 = float(coords[0])
                north_in1 = float(coords[1])
                lat_out, lon_out = utm2LL(east_in1, north_in1, zone, zoneQuadrant=zoneQuadrant, North=is_north,
                                          datum=datum_in)

                if lineCount < len(readerList):
                    east_in2 = float(readerList[lineCount][0])      # next easting
                    north_in2 = float(readerList[lineCount][1])     # next northing
                    distance += distanceBetweenUTM(east_in1, north_in1, east_in2, north_in2)

                writer.writerow([lat_out, lon_out])

            writer.writerow(['TotalDistance(km)', distance])
    print(f'\nConverted {lineCount} coordinates')
    print(f'\nTotal polyline distance travelled: {distance}km\n')


# main    
if __name__ == "__main__":

    mainMenu()
