from CoordinateConversion import LL2utm, utm2LL, getLLfromDMS
from utils import get_datum, get_ConversionDirection
import sys


def menu():

    datum = get_datum()
    
    print('\nTo continue, enter one of the three conversion options:\n')
    conv_dir = get_ConversionDirection()

    if conv_dir.casefold() == 'll2utm':
        Lat = float(input('\nThe latitude is: '))
        Lon = float(input('The longitude is: '))
        print(f"\nConversion to UTM (Easting, Northing) - {LL2utm(Lat, Lon, datum)}")
        
    elif conv_dir.casefold() == 'lldms2utm':
        print('\nEnter your coordinates in deg min sec; all space delimited')
        s = input('The latitude is: ')
        lat = list(map(float, s.split()))
        s = input('The longitude is: ')
        lon = list(map(float, s.split()))

        lat_decDeg, lon_decDeg = getLLfromDMS(lat[0], lat[1], lat[2], lon[0], lon[1], lon[2])
        print(f"Conversion to UTM (Easting, Northing) - {LL2utm(lat_decDeg, lon_decDeg, datum)}")

    elif conv_dir.casefold() == 'utm2ll':
        easting = float(input('\nThe Easting is: '))
        northing = float(input('The Northing is: '))
        
        print('\nWhat zone are the sets of UTM coordinates in: ')
        zone = int(input('Input: '))
        
        print('\nWhat zone quadrant are the sets of UTM coordinates in? (ex. U)')
        zoneQuad = str(input('Input: '))
        
        print('''\nAre the sets of UTM coordinates in the northern or southern hemisphere: Enter True for Northern 
and False for Southern''')
        isNorth = bool(input('Input: '))  
        
        print(f"\nConversion to Lat/Lon (Lat, Lon) - {utm2LL(easting, northing, zone, zoneQuad, isNorth, datum)}")

    else:
        print('''\nNo valid conversion direction chosen please re-enter your desired direction.
If you would like to terminate enter "quit" \n''')
        conv_dir = get_ConversionDirection()
        if conv_dir.casefold() == 'quit':
            sys.exit()


if __name__ == "__main__":
    Run = True
    print('\nWelcome to a Coordinate Conversion Tool'.center(40, '='))

    while Run:
        menu()
        print('\nTo convert again press enter. To terminate type and submit: "quit".')

        if input().casefold() == 'quit':
            Run = False
