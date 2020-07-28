import csv
import re
import os

utmRegex = re.compile(r'''(AcDbPoint\n\s10\n(\d+\.\d+)\n\s20\n(\d+\.\d+)\n\s30\n(\d+\.\d+))
''', re.VERBOSE)


def dxfParser(Path, Filename):
    outputFilename = Filename + '_dxf_converted.csv'
    with open(Path, 'r') as myfile:
        data = myfile.read()    # reads in dxf.txt file and returns the data in string form

        data = utmRegex.findall(data)   # returns a list of tuples. Each tuple corresponds to a coordinate set

        coordinateList = []

        for entry in data:
            coordinates = {'Easting': entry[1], 'Northing': entry[2], 'Elevation': entry[3]}
            coordinateList.append(coordinates)

        with open(outputFilename, 'w', newline='') as csvFile:
            fieldnames = ['Easting', 'Northing', 'Elevation']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

            writer.writeheader()
            for coordindateDict in coordinateList:
                writer.writerow(coordindateDict)

        scriptDirectory = os.getcwd()
        print(f'Conversion Complete. Please check [{scriptDirectory}] for the converted file.')

        print("Press Enter to continue ...")
        input()


def pathInput():
    print('DXF to CSV Conversion Tool'.center(40, '='))
    print('\nTo start your conversion, please enter one of the following options:')
    print('\nOption-1: Please enter the path for your .dxf file.')
    print('''\nOption-2: Ensure that the selected DXF file is located in the same directory as this script and
please enter the filename for your .dxf file.\n''')
    Path = input('Input:')
    while not os.path.isfile(Path):
        print('Your selected path either does not exist or is not a file. Please try again.')
        Path = input('Input:')
    Filename = os.path.basename(Path)
    Filename = Filename.split('.')[0]
    return Path, Filename


if __name__ == "__main__":
    path, filename = pathInput()
    dxfParser(path, filename)
