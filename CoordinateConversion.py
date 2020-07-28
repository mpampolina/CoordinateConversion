from math import sqrt, sin, cos, tan, atan, cosh, sinh, asinh, atanh,  floor, degrees, radians
from KruegerSeries import getAlphaSeries, getBetaSeries
import csv
import os

# CONSTANTS
k0 = 0.9996             # scale on central meridian
falseEasting = 5e5      # location of the zone meridian, placed at an arbitrary value of 500,000 m. E.
NorthQuadrants = ['N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
SouthQuadrants = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C']

# Datums are ordered (a, b), which refer to the characteristics of an ellipsoid
# a -> semi-major axis (distance from the vertex to center of an ellipse)
# b -> semi-minor axis (distance from the co-vertex or "short-distance" vertex to the center of an ellipse)

Datums = {
    'WGS 84': (6378137, 6356752.3142),
    'NAD 83': (6378137, 6356752.3142),
    'GRS 80': (6378137, 6356752.3141),
    'WGS 72': (6378135, 6356750.5),
    'Australian 1965': (6378160, 6356774.7),
    'Krasovsky 1940': (6378245, 6356863),
    'North American 1927': (6378206.4, 6356583.8),
    'International 1924': (6378388, 6356911.9),
    'Hayford 1909': (6378388, 6356911.9),
    'Clarke 1880': (6378249.1, 6356514.9),
    'Clarke 1866': (6378206.4, 6356583.8),
    'Airy 1830': (6377563.4, 6356256.9),
    'Bessel 1841': (6377397.2, 6356079),
    'Everest 1830': (6377276.3, 6356075.4)
}


def getDatumProperties(a, b):
    e = sqrt(1.0 - (b / a) ** 2.0)  # Eccentricity. Ellipses have 0 <= e < 1 counting perfect circles which have e = 0.
    n = (a - b) / (a + b)           # 3rd flattening or second derivative of the flattening factor f = (a-b) / a.

    # AA is the rectifying radius or scale of the ellipse. 2*pi*AA would be the circumference of the ellipse.
    AA = (a / (1 + n)) * (1 + (1 / 4) * n ** 2 + (1 / 64) * n ** 4 + (1 / 256) * n ** 6 + (25 / 16384) * n ** 8 + (
            49 / 65536) * n ** 10)

    return e, n, AA


def LL2utm(lat, long, datum='WGS 84'):
    a, b = Datums[datum]

    # latitude format alterations
    lat_rad = radians(abs(lat))

    zone, zone_cm = getZone(long)
    eastCM = isEastCM(long, zone_cm)    # 1 or -1
    zoneQuadrant = getZoneQuadrant(lat)

    # absolute difference between longitude (degrees) and central meridian of utm zone (degrees)
    relative_long = abs(long - zone_cm)
    relative_long_rad = radians(relative_long)

    e, n, AA = getDatumProperties(a, b)
    a1, a2, a3, a4, a5, a6, a7 = getAlphaSeries(n)  # (Krüger 1912, pg. 21, eqn. 41)

    # SOLUTION FOR LATITUDE BY NEWTON-RAPHSON ITERATION
    # (R.E. Deakin et. Al 2012,  pg. 13, eqn. 129-130) or (Karney 2010, pg. 2, eqn. 7-9)
    # a.k.a "newton's method"
    # "tau" = tan(lat_rad)
    sigma = sinh(e * atanh(e * tan(lat_rad) / sqrt(1 + tan(lat_rad) ** 2)))
    tau_prime = tan(lat_rad)*sqrt(1+sigma*sigma)-sigma*sqrt(1+tan(lat_rad)**2)

    # (Karney 2010, pg.2, eqn. 10)
    xi_prime = atan(tau_prime / cos(relative_long_rad))
    eta_prime = asinh(sin(relative_long_rad) / sqrt(tau_prime * tau_prime + (cos(relative_long_rad) ** 2)))

    # (Karney 2010, pg. 3, eqn. 11)
    xi = xi_prime + a1 * sin(2 * xi_prime) * cosh(2 * eta_prime) + a2 * sin(4 * xi_prime) * cosh(
        4 * eta_prime) + a3 * sin(6 * xi_prime) * cosh(6 * eta_prime) + a4 * sin(8 * xi_prime) * cosh(
        8 * eta_prime) + a5 * sin(10 * xi_prime) * cosh(10 * eta_prime) + a6 * sin(12 * xi_prime) * cosh(
        12 * eta_prime) + a7 * sin(14 * xi_prime) * cosh(14 * eta_prime)
    eta = eta_prime + a1 * cos(2 * xi_prime) * sinh(2 * eta_prime) + a2 * cos(4 * xi_prime) * sinh(
        4 * eta_prime) + a3 * cos(6 * xi_prime) * sinh(6 * eta_prime) + a4 * cos(8 * xi_prime) * sinh(
        8 * eta_prime) + a5 * cos(10 * xi_prime) * sinh(10 * eta_prime) + a6 * cos(12 * xi_prime) * sinh(
        12 * eta_prime) + a6 * cos(14 * xi_prime) * sinh(14 * eta_prime)

    # (Karney 2010, pg.3, eqn. 13)
    # Scale xi and eta by central meridian scale and the scale of the ellipse.
    relative_Easting = k0 * AA * eta
    relative_Northing = k0 * AA * xi

    # If the latitude is in the northern hemisphere, we know our relative northing = true northing.
    # Since, the equator is assigned an arbitrary value of 10,000,000 m. N., if our coordinates are
    # in the south, we need to subtract the relative northing from 10,000,000 m.
    if lat > 0:
        Northing = relative_Northing
    else:
        Northing = 1e7 - relative_Northing

    # Relative easting refers to how far east or west a coordinate is from the zone's central meridian
    # Relative easting is thus added/subtracted (controlled by "eastCM") from the false easting to give
    # a true easting value.
    Easting = falseEasting + relative_Easting * eastCM

    return Easting, Northing, zone, zoneQuadrant


def utm2LL(Easting, Northing, zone, zoneQuadrant=None, North=None, datum='WGS 84'):
    a, b = Datums[datum]
    zone_cm = getZoneCM(zone)           # zone central meridian in degrees longitude

    if zoneQuadrant:    # if both North and zoneQuadrant are specified, use zoneQuadrant to determine North
        North = isNorth(zoneQuadrant)
    elif North is None:
        raise Exception("Either 'zoneQuadrant' or 'North' arguments must be specified")

    e, n, AA = getDatumProperties(a, b)
    b1, b2, b3, b4, b5, b6, b7 = getBetaSeries(n)   # (Krüger 1912, pg. 21, eqn. 41)

    if North:
        xi = Northing / (k0 * AA)  # (Karney 2010, pg.3, eqn. 15)
    else:
        xi = Northing / (1e7 - Northing) / (k0 * AA)

    eta = (Easting - falseEasting) / (k0 * AA)     # (Karney 2010, pg.3, eqn. 13)

    # (Karney 2010, pg.3, eqn. 11) which is an inversion of (Karney 2010, pg. 2, eqn. 7-9)
    xi_prime = (xi - (
        b1 * sin(2 * xi) * cosh(2 * eta) + b2 * sin(4 * xi) * cosh(4 * eta) + b3 * sin(6 * xi) * cosh(
            6 * eta) + b4 * sin(8 * xi) * cosh(8 * eta) + b5 * sin(10 * xi) * cosh(10 * eta) + b6 * sin(
                12 * xi) * cosh(12 * eta) + b7 * sin(14 * xi) * cosh(14 * eta)))

    eta_prime = (eta - (
        b1 * cos(2 * xi) * sinh(2 * eta) + b2 * cos(4 * xi) * sinh(4 * eta) + b3 * cos(6 * xi) * sinh(
            6 * eta) + b4 * cos(8 * xi) * sinh(8 * eta) + b5 * cos(10 * xi) * sinh(10 * eta) + b6 * cos(
                12 * xi) * sinh(12 * eta) + b7 * cos(14 * xi) * sinh(14 * eta)))

    tau_prime = sin(xi_prime) / sqrt(sinh(eta_prime) ** 2 + cos(xi_prime) ** 2)
    relative_long_rad = atan(sinh(eta_prime) / cos(xi_prime))
    relative_long = degrees(relative_long_rad)  # longitude relative to central meridian

    # We are in a pickle here. Since tau is unknown and sigma is a function of tau, we need to use an approximation
    # for newton's method with a first guess for tau, say tau = tau_prime. With each iteration, f converges closer and
    # closer to zero and tau stabilizes. f should converge after 2-3 iterations, but other programs have used 7.
    # Likewise, we will be using 7 iterations.
    # source: [https: // stevedutch.net / usefuldata / utmformulas.htm] analogous to (Karney 2010, pg.3, eqn. 19-21)

    tau = tau_prime
    for iteration in range(7):
        sigma = sinh(e * atanh(e * tau / sqrt(1 + tau ** 2)))
        f_tau = tau * sqrt(1 + sigma ** 2) - sigma * sqrt(1 + tau ** 2) - tau_prime
        d_tau = (sqrt((1 + sigma ** 2) * (1 + tau ** 2)) - sigma * tau) * (1 - e ** 2) * sqrt(1 + tau ** 2) / (
                    1 + (1 - e ** 2) * tau ** 2)
        tau = tau - f_tau / d_tau

    lat = degrees(atan(tau))    # Return latitude back to degrees.

    if North:                   # Convert latitude to negative if South.
        lat = abs(lat)
    else:
        lat = abs(lat) * -1

    long = relative_long + zone_cm

    return lat, long


# Longitude range: -180 degrees <= long <= 180 degrees and is centered at the Greenwich
# Meridian located at 0 degrees longitude. UTM has a zone system from 0 degrees moving
# right from the IDL and 360 degrees moving right to the IDL. Each zone spans 6 degrees in
# width. To convert from longitude to zone, we have to add 180 degrees to the longitude to
# get the degrees right from the IDL. Then we then divide by 6 degrees to get the zone.
# Since UTM starts from zone 1 and each in between coordinates round down to the nearest
# zone we add 1. If the longitude is greater than 0 we still divide by 6, but instead
# add 31 to account for starting at 180 degrees right of the IDL
# (180/6 = 30 + 1 for the starting zone = 31)

def getZone(longitude):
    if longitude < 0:
        zone = int((180 + longitude) / 6) + 1
    else:
        zone = int(longitude / 6) + 31
    zone_cm = getZoneCM(zone)

    return zone, zone_cm


# Get the location of a zone's central meridian in degrees longitude.
# i.e. I'm in zone 31 (just east of the Greenwich Meridian).
# The central meridian for my zone is 6 * 31 - 183 = 3 degrees longitude.

def getZoneCM(zone):
    return 6 * zone - 183


# Returns a Boolean value reflecting whether a zone is located in the North or not
def isNorth(zoneQuadrant):
    if zoneQuadrant in NorthQuadrants:
        return True
    elif zoneQuadrant in SouthQuadrants:
        return False
    else:
        return None


# Will return 1 if the longitude degrees is greater than a zone's central meridian
# otherwise, return -1
def isEastCM(longitude, zone_cm):
    if longitude > zone_cm:
        eastCM = 1
    else:
        eastCM = -1
    return eastCM

# Zone quadrants are divided into degrees of 8 with the exception of zone quadrant X.
# To identify a given zone quadrant, we need to take the absolute value of the latitude
# and divide by 8 degrees to get the quadrant index number. Using our lookup lists, we
# can use our quadrant index to determine a given zone quadrant.


def getZoneQuadrant(latitude):
    quadrantIndex = floor(abs(latitude) / 8)
    if quadrantIndex > 0:
        zoneQuadrant = NorthQuadrants[quadrantIndex]
    else:
        zoneQuadrant = SouthQuadrants[quadrantIndex]
    return zoneQuadrant


# Returns 1 or -1 if a LL coordinate is (N, E) or (S, W) respectively
def getSign(lat, long):
    lat_sign = 1
    long_sign = 1
    if lat < 0:
        lat_sign = -1
    if long < 0:
        long_sign = -1
    return lat_sign, long_sign


# Takes DMS coordinates and converts to decimal degrees.
# (1 Degree : 60 Minutes)
# (1 Minute : 60 Seconds)
def getLLfromDMS(lat_deg, lat_min, lat_sec, long_deg, long_min, long_sec):
    lat_sign, long_sign = getSign(lat_deg, long_deg)
    latitude = (abs(lat_deg) + lat_min * 1/60 + lat_sec * 1/3600) * lat_sign
    longitude = (abs(long_deg) + long_min * 1/60 + long_sec * 1/3600) * long_sign
    return latitude, longitude


# Takes decimal degree coordinates and converts to latitude and longitude.
# floor() - automatically rounds down the argument value.
# round() - rounds the floored float into an integer value.
def getDMSfromLL(lat, long):
    lat_sign, long_sign = getSign(lat, long)

    lat_deg = round(floor(abs(lat))) * lat_sign
    lat_min = round(floor((60 * (abs(lat) - abs(lat_deg)))))
    lat_sec = 3600 * (abs(lat) - abs(lat_deg) - (lat_min / 60))

    long_deg = round(floor(abs(long))) * long_sign
    long_min = round(floor((60 * (abs(long) - abs(long_deg)))))
    long_sec = 3600 * (abs(long) - abs(long_deg) - (long_min/60))
    return (lat_deg, lat_min, lat_sec), (long_deg, long_min, long_sec)


# Give & get filename for the csv file that needs to be converted, the conversion direction, and desired datum
def fileInput():
    print('utm2LL and LL2utm  Conversion Tool'.center(40, '='))
    print('\nTo start your conversion, please enter one of the following options:')
    print('\nOption-1: Please enter the path for your .csv file.')
    print('''Option-2: Ensure that the selected csv file is located in the same directory as this script and 
please enter the filename for your .csv file (example: MyCoordinates.csv).\n''')
    filename = input('Input:')
    print('\nSelect the conversion direction:\n Lat/lon to UTM input -> LL2utm \n UTM to lat/lon input -> utm2LL')
    conversionDirection = str(input('Input: '))
    print('\nWhat datum you would like to reference the conversion with (i.e. NAD 83, WGS 84 etc.:')
    datum_in = input('Input:')
    return filename, conversionDirection, datum_in


# Convert a CSV file of latitude and longitude coordinates to UTM
def batch_LL2utm(filename, datum_in):
    with open(filename) as f:                                                   # Open Latitude/Longitude file
        reader = csv.reader(f, delimiter=',')                                   # Generate a reader object from file
        with open('LL2utm_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Easting', 'Northing', 'Zone', 'Zone Quadrant'],)  # Write headers for the writer object
            next(reader)                                                        # Skip the reader object header
            for lineCount, coords in enumerate(reader, start=1):
                # Record the lat/lon values in as floats and use these in the LL2utm method
                lat_in = float(coords[0])
                lon_in = float(coords[1])
                east_out, north_out, zone, zone_quad = LL2utm(lat_in, lon_in, datum=datum_in)
                writer.writerow([east_out, north_out, zone, zone_quad])
    print(f'Converted {lineCount} coordinates')


