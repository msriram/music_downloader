################ DOWNLOAD TAMIL SONGS FROM TAMIL TAMILTUNES.PRO ###################
from __future__ import print_function, unicode_literals
import sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib
from html.parser import HTMLParser
import shutil
import os
import youtube_dl

debug = False
skip_download = False
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
import logging
logging.basicConfig(filename='missing_download.log',level=logging.DEBUG)
logging.error('Sample Error Log')
logging.warning('Sample Warning Log')
logging.debug('Sample Debug Log')
logging.info('Sample Info Log')

from googlesearch import search
import requests
import re
import eyed3
import re
import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
eyed3.log.setLevel("ERROR")

hexaPattern = r'%[0-9a-fA-F]{2}'
bitratePattern = r'[0-9]{3}kbps'
yearPattern = r'[12]{1}[0-9]{3}'
def fixName(tag):
    # Preliminary change, must modify for each website
    def fixWebsiteName(file):
        file = re.sub(r'Masstamilan\.in','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Masstamilan\.com','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'-Masstamilan\.in', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'- Masstamilan\.In', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'\[Masstamilan\.In\]', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'\[Starmusiq\.La\]', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Masstamilan\.In', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Masstamilan In', '', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'www\.', '', file, flags=re.IGNORECASE).lstrip()
        return file

    # Common stuff
    def fixPunctuation(file):
        file = re.sub(hexaPattern, '', file)
        file = re.sub(bitratePattern, '', file, flags=re.IGNORECASE)
        file = re.sub(yearPattern, '', file)
        file = re.sub('[','', file)
        file = re.sub(']','', file)
        file = re.sub('_','', file)
        file = re.sub(r'\.+', '.', file)
        file = re.sub(r'-\.', '.', file)
        file = re.sub(r'-', '', file)
        # file = re.sub(r'-+$', '', file)
        return file
    
    return fixPunctuation(fixWebsiteName(tag))

def fixArtistNames(artist):
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'&', ', ', artist)
    artist = re.sub(r'  ', ' ', artist)

    # Specific artist names
    artist = re.sub(r'ar ', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a.r.', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kj ', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'k.j.', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'spb ', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r's.p.b.', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'gv ', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'g.v.', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B Lasubrahmanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'-', ';', artist)
    artist = re.sub(r',', ';',artist)
    artist = re.sub(r',', ';',artist)
    artist = re.sub(r'/', ';',artist)
    artist = re.sub(r'\\', ';',artist)
    artist = artist.title().lstrip().rstrip()
    return artist


def set_id3(filename):
    """Module to read MP3 Meta Tags.

    Accepts Path like object only.
    """
    audio = eyed3.load(filename)
    if not audio:
        logging.error('failed to add tag for %s, invalid load', filename)
        return
    # =========================================================================
    # Set Variables
    # =========================================================================
    if 1:
        audio.tag.read_only = False
        # Cleanup Tags
        if audio.tag.title:
            fixName(audio.tag.title)
        if audio.tag.album:
            fixName(audio.tag.album)
        if audio.tag.album_artist:
            fixName(audio.tag.album_artist)
        if audio.tag.artist:
            fixName(audio.tag.artist)

        # Updating Album-Artist
        album_artist = audio.tag.album_artist if audio.tag.album_artist else ""
        if not audio.tag.album_artist:
            if audio.tag.composer:
                audio.tag.album_artist = audio.tag.composer
                audio.tag.composer = None
            elif audio.tag.artist:
                audio.tag.album_artist = audio.tag.artist.split(",")[0]
        if audio.tag.album_artist:
            audio.tag.album_artist = fixArtistNames(audio.tag.album_artist)

            if debug:
                print(album_artist,  "---->", audio.tag.album_artist)
        
        # Updating Arist
        artist = audio.tag.artist
        if not audio.tag.artist or audio.tag.artist == audio.tag.composer:
            if audio.tag.album_artist != audio.tag.artist:
                audio.tag.artist = audio.tag.album_artist

        if audio.tag.artist:
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

        # Split filename
        filename_split = os.path.dirname(filename).split('\\')
        if len(filename_split) == 1:
            filename_split = os.path.dirname(filename).split('/')
        # Updating Album and Year
        if not audio.tag.album:
            audio.tag.album = filename_split[-1]

        # Fixup Year
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
                else:
                    audio.tag.release_date = filename_split[-2]
                    audio.tag.recording_date = audio.tag.release_date

            if debug:
                year_= ""
                if audio.tag.recording_date:
                    year_ = audio.tag.recording_date
                if not year_ == "":
                    print(year, "---->", year_)
        # Fixup Album Name
        if audio.tag.album:
            album = audio.tag.album
            audio.tag.album = re.sub(r' \(\b[12]{1}[0-9]{3}\b\)', '', audio.tag.album)

            if debug:
                print(album, "---->", audio.tag.album)

        # Misc: Genre, Urls, Images etc
        audio.tag.genre = 'Tamil'
        for y in audio.tag.images:
            audio.tag.images.remove(y.description)

        # if debug:
        #     input("Press Enter to confirm...")
        # Save Tags
        try:
            audio.tag.save()
            audio.tag.save(version=(2, 3, 0))
        except:
            logging.error('failed to save tag for %s', filename)
            if debug:
                print ('failed to save tag for ', filename)
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
            print('-------------------------------')
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
            print('-------------------------------')
            
        # renamed_file = os.path.join(os.path.dirname(filename), audio.tag.title) + ".mp3"
        # print("renaming file: ", filename, " to ",renamed_file)
        # os.rename(filename, renamed_file)
    # except:
        # print ("Failed to edit metadata for file: ",filename)


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        self.links.append(attr)

