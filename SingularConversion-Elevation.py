from bs4 import BeautifulSoup
import lxml
import requests
from dataclasses import dataclass

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

baseURL = "https://webapp.geod.nrcan.gc.ca/CSRS/tools/GPSH/"

geoidOptions = {
    "CGVD28_to_CGVD2013": "HT2_2010_to_CGG2013a",
    "CGVD2013_to_CGVD28": "CGG2013a_HT2_2010",
    "CGVD28": "HT2_2010v70",
    "CGVD2013": "CGG2013a",
}

interface = {
    "LL": ("latitude", "longitude", "elevation"),
    "UTM": ("northing", "easting", "elevation", "zone"),
}


@dataclass
class Query:
    proj: str
    datum: str
    c_model: str
    model: str
    zone: str
    x: str
    y: str
    z: str
    conversion: bool = False
    hmode: bool = False
    epoch: bool = False

    def buildQuery(self):
        Q = {
            "lang": "en",
            "proj": self.proj,
            "conversionModel": geoidOptions[self.c_model],
            "destdatum": self.datum,
            "geoidModel": geoidOptions[self.datum],
            "model": geoidOptions[self.model],
            "frame": "NAD83%28CSRS%29",
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }
        if self.zone:
            Q.update({"zone": "UTM" + self.zone})
        if self.conversion:
            Q.update({"conversion": "on"})
        if self.hmode:
            Q.update({"hmode": "on"})
        if self.epoch:
            Q.update({"epoch": "2010-01-01"})

        url = baseURL + geoidOptions[self.model] + "?"
        return Q, url


def menu():

    print("Welcome to the CGVD28 to CGVD2013 Conversion Tool".center(59, "="))

    print(
        '''Are you converting: \n1. From elevation (CGVD28) to  elevation (CGVD2013) -> Enter "1"
2. From elevation (CGVD2013) to elevation (CGVD28) -> Enter "2"
3. From an Ellipsoidal Elevation to an Orthometric Elevation -> Enter "3"
4. From an Orthometric Elevation to an Ellipsoidal Elevation -> Enter "4"'''
    )
    conv_direction = choiceValidation(["1", "2", "3", "4"], "Conversion Direction: ")

    conversion = False
    hmode = False
    epoch = False

    if int(conv_direction) == 1 or int(conv_direction) == 2:

        conversion = True

        if int(conv_direction) == 1:
            datum = "CGVD28"
            c_model = "CGVD28_to_CGVD2013"

        else:
            datum = "CGVD2013"
            c_model = "CGVD2013_to_CGVD28"

        model = c_model

    else:

        if int(conv_direction) == 3:
            verb = "output"
            c_model = "CGVD28_to_CGVD2013"

        else:
            hmode = True
            verb = "input"
            c_model = "CGVD28_to_CGVD2013"

        datum, epoch = getDatum(verb)
        model = datum

    print(
        '''\nPlease select your location system.\n1. Latitude/Longitude -> Enter "LL"
2. Universal Transverse Mercator (UTM) -> Enter "UTM"'''
    )
    locSys = choiceValidation(["LL", "UTM"], "Location System: ")

    if locSys == "LL":

        proj = "geo"
        zone = None

        print("\nPlease input your latitude (decimal degrees).")
        x = numericValidation("Latitude: ")

        print("\nPlease input your longitude (decimal degrees).")
        y = numericValidation("Longitude: ")

    else:

        proj = "plan"

        print("\nPlease input your Easting (m).")
        x = numericValidation("Easting: ")

        print("\nPlease input your Northing (m).")
        y = numericValidation("Northing: ")

        print("\nPlease input your Zone.")
        zone = zoneValidation()

    print("\nPlease input your elevation (m).")
    z = numericValidation("Elevation: ")

    query = Query(proj, datum, c_model, model, zone, x, y, z, conversion, hmode, epoch)

    getHeight(query)


def choiceValidation(choiceList, inputMessage="Input: "):
    while True:
        choice = input(inputMessage).replace(" ", "")
        if choice not in choiceList:
            print("Invalid Option. Please Try again.")
        else:
            break
    return choice


def numericValidation(inputMessage="Input: "):
    while True:
        value = input(inputMessage)
        try:
            float(value)
            break
        except ValueError:
            print("Invalid Input. Input is not numeric.")
            continue
    return value


def zoneValidation(inputMessage="Zone: "):
    while True:
        value = input(inputMessage)
        if 1 <= int(float(value)) <= 60:
            break
        else:
            print("Invalid Zone. Please try again.")
            continue
    return value


def getDatum(verb):
    epoch = False
    print(f'\nSpecify your {verb} orthometric datum: "CGVD28" or "CGVD2013"')
    datum = choiceValidation(["CGVD28", "CGVD2013"], "Datum: ")
    if datum == "CGVD2013":
        epoch = True
    return datum, epoch


# he = H28 height in m
# ho = H2013 height in m
# n = Offset (or dH) in m
def getHeight(query):

    params, url = query.buildQuery()

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    locSys = "LL"
    if query.zone:
        locSys = "UTM"

    print("\n")
    print("OUTPUT".center(10, "="))
    print(
        f"Point: {interface[locSys][0]} {query.x} | {interface[locSys][1]} {query.y} | {interface[locSys][2]} {query.z}"
    )
    if query.conversion:
        H28, H2013, offset = tuple(map(lambda x: soup.find(x).text, ["he", "ho", "n"]))
        print(
            f"CGVD28 datum height: {H28}m | CGVD2013 datum height: {H2013}m | Height Difference: {offset}m"
        )
    elif query.hmode:
        H_ellipse = soup.find("he").text
        print(f"Equivalent Ellipsoidal Height: {H_ellipse}m")
    else:
        H_ortho = soup.find("ho").text
        print(f"Equivalent Orthometric Height ({query.datum}): {H_ortho}m")


if __name__ == "__main__":
    menu()
