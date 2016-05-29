import json
from urllib import request as urlopen

from Utility.Utility import getDataFromServer


def GetAlbumArtwork(id, path):
    base_url = "https://coverartarchive.org/release/"
    data = getDataFromServer(base_url + id)
    jsonData = json.loads(data)
    try:
        image = urlopen.urlopen(jsonData["images"][0]["image"]).read()
    except:
        print("Failed to get artwork. Sorry")
    open(path + "artwork.jpg", 'wb').write(image)