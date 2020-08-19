# import dependencies
from bs4 import BeautifulSoup
import csv
import lxml
import os
from BatchConversions import get_path, get_outputfilename


def process_coordinate_string(string):
    # take the coordinate string from the KML file, and break it up into [Lat,Lon,Lat,Lon...] for a CSV row
    comma_split = string.split(',')
    return [comma_split[1], comma_split[0], comma_split[2]]     # return (lat, long, elevation)


def kmlParser(path):
    # Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    # Make sure "profile.kml" or whatever the file is called is in the same directory
    outputFilename = get_outputfilename()
    with open(path, 'r') as f:
        s = BeautifulSoup(f, 'lxml')
        with open(outputFilename, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)

            # add header
            writer.writerow(['Latitude', 'Longitude', 'Elevation'])
            for coords in s.find_all('coordinates'):
                writer.writerow(process_coordinate_string(coords.string))

            scriptDirectory = os.getcwd()
            print(f'\nConversion Complete. Please check [{scriptDirectory}] for the converted file.')

            print("Press Enter to continue ...")
            input()


if __name__ == "__main__":
    path = get_path()
    kmlParser(path)
