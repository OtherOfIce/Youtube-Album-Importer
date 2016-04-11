import youtube_dl

class youtubeLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)


noLogOptions = {'logger':youtubeLogger()}

def DownloadTitle(url):
    with youtube_dl.YoutubeDL(noLogOptions) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', None)

def DownloadDescription(url):
    with youtube_dl.YoutubeDL(noLogOptions) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('description', None)

def DownloadLength(url):
    with youtube_dl.YoutubeDL(noLogOptions) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('duration',None)

def DownloadAlbum(url,path):
    options ={
    'format': 'bestaudio/best',
    'outtmpl' : path + ".%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

