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

def FindAlbumID(title):
    base_url = "https://musicbrainz.org/ws/2/release/?query="
    title = title.replace(" ","+")
    xml_data = __GetDataFromServer(base_url + title)
    parsed_xml = BeautifulSoup(xml_data, 'html.parser')
    id = parsed_xml.find("release")['id']
    logger.debug(id)
    return id


def GetAlbumArtwork(id, path):
    base_url = "https://coverartarchive.org/release/"
    data = __GetDataFromServer(base_url + id)
    jsonData = json.loads(data)
    image = urlopen.urlopen(jsonData["images"][0]["image"]).read()
    open(path + "artwork.jpg", 'wb').write(image)


def GetTracks(id):
    base_url = "https://musicbrainz.org/ws/2/release/"
    url_suffix = "?inc=recordings+artists"
    xml_data = __GetDataFromServer(base_url + id + url_suffix)
    parsed_xml = BeautifulSoup(xml_data, 'html.parser')
    xml_tracks = parsed_xml.findAll("track")
    logger.debug("Number of tracks: ", parsed_xml.find("track-list").count)
    tracks = [{} for x in range(int(parsed_xml.find("track-list")["count"]))]
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