# Convert a CSV file of UTM coordinates to latitude and longitude
def batch_utm2LL(filename, datum_in, zone, zoneQuadrant, is_north):
    with open(filename) as f:                                           # Open the UTM file from the dxf_to_csv parser
        reader = csv.reader(f, delimiter=',')
        with open('utm2LL_out.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Latitude', 'Longitude'],)                 # Write headers for the writer object
            next(reader)                                                # Skip the reader object header
            for lineCount, coords in enumerate(reader, start=1):
                # Parse through all the rows of in the UTM coordinate file
                # For coordinate rows, record UTM values as floats and use them for the utm2LL method
                east_in = float(coords[0])
                north_in = float(coords[1])
                lat_out, lon_out = utm2LL(east_in, north_in, zone, zoneQuadrant=zoneQuadrant, North=is_north,
                                          datum=datum_in)
                writer.writerow([lat_out, lon_out])
    print(f'Converted {lineCount} coordinates')


if __name__ == "__main__":

    # Kobau 1 and 2 refer to geodetic control monuments with known Latitude and Longitude + UTM values
    # Overall with testing, the CoordinateConversion implementation of Karney's (2010) algorithm is within tenths
    # of a millimeter of the true easting values and within 2 millimeters of the true northing values. This
    # implementation also has a tendency to underestimate by 1 millimeter on the Northing side, likely due to
    # accruing a significant amount of floating point error over the course of the calculations.

    test = False
    if test:
        Latitude, Longitude = getLLfromDMS(49, 6, 57.31599, -119, 40, 33.63357)
        print(f"Kobau 1 Latitude, Longitude - {Latitude, Longitude}")
        print(f"Kobau 1 conversion to UTM (Easting, Northing) - {LL2utm(Latitude, Longitude, datum='WGS 84')}")
        print(f"Kobau 1 true values (Easting, Northing) - (304734.658, 5443790.965)")
        print(f"Kobau 1 conversion to UTM and back {utm2LL(*LL2utm(Latitude, Longitude, datum='WGS 84'))}")

        print("\n")

        Latitude, Longitude = getLLfromDMS(49, 6, 50.67477, -119, 40, 24.04625)
        print(f"Kobau 2 Latitude, Longitude - {Latitude, Longitude}")
        print(f"Kobau 2 conversion to UTM (Easting, Northing) - {LL2utm(Latitude, Longitude, datum='WGS 84')}")
        print(f"Kobau 1 true values (Easting, Northing) - (304921.726, 5443579.054)")
        print(f"Kobau 2 conversion to UTM and back {utm2LL(*LL2utm(Latitude, Longitude, datum='WGS 84'))}")
    
    # Record the filename or path input, the conversion direction, and the datum used
    Filename, convDir, datum_input = fileInput()
    
    # Determine which batch conversion to use
    if convDir == 'LL2utm':
        batch_LL2utm(Filename, datum_input)
    elif convDir == 'utm2LL':
        print('What zone are the sets of UTM coordinates in: ')
        Zone = int(input('Input:'))
        print('\nWhat zone quadrant are the sets of UTM coordinates in? (ex. U) ')
        zoneQuad = str(input('Input:'))
        print('''\nAre the sets of UTM coordinates in the northern or southern hemisphere: Enter True for Northern 
        and False for Southern''')
        isNorth = bool(input('Input:'))
        batch_utm2LL(Filename, datum_input, Zone, zoneQuad, isNorth)
    
    scriptDirectory = os.getcwd()
    print(f'Conversion Complete. Please check [{scriptDirectory}] for the converted file.')

    print("Press Enter to continue ...")
    input()
