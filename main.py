import os
import sys
from pydub import AudioSegment
import MusicBrainz
import Youtube
from Tagging import SetAlbumArtwork


if len(sys.argv) != 1:
    url = sys.argv[1]
else:
    url = input("Please enter the URL of the album:")

title = Youtube.DownloadTitle(url)
print(title)

if not os.path.exists("./" + title):
    os.mkdir(title)

description = Youtube.DownloadDescription(url)
songList = MusicBrainz.GetSongList(title)

if not os.path.exists("./" + title + ".mp3"):
    Youtube.DownloadAlbum(url,title)

print("Importing the mp3 file...")
sound = AudioSegment.from_mp3(title + ".mp3")


processedLength = 0

for song_number in range(len(songList)):
    songInfo = songList[song_number]
    songTitle = songInfo["title"].replace("/"," ")
    songLength = songInfo["length"]

    print("Extracting and writing: " + songTitle)

    song = sound[processedLength: processedLength + songLength]
    processedLength += songLength

    song.export(title + "/" + songTitle + ".mp3", format="mp3", tags={
                    'title' : songInfo["title"],
                    'artist': songInfo["artist"],
                      'album': songInfo["artist"],
                       'track' : songInfo["track number"]}
        )
    SetAlbumArtwork(title, songTitle)
