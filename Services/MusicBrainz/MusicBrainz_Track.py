import json
import logging
import urllib
import urllib.request as urlopen
from bs4 import BeautifulSoup
from Utility.Utility import getDataFromServer



class MusicBrainzTrack(object):
    def __init__(self):
        self.__title = 0
        self.__length = 0
        self.__artist = 0
        self.__album = 0
        self.__track_number = 0
