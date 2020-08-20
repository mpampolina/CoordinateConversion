from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from SingularConversionElevation import geoidOptions
from utils import (
    get_path, 
    choiceValidation, 
    get_vertical_Datum,

)
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

# Main menu method
def menu():

    print("Welcome to the CGVD28 to CGVD2013 Conversion Tool".center(59, "="))

    print(
        '''\nAre you converting: 
    1. From elevation (CGVD28) to  elevation (CGVD2013)           -> Enter "1"
    2. From elevation (CGVD2013) to elevation (CGVD28)            -> Enter "2"
    3. From an Ellipsoidal Elevation to an Orthometric Elevation  -> Enter "3"
    4. From an Orthometric Elevation to an Ellipsoidal Elevation  -> Enter "4"'''
    )
    conv_direction = choiceValidation(["1", "2", "3", "4"], "\nConversion Direction: ")

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

        value, _ = get_vertical_Datum(verb)

    path = get_path()

    batchProcessing(convert, value, path)


# Method for Batch processing via the GPSH web app
def batchProcessing(convert, value, path):

    # options to ignore SSL error code 1
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    browser = webdriver.Chrome(options=options)
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

    if os.getcwd() not in path:
        abs_filename = os.getcwd() + "\\" + path
    else:
        abs_filename = path

    browser.find_element_by_xpath(ChooseFile_XP).send_keys(abs_filename)

    browser.find_element_by_xpath(SendFile_XP).click()

    time.sleep(5)  # wait 5 seconds for the download to complete

    browser.quit()


if __name__ == "__main__":
    menu()
