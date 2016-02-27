import youtube_dl

def DownloadAlbum(url,title):
    options ={
    'format': 'bestaudio/best',
    'outtmpl' : title + ".%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
