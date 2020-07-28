from CoordinateConversion import LL2utm, utm2LL, getLLfromDMS
import csv
import os


# Give & get filename for the csv file that needs to be converted, the conversion direction, and desired datum
def fileInput():
    print('utm2LL and LL2utm  Conversion Tool'.center(40, '='))
    print('\nTo start your conversion, please enter one of the following options:')
    print('\nOption-1: Please enter the path for your .csv file.')
    print('''Option-2: Ensure that the selected csv file is located in the same directory as this script and 
    please enter the filename for your .csv file (example: MyCoordinates.csv).\n''')
    filename = input('Input: ')
    print('\nSelect the conversion direction:\n Lat/lon to UTM input -> LL2utm \n UTM to lat/lon input -> utm2LL\n Lat/Lon (DMS) to UTM input -> LLdms2utm\n')
    conversionDirection = str(input('Input: '))
    print('\nWhat datum you would like to reference the conversion with (i.e. NAD 83, WGS 84 etc.:')
    datum_in = input('Input: ')
    return filename, conversionDirection, datum_in


# Convert a CSV file of latitude and longitude coordinates to UTM
def batch_LL2utm(filename, datum_in):
    with open(filename) as f:                                                   # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=',')                                   # Generate a reader object from file
        with open('LL_to_Utm_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude', 'Easting', 'Northing', 'Zone', 'Zone Quadrant'],)  # Write headers for the writer object
            next(reader)                                                        # Skip the reader object header
            for lineCount, coords in enumerate(reader, start=1):
                # Record the lat/lon values in as floats and use these in the LL2utm method
                lat_in = float(coords[0])
                lon_in = float(coords[1])
                east_out, north_out, zone, zone_quad = LL2utm(lat_in, lon_in, datum=datum_in)
                writer.writerow([lat_in, lon_in, east_out, north_out, zone, zone_quad])
    print(f'\nConverted {lineCount} coordinates')


# Convert CSV file of latitude longitude coordaintes in Deg,min,sec to UTM
def batch_LLdms2utm(filename, datum_in):
    with open(filename) as f:                                                   # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=',')                                   # Generate a reader object from file
        with open('LLdms_to_Utm_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude', 'Easting', 'Northing', 'Zone', 'Zone Quadrant'],)  # Write headers for the writer object
            next(reader)                                                        # Skip the reader object header
            for lineCount, coords in enumerate(reader, start=1):
                # Parse through all the rows of in the LatLon coordinate file
                # Collect the DMS values and convert to degrees (lat,lon) for each row
                lat_in, lon_in = getLLfromDMS(float(coords[0]), float(coords[1]), float(coords[2]),float(coords[3]), float(coords[4]), float(coords[5])) 
                east_out, north_out, zone, zone_quad = LL2utm(lat_in, lon_in, datum=datum_in)
                writer.writerow([lat_in, lon_in, east_out, north_out, zone, zone_quad])
    print(f'\nConverted {lineCount} coordinates') 

# Convert a CSV file of UTM coordinates to latitude and longitude
def batch_utm2LL(filename, datum_in, zone, zoneQuadrant, is_north):
    with open(filename) as f:                                           # Open the UTM file from the dxf_to_csv parser
        reader = csv.reader(f, delimiter=',')
        with open('utm_to_LL_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude'],)                 # Write headers for the writer object
            next(reader)                                                # Skip the reader object header
            for lineCount, coords in enumerate(reader, start=1):
                # Parse through all the rows of in the UTM coordinate file
                # For coordinate rows, record UTM values as floats and use them for the utm2LL method
                east_in = float(coords[0])
                north_in = float(coords[1])
                lat_out, lon_out = utm2LL(east_in, north_in, zone, zoneQuadrant=zoneQuadrant, North=is_north, datum=datum_in)
                writer.writerow([lat_out, lon_out])
    print(f'\nConverted {lineCount} coordinates')

# main    
if __name__ == "__main__":

    # Record the filename or path input, the conversion direction, and the datum used
    Filename, convDir, datum_input = fileInput()
    
    # Determine which batch conversion to use
    if convDir == 'LL2utm':
        batch_LL2utm(Filename, datum_input)
        conv_complete = True
    elif convDir == 'utm2LL':
        print('What zone are the sets of UTM coordinates in: ')
        Zone = int(input('Input: '))
        print('\nWhat zone quadrant are the sets of UTM coordinates in? (ex. U) ')
        zoneQuad = str(input('Input: '))
        print('''\nAre the sets of UTM coordinates in the northern or southern hemisphere: Enter True for Northern 
        and False for Southern''')
        isNorth = bool(input('Input: '))
        batch_utm2LL(Filename, datum_input, Zone, zoneQuad, isNorth)
        conv_complete = True
    elif convDir == 'LLdms2utm':
        batch_LLdms2utm(Filename, datum_input)
        conv_complete = True
    else:
        print('No valid conversion direction chosen please re-run the script\n')
        conv_complete = False
        
    if conv_complete:
        scriptDirectory = os.getcwd()
        print(f'Conversion Complete. Please check [{scriptDirectory}] for the converted file.')

    print("Press Enter to continue ...")
    input()