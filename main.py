from pydub import AudioSegment
import ProcessSongs
import MusicBrainz
import Youtube
import os

url = input("Please enter the URL of the album:")

title = Youtube.DownloadTitle(url)
print("The title is:", title)
description = Youtube.DownloadDescription(url)
songList = MusicBrainz.GetSongList(title)
print(songList)
if not os.path.exists("./" + title + ".mp3"):
    print(title + ".mp3")
    Youtube.DownloadAlbum(url,title)

print("Importing the mp3 file...")
sound = AudioSegment.from_mp3(title + ".mp3")
if not os.path.exists("./" + title):
    os.mkdir(title)
print("Creating directory")

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
                       'track number' : songInfo["track number"]}
        )
    
