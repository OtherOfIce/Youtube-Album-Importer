import os, sys
import logging
from Services import Youtube, ProcessSongs
from Services.MusicBrainz import MusicBrainz_Album, MusicBrainz_Track, MusicBrainz
from MP3 import CutMP3


#logging.basicConfig(level=logging.INFO)

if len(sys.argv) != 1:
    url = sys.argv[1]
else:
    url = input("Please enter the URL of the album:")

try:
    youtube = Youtube.Youtube(url)
    videoTitle = youtube.get_title()
    videoDescription = youtube.get_description()
    videoLength = youtube.get_length()
except Youtube.youtube_dl.utils.DownloadError:
    print("Given URL is invalid")
    sys.exit()


    musicBrainz = musicBrainz()
    album = MusicBrainz_Album()



if ProcessSongs.VideoHasTimeCodes(videoDescription):
    temp_list = ProcessSongs.GetSongList(videoDescription)
    trackList = list(map(MusicBrainz_Track(),temp_list))

    trackMetadata = list(map(lambda x: musicBrainz.downloadTrackMetaData(x[0]),temp_list))
    map(lambda x: album.AddTrack())
