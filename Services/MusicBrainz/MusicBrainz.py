import logging
import urllib
from bs4 import BeautifulSoup
from Utility.Utility import getDataFromServer


class musicBrainz(object):
    def __init__(self):
        pass
    def downloadTrackMetaData(self, title):
            base_url = "https://musicbrainz.org/ws/2/release/?query="
            url_suffix = "?inc=recordings+artists"
            title = urllib.parse.quote_plus(title)
            url = base_url + title + url_suffix
            logging.info(url)
            xml_data = getDataFromServer(url)
            parsed_xml = BeautifulSoup(xml_data, 'html.parser')
            track = []
            track["title"] = parsed_xml.recording.title.string
            track["length"] = int(parsed_xml.recording.length.string)
            #track["artist"] = parsed_xml.recording
             #   tracks[xml_track_count]["album"] = parsed_xml.metadata.release.title.string
             #   tracks[xml_track_count]["track number"] = xml_track.number.string
             #   xml_track_count += 1
            return track
    def downloadAlbumMetaData(self,title):
        pass



def GetBestTrackList(title,videoLength):
    albumIDs = FindAlbumIDs(title)
    difference = {'id': 0, 'difference': 1000000000}
    for albumID in albumIDs:
        logging.debug(albumID)
        albumTracks = GetTracks(albumID)
        albumLength = GetAlbumLength(albumTracks)
        if albumLength == 0:
            logging.debug("No length for album.")
            break;
        logging.debug("Current ID: ", albumID)
        logging.debug("Difference: ", abs(albumLength - videoLength))
        if abs(albumLength - videoLength) < difference["difference"]:
            difference["id"] = albumID
            difference["difference"] = abs(albumLength - videoLength)

    if difference["difference"] > 5000:
        print("Difference is greater than 5 seconds Music will be out of sync. Quitting")
        exit()
    return difference


def GetTracks(id):
    base_url = "https://musicbrainz.org/ws/2/release/"
    url_suffix = "?inc=recordings+artists"
    url = base_url + id + url_suffix
    logging.info(url)
    xml_data = getDataFromServer(url)
    parsed_xml = BeautifulSoup(xml_data, 'html.parser')
    xml_tracks = parsed_xml.findAll("track")
    tracks = [{} for x in range(50)]
    xml_track_count = 0
    for xml_track in xml_tracks:
            tracks[xml_track_count] = {}
            tracks[xml_track_count]["title"] = xml_track.recording.title.string
            tracks[xml_track_count]["length"] = int(xml_track.recording.length.string)
            tracks[xml_track_count]["artist"] = parsed_xml.find("artist").contents[0].string
            tracks[xml_track_count]["album"] = parsed_xml.metadata.release.title.string
            tracks[xml_track_count]["track number"] = xml_track.number.string
            xml_track_count += 1
    return tracks

def GetAlbumLength(tracks):
    album_length = 0
    for track in tracks:
        try:
            trackLength = track["length"]
        except KeyError:
            return 0
        album_length += trackLength
    return album_length / 1000


def FindAlbumIDs(title):
    base_url = "https://musicbrainz.org/ws/2/release/?query="
    title = urllib.parse.quote_plus(title)
    url = base_url + title
    logging.info(url)
    xml_data = getDataFromServer(url)
    parsed_xml = BeautifulSoup(xml_data, 'html.parser')
    release_list = parsed_xml.findAll("release")
    ids = list(filter(lambda x: int(x["ext:score"]) > 85, release_list))
    ids = list(map(lambda x:x["id"],ids))
    return ids
