from mutagen.id3 import ID3, error, APIC
from mutagen.mp3 import MP3


def set_album_artwork(title, song_title):
    audio = MP3(title + song_title + ".mp3", ID3=ID3)
    # add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except error:
        pass
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime='image/jpg',  # image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc=u'Cover',
            data=open(title + "/artwork.jpg", "rb").read()
        )
    )
    audio.save()