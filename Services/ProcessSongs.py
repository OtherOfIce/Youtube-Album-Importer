import re
def GetSongList(desciption):
    songList= []
    for lineOfDescription in desciption.splitlines():
        lineList = lineOfDescription.split()
        song_time = 0
        song_name = ""
        if __lineContainsTimeCode(lineOfDescription):
            for part in lineList:
                if re.search("[0-9]:?[0-9][0-9]",part) != None:
                    #print(part)
                    time_codes = part.split(sep = ":")
                    time_codes = list(reversed(time_codes))
                    for time_code in range(len(time_codes)):
                        temp_time = int(time_codes[time_code]) * 1000
                        if time_code != 0:
                            temp_time *= (60 ** time_code)

                        #print(time_code, " = ", temp_time, " == ", time_codes[time_code])
                        #print("Times by:", (60 ** time_code))
                        song_time += temp_time
                    #print(song_time)
                    break

                if re.search("[a-z]",part) != None:
                    song_name += str(part) + " "
            songList.append((song_name,song_time))
    return songList

def __lineContainsTimeCode(line):
    if re.search("[0-9]:[0-9][0-9]",line) != None:
        return True
    if re.search("[0-9][0-9]:[0-9][0-9]",line) != None:
        return True
    return False
