import urllib
import time
from collections import defaultdict
import logging

logging.basicConfig(filename='progress.log',level=logging.ERROR)

def extractlink(driver, year, baselink, paretialtext, limit=None):
    driver.get(baselink)
    allLinks = driver.find_elements_by_partial_link_text(paretialtext)
    movieLinkList = []
    mp3dict = []
    ind_dict = defaultdict(set)
    yearDict = {}
    for link in allLinks:
        movieLinkList.append(link.get_attribute("href"))
    if limit:
        movieLinkList = movieLinkList[0:limit]

    for link in movieLinkList:
        driver.get(link)
        links = driver.find_elements_by_partial_link_text("320")
        found = False
        if links:
            for l in links:
                href = l.get_attribute("href")
                if href.endswith(".zip"):
                    movie = getMoviename(href, year)
                    mp3dict.append({'Movie' : movie, 'Link' : href, 'Year' : year})
                    logging.error(movie + " Downloaded")
                    found = True
        else:
            links = driver.find_elements_by_partial_link_text("ownload")
            for l in links:
                href = l.get_attribute("href")
                if href.endswith(".zip"):
                    movie = getMoviename(href, year)
                    mp3dict.append({'Movie': movie, 'Link': href, 'Year': year})
                    logging.error(movie + " Downloaded")
                    found = True
        if not found:
            links = driver.find_elements_by_partial_link_text("Download")
            for link in links:
                href = link.get_attribute("href")
                if href.endswith(".mp3"):
                    movie, song = getMovienameAndSong(href, year)
                    ind_dict[movie].add(href)
                    yearDict[movie] = year
            logging.error(movie + " Individual Downloaded")
            found = True
        time.sleep(1)
    return mp3dict, ind_dict, yearDict

def getMoviename(href, year):
    t = href.split('/')[-2].replace('.zip', '').replace('128kbps', '').replace('320kbps', '').replace('128Kbps',
                                                                                                      '').replace(
        '320Kbps', '').replace('160Kbps', '').replace('160kbps', '').replace('_', ' ').replace('-', ' ').split('(')[
        0].split(year)[0]
    movie = urllib.unquote(t).decode().strip().title()
    return movie

def getMovienameAndSong(href, year):
    t = href.split('/')[-2].replace('.zip', '').replace('128kbps', '').replace('320kbps', '').replace('128Kbps',
                                                                                                      '').replace(
        '320Kbps', '').replace('160Kbps', '').replace('160kbps', '').replace('_', ' ').replace('-', ' ').split('(')[
        0].split(year)[0]
    movie = urllib.unquote(t).decode().strip().title()
    t = href.split('/')[-1].replace('.zip', '').replace('128kbps', '').replace('320kbps', '').replace('128Kbps',
                                                                                                      '').replace(
        '320Kbps', '').replace('160Kbps', '').replace('160kbps', '').replace('_', ' ').replace('-', ' ').split('(')[
        0].split(year)[0]
    song = urllib.unquote(t).decode().strip().title()
    return movie, song