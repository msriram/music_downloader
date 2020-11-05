from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
# audio = MP3File("C:\\Users\Sriram\Documents\dev\music_downloader\TamilTunes\Dagaalty(2020)\AaliyahAaliyah.mp3")

# print(audio.song[0].song)
# # print (audio.song[0].strip('- TamilTunes.com'))
# # del audio.year, audio.comment, audio.publisher, audio.url, audio.copyright, audio.band
# # print("artist: ", audio.artist)
# # print("album: ", audio.album)
# # print("song: ", audio.song)
# # print("track: ", audio.track)
# # print("comment: ", audio.comment)
# # print("year: ", audio.year)
# # print("genre: ", audio.genre)
# # print("band: ", audio.band)
# # print("composer: ", audio.composer)
# # print("copyright: ", audio.copyright)
# # print("url: ", audio.url)
# # print("publisher: ", audio.publisher)
# audio.set_version(VERSION_BOTH)
# audio.save()

from googlesearch import search
import requests
import re
import eyed3
import re
import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
debug = False
eyed3.log.setLevel("ERROR")

def fixArtistNames(artist):
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'&', ', ', artist)
    artist = re.sub(r'-', ' ', artist)
    artist = re.sub(r'  ', ' ', artist)

    # Specific artist names
    artist = re.sub(r'ar ', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kk ', 'K K ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kj ', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r',', ';',artist, flags=re.IGNORECASE)
    artist = artist.title().lstrip().rstrip()
    return artist

def set_id3(filename):
    """Module to read MP3 Meta Tags.

    Accepts Path like object only.
    """
    audio = eyed3.load(filename)
    # =========================================================================
    # Set Variables
    # =========================================================================
    if 1:
        audio.tag.read_only = False
        # Updating Title
        title = audio.tag.title
        title_ = audio.tag.title
        title_ = re.sub(r'-Masstamilan.In', '',title_, flags=re.IGNORECASE).lstrip()
        title_ = re.sub(r'- Masstamilan.In', '',title_, flags=re.IGNORECASE).lstrip()
        if debug:
            print(title, "---->", title_)
        if title_:
            audio.tag.title = title_

        # Updating Album-Artist
        album_artist = audio.tag.album_artist if audio.tag.album_artist else ""
        if not audio.tag.album_artist:
            if audio.tag.composer:
                audio.tag.album_artist = audio.tag.composer
                audio.tag.composer = None
            elif audio.tag.artist:
                audio.tag.album_artist = audio.tag.artist.split(",")[0]
        if audio.tag.album_artist:
            audio.tag.album_artist = re.sub(r'-Masstamilan.In', '',audio.tag.album_artist, flags=re.IGNORECASE).lstrip()
            audio.tag.album_artist = re.sub(r'- Masstamilan.In', '',audio.tag.album_artist, flags=re.IGNORECASE).lstrip()
            audio.tag.album_artist = fixArtistNames(audio.tag.album_artist)

            if debug:
                print(album_artist,  "---->", audio.tag.album_artist)
        
        # Updating Arist
        artist = audio.tag.artist
        if not audio.tag.artist or audio.tag.artist == audio.tag.composer:
            if audio.tag.album_artist != audio.tag.artist:
                audio.tag.artist = audio.tag.album_artist

        if audio.tag.artist:
            audio.tag.artist = re.sub(r'-Masstamilan.In', '',audio.tag.artist, flags=re.IGNORECASE).lstrip()
            audio.tag.artist = re.sub(r'- Masstamilan.In', '',audio.tag.artist, flags=re.IGNORECASE).lstrip()
            audio.tag.artist = fixArtistNames(audio.tag.artist)

        # title_split = audio.tag.title.split("-")
        # # print (title_split)
        # # input("pree to contin")

        # if len(title_split) == 2:
        #     audio.tag.title = title_split[0]
        #     audio.tag.artist = title_split[1]
        

        if debug:
            print(artist, "---->", audio.tag.artist)

        # Updating Comments
        if audio.tag.comments:
            comments = audio.tag.comments[0].text
            audio.tag.comments.set(u"")
            if debug:
                if not audio.tag.comments[0].text == "":
                    print(comments, "---->", audio.tag.comments[0].text)

        # Updating Year
        if audio.tag.recording_date:
            year = audio.tag.recording_date
        else:
            if audio.tag.release_date:
                audio.tag.recording_date = audio.tag.release_date
            else:
                year = re.search(r'\b[12]{1}[0-9]{3}\b', audio.tag.album)
                if year:
                    audio.tag.release_date = year.group()
                    audio.tag.recording_date = audio.tag.release_date
            if debug:
                year_= ""
                if audio.tag.recording_date:
                    year_ = audio.tag.recording_date
                if not year_ == "":
                    print(year, "---->", year_)

        # Updating Album
        album = audio.tag.album
        audio.tag.album = re.sub(r' \(\b[12]{1}[0-9]{3}\b\)', '', audio.tag.album)
        audio.tag.album = re.sub(r'-Masstamilan.In', '',audio.tag.album, flags=re.IGNORECASE).lstrip()
        audio.tag.album = re.sub(r'- Masstamilan.In', '',audio.tag.album, flags=re.IGNORECASE).lstrip()

        if debug:
            print(album, "---->", audio.tag.album)

        audio.tag.genre = 'Tamil'
        # if debug:
        #     input("Press Enter to confirm...")
        try:
            audio.tag.save(version=(2, 3, 0))
        except:
            print ("failed to save tag for ", filename)
            pass
        audio.tag.save(version=(1, 0, 0))

        #TODO: USE GOOGLE SEARCH TO UPDATE METADATA
        # metadata = audio.tag.title + " " + audio.tag.artist.split(",")[0]
        # print ("Searching Google for metadata", metadata)
        # try:
        #     for url in search(metadata, stop=1):
        #         r = requests.get(url)
        #         title = re.search('<title>(.*)</title>', r.text)
        #         print(title.group(1))
        # except:
        #     print ("Failed to search google ")
        #     pass
        if debug:
            mp3 = MP3File(filename)
            print("artist: ", mp3.artist)
            print("album: ", mp3.album)
            print("song: ", mp3.song)
            print("track: ", mp3.track)
            print("comment: ", mp3.comment)
            print("year: ", mp3.year)
            print("genre: ", mp3.genre)
            print("band: ", mp3.band)
            print("composer: ", mp3.composer)
            mp3.copyright=""
            mp3.url=""
            mp3.publisher=""
            print("copyright: ", mp3.copyright)
            print("url: ", mp3.url)
            print("publisher: ", mp3.publisher)
            mp3.set_version(VERSION_2)
            mp3.save()
        # renamed_file = os.path.join(os.path.dirname(filename), audio.tag.title) + ".mp3"
        # print("renaming file: ", filename, " to ",renamed_file)
        # os.rename(filename, renamed_file)
    # except:
        # print ("Failed to edit metadata for file: ",filename)


def list_files(startpath):
    for root, dirs, files in os.walk(startpath): #os.getcwd()):
        for file in files:
            filePath = os.path.join(os.path.abspath(root), file)
            if (os.path.exists(filePath)):
                if debug:
                    print (filePath)
                set_id3(os.path.abspath(filePath))

list_files('123Music')
# list_files('Bigil(2019)')
# set_id3("C:\\Users\Sriram\Documents\dev\music_downloader\TamilTunes\Dagaalty(2020)\AaliyahAaliyah.mp3")
