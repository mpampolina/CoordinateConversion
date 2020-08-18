import csv
import re
import os
from BatchConversions import get_file

utmRegex = re.compile(r'''(AcDbPoint\n\s10\n(\d+\.\d+)\n\s20\n(\d+\.\d+)\n\s30\n(\d+\.\d+))
''', re.VERBOSE)


def dxfParser(zone, Filename):
    outputFilename = Filename.split('.')[0] + '_dxf_converted.csv' # File name is original file + string
    
    with open(Filename, 'r') as myfile:
        data = myfile.read()    # reads in dxf.txt file and returns the data in string form

        data = utmRegex.findall(data)   # returns a list of tuples. Each tuple corresponds to a coordinate set

        coordinateList = []

        for entry in data:
            coordinates = {'Easting': entry[1], 'Northing': entry[2], 'Zone': zone, 'Elevation': entry[3]} # Structure of each csv line
            coordinateList.append(coordinates)

        with open(outputFilename, 'w', newline='') as csvFile:
            fieldnames = ['Easting', 'Northing', 'Zone', 'Elevation']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

            writer.writeheader()
            for coordindateDict in coordinateList:
                writer.writerow(coordindateDict)

        scriptDirectory = os.getcwd()
        print(f'\nConversion Complete. Please check [{scriptDirectory}] for the converted file.')

        print("Press Enter to continue ...")
        input()

def get_zone():
    print('\nWhat zone are the coordinates in this dxf file from?')
    return int(input('\nInput: '))

if __name__ == "__main__":
    filename = get_file()
    zone = get_zone()
    dxfParser(zone, filename)
