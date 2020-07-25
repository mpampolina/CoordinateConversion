# import dependencies

from bs4 import BeautifulSoup
import csv
import lxml
import os


def process_coordinate_string(string):
    # take the coordinate string from the KML file, and break it up into [Lat,Lon,Lat,Lon...] for a CSV row
    comma_split = string.split(',')
    return [comma_split[1], comma_split[0], comma_split[2]]     # return (lat, long, elevation)


def kmlParser(Path):
    # Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    # Make sure "profile.kml" or whatever the file is called is in the same directory
    with open(Path, 'r') as f:
        s = BeautifulSoup(f, 'lxml')
        with open('profile.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)

            # add header
            writer.writerow(['Latitude', 'Longitude', 'Elevation'])
            for coords in s.find_all('coordinates'):
                writer.writerow(process_coordinate_string(coords.string))

            scriptDirectory = os.getcwd()
            print(f'Conversion Complete. Please check [{scriptDirectory}] for the converted file.')

            print("Press Enter to continue ...")
            input()


def pathInput():
    print('KML to CSV Conversion Tool'.center(40, '='))
    print('\nTo start your conversion, please enter one of the following options:')
    print('\nOption-1: Please enter the path for your .kml file.')
    print('''\nOption-2: Ensure that the selected KML file is located in the same directory as this script and
please enter the filename for your .kml file.\n''')
    Path = input('Input: ')
    return Path


# Run the main method
if __name__ == "__main__":
    path = pathInput()
    kmlParser(path)
