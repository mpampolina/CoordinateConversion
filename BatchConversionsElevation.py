from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from SingularConversionElevation import choiceValidation, getDatum, geoidOptions
import os
import time
import sys


url = "https://webapp.geod.nrcan.gc.ca/geod/tools-outils/gpsh.php"
BatchProcessing_XP = '//*[@id="batchMode"]'
Convert_XP = '//*[@id="batchConversionBox"]'
Conversion_XP = '//*[@id="batchconversionModel"]'
ChooseFile_XP = '//*[@id="file"]'
SendFile_XP = '//*[@id="batchgpshform"]/div[4]/input'
VerticalDatum_XP = '//*[@id="batchdestdatum"]'


def menu():

    print("Welcome to the CGVD28 to CGVD2013 Conversion Tool".center(59, "="))

    print(
        '''Are you converting: \n1. From elevation (CGVD28) to  elevation (CGVD2013) -> Enter "1"
2. From elevation (CGVD2013) to elevation (CGVD28) -> Enter "2"
3. From an Ellipsoidal Elevation to an Orthometric Elevation -> Enter "3"
4. From an Orthometric Elevation to an Ellipsoidal Elevation -> Enter "4"'''
    )
    conv_direction = choiceValidation(["1", "2", "3", "4"], "Conversion Direction: ")

    convert = False

    if int(conv_direction) == 1 or int(conv_direction) == 2:

        convert = True

        if int(conv_direction) == 1:
            value = "CGVD28_to_CGVD2013"

        else:
            value = "CGVD2013_to_CGVD28"

    else:

        if int(conv_direction) == 3:
            verb = "output"

        else:
            verb = "input"

        value, _ = getDatum(verb)

    filename = getFilename()

    batchProcessing(convert, value, filename)


def batchProcessing(convert, value, filename):

    # options to ignore SSL error code 1
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    browser = webdriver.Chrome(chrome_options=options)
    browser.implicitly_wait(15)

    browser.get(url)
    browser.find_element_by_xpath(BatchProcessing_XP).click()

    if convert:
        browser.find_element_by_xpath(Convert_XP).click()

        DropDown = Conversion_XP
        Option = geoidOptions[value]

    else:

        DropDown = VerticalDatum_XP
        Option = value

    ConversionModel_Selector = Select(browser.find_element_by_xpath(DropDown))
    ConversionModel_Selector.select_by_value(Option)

    abs_filename = os.getcwd() + "\\" + filename

    browser.find_element_by_xpath(ChooseFile_XP).send_keys(abs_filename)

    browser.find_element_by_xpath(SendFile_XP).click()

    time.sleep(5)  # wait 5 seconds for the download to complete

    browser.quit()


def getFilename():
    while True:
        print(
            """Ensure that the selected csv file is located in the same directory as this script and 
please enter the filename for your .csv file (example: MyCoordinates.csv).\n"""
        )
        filename = str(input("Input: "))
        if not os.path.isfile(filename):
            print(
                'This path or file does not exist. Please try again or enter "quit" to terminate the system.'
            )
        elif filename == "quit":
            sys.exit()
        else:
            break

    return filename


if __name__ == "__main__":
    menu()
