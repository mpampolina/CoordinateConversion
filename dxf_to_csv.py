import re

utmRegex = re.compile(r'''(AcDbPoint\n\s10\n(\d+\.\d+)\n\s20\n(\d+\.\d+)\n\s30\n(\d+\.\d+))
''', re.VERBOSE)


def dxfParser(Zone, Path):

    with open(Path, 'r') as myfile:
        data = myfile.read()    # reads in dxf.txt file and returns the data in string form

        data = utmRegex.findall(data)   # returns a list of tuples. Each tuple corresponds to a coordinate set

        coordinateList = []

        for entry in data:
            coordinates = {'utm_e': entry[1], 'utm_n': entry[2], 'utm_z': Zone, 'Elevation (m)': entry[3]}
            coordinateList.append(coordinates)

        return coordinateList   # data structure
