from pydub import AudioSegment
import ProcessSongs
import ProcessHTML
import DownloadAlbum
import os

url = input("Please enter the URL of the album:")
title, description = ProcessHTML.GetHTMLData(url)
songList = ProcessSongs.GetSongList(description)
print("The title is:", title)
#DownloadAlbum.DownloadAlbum(url,title)

print("Importing the mp3 file...")
sound = AudioSegment.from_mp3(title + ".mp3")
os.mkdir(title)
print("Creating directory")
for song_number in range(len(songList)):
    print("Extracting and writing: " + songList[song_number][0])
    # len() and slicing are in milliseconds
    if song_number == len(songList) - 1:
        song = sound[songList[song_number][1]:]
    else:
        song = sound[songList[song_number][1]:songList[song_number + 1][1]]

    # writing mp3 files is a one liner
    song.export(title + "/" + songList[song_number][0] + ".mp3", format="mp3")
