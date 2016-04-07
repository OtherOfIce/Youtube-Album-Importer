from pydub import AudioSegment
from Tagging import SetAlbumArtwork
def CutMP3(path,videoTitle,trackList):
    sound = AudioSegment.from_mp3(path+"/" + videoTitle + ".mp3")
    processedLength = 0

    for song_number in range(len(trackList)):
        songInfo = trackList[song_number]
        songTitle = songInfo["title"].replace("/", " ")
        songLength = songInfo["length"]

        print("Extracting and writing: " + songTitle)
        song = sound[processedLength: processedLength + songLength]
        processedLength += songLength

        song.export(path + "/" + songTitle + ".mp3", format="mp3", tags={
                        'title' : songInfo["title"],
                        'artist': songInfo["artist"],
                          'album': songInfo["artist"],
                           'track' : songInfo["track number"]}
                    )
        SetAlbumArtwork(path, songTitle)