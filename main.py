from pydub import AudioSegment
import ProcessSongs
import MusicBrainz
import Youtube
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

url = input("Please enter the URL of the album:")

title = Youtube.DownloadTitle(url)
print("The title is:", title)

if not os.path.exists("./" + title):
    os.mkdir(title)
print("Creating directory")

description = Youtube.DownloadDescription(url)
songList = MusicBrainz.GetSongList(title)
print(songList)
if not os.path.exists("./" + title + ".mp3"):
    print(title + ".mp3")
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
    audio = MP3(title + "/" + songTitle + ".mp3", ID3=ID3)
    # add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except error:
        pass

    audio.tags.add(
        APIC(
            encoding=3, # 3 is for utf-8
            mime='image/jpg', # image/jpeg or image/png
            type=3, # 3 is for the cover image
            desc=u'Cover',
            data= open(title + "/artwork.jpg", "rb").read()
        )
    )
    audio.save()
