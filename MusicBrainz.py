import sys
import urllib
import urllib.request as urlopen
from bs4 import BeautifulSoup

retry_attempts = 10

def GetSongList(title):
    id = __FindAlbumID(title)
    tracks = __GetTracks(id)
    return tracks

def __FindAlbumID(title):
    base_url = "https://musicbrainz.org/ws/2/release/?query="
    title = title.replace(" ","+")

    xml_data = urlopen.urlopen(base_url + title).read().decode("utf-8")


    parsed_xml = BeautifulSoup(xml_data, 'lxml')
    id = parsed_xml.find("release")['id']
    return id

def __GetTracks(id):
    base_url = "https://musicbrainz.org/ws/2/release/"
    url_suffix = "?inc=recordings+artists"
    xml_data = urlopen.urlopen(base_url + id + url_suffix).read().decode("utf-8")
    parsed_xml = BeautifulSoup(xml_data, 'lxml')
    xml_tracks = parsed_xml.findAll("track")
    print(parsed_xml.find("track-list").count)
    tracks = [{} for x in range(int(parsed_xml.find("track-list")["count"]))]
    xml_track_count = 0
    for xml_track in xml_tracks:
        print(xml_track_count)
        tracks[xml_track_count] = {}
        tracks[xml_track_count]["title"] = xml_track.recording.title.string
        tracks[xml_track_count]["length"] = int(xml_track.recording.length.string)
        tracks[xml_track_count]["artist"] = parsed_xml.find("artist").contents[0].string
        tracks[xml_track_count]["album"] = parsed_xml.metadata.release.title.string
        tracks[xml_track_count]["track number"] = xml_track.number.string
        xml_track_count += 1;
    return tracks
#print(GetSongList("Foo Fighters - Echoes, Silence, Patience & Grace"))
#GetSongList("a0aa34aa-4fe2-4de4-a1c6-0587d5422b33?inc=recordings")
