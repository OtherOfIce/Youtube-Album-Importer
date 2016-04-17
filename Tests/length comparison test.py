import Services.Youtube as Youtube
import Services.MusicBrainz as MusicBrainz

url = "https://www.youtube.com/watch?v=C-PlblnyPgM"


videoTitle = Youtube.DownloadTitle(url)
videoLength = Youtube.DownloadLength(url)

print(videoTitle)

print("Finding IDS")
albumIDs = MusicBrainz.FindAlbumIDs(videoTitle)
print(albumIDs)
difference = {'id' : 0, 'difference':1000000000}
for albumID in albumIDs:
    print(albumID)
    print("Finding Tracks")
    albumTracks = MusicBrainz.GetTracks(albumID)
    albumLength = MusicBrainz.GetAlbumLength(albumTracks)

    if abs(albumLength-videoLength) < difference["difference"]:
        difference["id"] = albumID
        difference["difference"] = abs(albumLength-videoLength)

print(difference)
    #if videoLength == albumLength:
     #   print("SAME SIZE!!!!")
     #   print("video length ", videoLength," == Album length ", albumLength)
   # else:
      #  print("albumLength: ", albumLength)
     #  print("videoLength: ", videoLength)
