import csv
import re
import os
from BatchConversions import get_path, get_outputfilename
from SingularConversionElevation import zoneValidation

utmRegex = re.compile(r'''(AcDbPoint\n\s10\n(\d+\.\d+)\n\s20\n(\d+\.\d+)\n\s30\n(\d+\.\d+))
''', re.VERBOSE)


def dxfParser(zone, path):
    
    outputFilename = get_outputfilename()

    with open(path, 'r') as myfile:
        data = myfile.read()    # reads in dxf.txt file and returns the data in string form

        data = utmRegex.findall(data)   # returns a list of tuples. Each tuple corresponds to a coordinate set

        coordinateList = []

        for entry in data:
            coordinates = {'utm_e': entry[1], 'utm_n': entry[2], 'utm_z': zone, 'Elevation (m)': entry[3]} # Structure of each csv line
            coordinateList.append(coordinates)

        with open(outputFilename, 'w', newline='') as csvFile:
            fieldnames = ['utm_e', 'utm_n', 'utm_z', 'Elevation (m)']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

            writer.writeheader()
            for coordindateDict in coordinateList:
                writer.writerow(coordindateDict)

        scriptDirectory = os.getcwd()
        print(f'\nConversion Complete. Please check [{scriptDirectory}] for the converted file.')

        print("Press Enter to continue ...")
        input()


if __name__ == "__main__":
    path = get_path()
    zone = zoneValidation()
    dxfParser(zone, path)
