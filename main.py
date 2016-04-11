import os
import sys
from Services import Youtube, MusicBrainz
from MP3 import CutMP3

if len(sys.argv) != 1:
    url = sys.argv[1]
else:
    url = input("Please enter the URL of the album:")

videoTitle = Youtube.DownloadTitle(url)
videoDescription = Youtube.DownloadDescription(url)
videoLength = Youtube.DownloadLength(url)
print(videoTitle)

musicPath = "Music/" + videoTitle + "/"

if not os.path.exists(musicPath):
    os.mkdir(musicPath)
difference = MusicBrainz.GetBestTrackList(videoTitle, videoLength)

trackList = MusicBrainz.GetTracks(difference["id"])
MusicBrainz.GetAlbumArtwork(difference["id"], musicPath)

if not os.path.exists(musicPath + videoTitle + ".mp3"):
    Youtube.DownloadAlbum(url, musicPath + videoTitle)

print("Importing the mp3 file...")

CutMP3.CutMP3(musicPath,videoTitle,trackList)


print(difference["id"])
print(difference["difference"])
