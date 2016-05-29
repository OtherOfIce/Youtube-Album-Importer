import json
import logging
import urllib
import urllib.request as urlopen
from bs4 import BeautifulSoup
from Utility.Utility import getDataFromServer
from Services.MusicBrainz import MusicBrainz_Track


class MusicBrainzAlbum(object):
    def __init__(self):
        self.tracks = []
        self.mbID = 0

    def getAlbumLength(self):
        return sum(list(map( lambda x: x.length, self.tracks)))