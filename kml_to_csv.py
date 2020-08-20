from bs4 import BeautifulSoup
import lxml


def process_coordinate_string(string):
    # take the coordinate string from the KML file, and break it up into [Lat,Lon,Lat,Lon...] for a CSV row
    comma_split = string.split(',')
    return {'Latitude': comma_split[1], 'Longitude': comma_split[0], 'Elevation (m)': comma_split[2]}


def kmlParser(Path):
    # Open the KML. Read the KML. Open a list. Process a coordinate string to be a dictionary item in said list.
    # Make sure "profile.kml" or whatever the file is called is in the same directory
    with open(Path, 'r') as f:
        s = BeautifulSoup(f, 'lxml')

        coordinateList = []

        for coords in s.find_all('coordinates'):
            coordinateList.append(process_coordinate_string(coords.string))

        return coordinateList   # data structure
