# Import dependecies

from bs4 import BeautifulSoup
import csv


def process_coordinate_string(str):    
    # Take the coordinate string from the KML file, and break it up into [Lat,Lon,Lat,Lon...] for a CSV row
    ret = []
    comma_split = str.split(',')
    return [comma_split[1], comma_split[0], comma_split[2]] #Return (lat, long, elevation)

def main():    
    # Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    # Make sure "profile.kml" or whatever the file is called is in the same directory
    with open('profile.kml', 'r') as f:
        s = BeautifulSoup(f, 'xml')
        with open('profile.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for coords in s.find_all('coordinates'):
                writer.writerow(process_coordinate_string(coords.string))

# Run the main method
main() 
