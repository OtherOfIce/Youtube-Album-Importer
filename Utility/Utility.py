import logging
import time
import urllib
from urllib import request as urlopen


def getDataFromServer(url, retry=5, wait=3):
    for attempt in range(retry):
        try:
            data = urlopen.urlopen(url).read().decode("utf-8")
            break
        except urllib.error.HTTPError:
            logging.debug("Failed to contact server: retrying attempt " + str(attempt))
            time.sleep(wait)
    return data