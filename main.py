from pydub import AudioSegment
import urllib.request
from bs4 import BeautifulSoup
import re
import html2text
import os

def GetSongList(desciption):
    songList= []
    for line in desciption.splitlines():
        lineList = line.split()
        song_time = 0
        song_name = ""
        if re.search("[0-9][0-9]:[0-9][0-9]",line) != None:
            for part in lineList:
                if re.search("[0-9][0-9]:?[0-9][0-9]",part) != None:
                    print(part)
                    song_time = 0
                    time_codes = part.split(sep = ":")
                    time_codes = list(reversed(time_codes))
                    for time_code in range(len(time_codes)):
                        temp_time = int(time_codes[time_code]) * 1000
                        if time_code != 0:
                            temp_time *= (60 ** time_code)

                        print(time_code, " = ", temp_time, " == ", time_codes[time_code])
                        print("Times by:", (60 ** time_code))
                        song_time += temp_time
                    print(song_time)

                if re.search("[a-z]",part) != None:
                    song_name += str(part) + " "
            songList.append((song_name,song_time))
    return songList

#musicUrl = input("Please enter the URL of the album:")
url = 'https://www.youtube.com/watch?v=pkHAPZLx6ok'
html_data = urllib.request.urlopen(url).read().decode("utf-8")

parsed_html = BeautifulSoup(html_data, 'html.parser')
title = parsed_html.head.title.text[:-10]
description = html2text.html2text(parsed_html.body.find('p', attrs={'id':'eow-description'}).prettify())


print("The title is:", title)
songList = GetSongList(description)

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