def create_folder(folder):
    path = os.getcwd()
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
        except OSError:
            if debug == True:
                print ("Creation of the directory %s failed" % folder)
        else:
            if debug == True:
                print ("Successfully created the directory %s " % folder)
    # else:
        # if debug == True:
            # print ("Directory already present %s" % folder)

def getFromYoutube(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'download_archive': 'youtube.list',
        'quiet': False,
        'no_warnings': True,
        'postprocessors': [ {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def getFromMassTamilan(year, links):
    print("Downloading Movies from year: ", year)
    for link in links:
        headers={'User-Agent':user_agent,}
        request=urllib2.Request(link, None, headers)
        try:
            response = urllib2.urlopen(request)
            html = response.read()
            response.close()
        except urllib2.HTTPError as e:
            print(e, 'while fetching', url)
            return
        
        parser = MyHTMLParser()
        parser.links = []
        parser.feed(str(html))

        for l in parser.links:
            if 'mp3' in l['href']:
                music_url = l['href'] #.replace('\\\'','%27').replace(' ','%20').replace('(','%28').replace(')','.set(u"")
                music_file = fixName(music_url.split("/")[-1])
                music_folder = "123Music/" + year + "/" + fixName(music_url.split("/")[-2])
                create_folder("123Music/" + year)
                create_folder(music_folder)

                if debug:
                    logging.info('Downloading music_url %s', music_url)
                    logging.info('as a file %s', music_file)
                    logging.info('in the location %s', music_folder)
                    logging.info('\n')

                music_path = music_folder + '/' + music_file
                # if debug == True:
                    # print(music_url, " -----> ", music_path)
                if os.path.exists(music_path):
                    if debug:
                        logging.info('already downloaded %s in %s', music_file, music_folder)
                elif not skip_download:
                    try:
                        music_request=urllib2.Request(music_url, None, headers)
                        with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
                            shutil.copyfileobj(response, out_file)
                        if 1:
                            logging.info('successfully downloaded file %s to %s', os.path.basename(out_file.name), music_folder)
                    except:
                        logging.error('Failed to download url %s', music_url)
                        pass
                if os.path.exists(music_path):
                    set_id3(music_path)

import multiprocessing
from queue import Queue
from threading import Thread

class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            dictionary = self.queue.get()
            try:
                for d in dictionary:
                    getFromMassTamilan(d, dictionary[d])
            finally:
                self.queue.task_done()


def urlParse(link, key, value, regex=''):
    headers={'User-Agent':user_agent,}
    request=urllib2.Request(link, None, headers)
    try:
        response = urllib2.urlopen(request)
        html = response.read()
        response.close()
    except urllib2.HTTPError as e:
        print(e, 'while fetching', url)
        return
    parser = MyHTMLParser()
    parser.links = []
    parser.feed(str(html))
    download_links = []
    for l in parser.links:
            # print (l)
            if value in l[key]: # change to https
                download_link = (re.sub(r'\\\'', '', l[key]))
                if download_link not in download_links and re.search(regex, download_link):
                    download_links.append(download_link)
    return download_links
# Mind the "if" instruction!
def downloadTamilSongs():
    queue = Queue()
    for i in range(16): #multiprocessing.cpu_count()):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    
    download_years = urlParse("https://masstamilan.in/browse-tamil-all-songs/", 'href', 'https', r'\b[12]{1}[0-9]{3}\b')
    download_years = [
        # "https://masstamilan.in/1979-tamil-songs-download/", 
        # "https://masstamilan.in/2018-tamil-songs-download/", 
        # "https://masstamilan.in/2017-tamil-songs-download/", 
        # "https://masstamilan.in/2016-tamil-songs-download/", 
        # "https://masstamilan.in/2015-tamil-songs-download/", 
        # "https://masstamilan.in/2014-tamil-songs-download/", 
        "https://masstamilan.in/1933-tamil-songs-download/"]
    for download_year in download_years:
        year = re.search(r'\b[12]{1}[0-9]{3}\b', download_year).group()
        download_links = urlParse(download_year, 'href', 'https')
        
        dictionary = {}
        for d in download_links:
            if year not in dictionary.keys():
                dictionary[year] = []
            dictionary[year].append(d)
            
        queue.put(dictionary)
        # for key, value in download:
            # print (key, value)
    queue.join() # starting workers

downloadTamilSongs()

# import cProfile

# cProfile.run('downloadTamilSongs()')