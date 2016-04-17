import youtube_dl


class YoutubeLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Youtube(object):
    def __init__(self, url):
        self.url = url
        self.noLogOptions = {'logger':YoutubeLogger()}
        self.video_info = youtube_dl.YoutubeDL(self.noLogOptions).extract_info(url, download=False)

    def get_title(self):
            return self.video_info.get('title', None)

    def get_description(self):
            return self.video_info.get('description', None)

    def get_length(self):
            return self.video_info.get('duration',None)

    def download_video(self, path):
        options ={
        'format': 'bestaudio/best',
        'outtmpl' : path + ".%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([self.url])

