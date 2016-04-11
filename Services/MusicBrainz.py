import urllib
import urllib.request as urlopen
import json
import time
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def __GetDataFromServer(url,retry=5,wait=3):
    for attempt in range(retry):
        try:
            data = urlopen.urlopen(url).read().decode("utf-8")
            break
        except urllib.error.HTTPError:
            logging.debug("Failed to contact server: retrying attempt " + str(attempt))
            time.sleep(wait)
    return data

def GetBestTrackList(title,videoLength):
    albumIDs = FindAlbumIDs(title)
    difference = {'id': 0, 'difference': 1000000000}
    for albumID in albumIDs:
        print(albumID)
        print("Finding Tracks")
        albumTracks = GetTracks(albumID)
        albumLength = GetAlbumLength(albumTracks)

        print("Current ID: ", albumID)
        print("Difference: ", abs(albumLength - videoLength))
        if abs(albumLength - videoLength) < difference["difference"]:
            difference["id"] = albumID
            difference["difference"] = abs(albumLength - videoLength)

    if difference["difference"] < 5000:
        print("Difference is greater than 5 seconds warning")
        exit()
    return difference


def GetAlbumArtwork(id, path):
    base_url = "https://coverartarchive.org/release/"
    data = __GetDataFromServer(base_url + id)
    jsonData = json.loads(data)
    image = urlopen.urlopen(jsonData["images"][0]["image"]).read()
    open(path + "artwork.jpg", 'wb').write(image)


def GetTracks(id):
    base_url = "https://musicbrainz.org/ws/2/release/"
    url_suffix = "?inc=recordings+artists"
    url = base_url + id + url_suffix
    logger.info(url)
    xml_data = __GetDataFromServer(url)
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
    albumLength = 0
    for track in tracks:
        try:
            trackLength = track["length"]
        except KeyError:
            return 0
        albumLength += trackLength
    return albumLength / 1000


def FindAlbumIDs(title):
    base_url = "https://musicbrainz.org/ws/2/release/?query="
    title = title.replace(" ","+")
    url = base_url + title
    logger.info(url)
    xml_data = __GetDataFromServer(url)
    parsed_xml = BeautifulSoup(xml_data, 'html.parser')
    releaseList = parsed_xml.findAll("release")
    ids = []
    for release in releaseList:
        if int(release["ext:score"]) > 85:
            ids.append(str(release["id"]))
    return ids
