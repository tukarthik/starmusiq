from selenium import webdriver
import extract_link
import csv
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#https://www.idiotinside.com/2015/04/14/export-dict-to-csv-list-to-csv-in-python/

csv_columns1 = ['Movie','Year','Link']

def initDriver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2, "profile.managed_default_content_settings.stylesheet":2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('--headless')
    driver = webdriver.Remote(
       command_executor='http://127.0.0.1:4444/wd/hub',
       #desired_capabilities=DesiredCapabilities.CHROME,)
       desired_capabilities = options.to_capabilities())
    return driver

def closeDriver(driver):
    driver.close()

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

d = {
     '2017' : ["http://starmusiq.me/2017-tamil-mp3-songs-download/", "Download"],
     '2016' : ["http://starmusiq.me/2016-all-tamil-mp3-songs-download", "Download"],
     '2015' : ["http://starmusiq.me/2015-all-tamil-mp3-songs-download", " 2015 Tami"],
     '2014' : ["http://starmusiq.me/2014-all-tamil-mp3-songs-download", " 2014 Tami"]
     }

if __name__ == "__main__":
    driver = initDriver()

    songDict = {}
    songlist = []
    dict_data = []
    for k,v in d.iteritems():
        d, t, y = extract_link.extractlink(driver, k, v[0],v[1])
        dict_data.extend(d)
        songDict.update(t)
    #for i in dict_data:
        #print i['Movie'], i['Year'], i['Link']

    for k,v in songDict.iteritems():
        for x in v:
            print k,x
            songlist.append({"Movie" : k, "Year" : y.get(k, ''), "Link" : x})

    closeDriver(driver)

    currentPath = os.getcwd()
    csv_file = currentPath + "/Names.csv"
    WriteDictToCSV(csv_file, csv_columns1, dict_data)

    currentPath = os.getcwd()
    csv_file = currentPath + "/Songs.csv"
    WriteDictToCSV(csv_file, csv_columns1, songlist)



