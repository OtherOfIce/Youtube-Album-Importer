import os
import sys
from Services import Youtube, MusicBrainz
from MP3 import CutMP3

if len(sys.argv) != 1:
    url = sys.argv[1]
else:
    url = input("Please enter the URL of the album:")

videoTitle = Youtube.DownloadTitle(url)
description = Youtube.DownloadDescription(url)
print(videoTitle)
musicPath = "Music/" + videoTitle + "/"

if not os.path.exists(musicPath):
    os.mkdir(musicPath)


albumID = MusicBrainz.FindAlbumID(videoTitle)
trackList = MusicBrainz.GetTracks(albumID)
MusicBrainz.GetAlbumArtwork(albumID, musicPath)

if not os.path.exists(musicPath + videoTitle + ".mp3"):
    Youtube.DownloadAlbum(url, musicPath + videoTitle)

print("Importing the mp3 file...")

CutMP3.CutMP3(musicPath,videoTitle,trackList)

