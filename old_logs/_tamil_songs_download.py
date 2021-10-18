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

debug = True
ddebug = True
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'


from googlesearch import search
import requests
import re
import eyed3
import re
import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
eyed3.log.setLevel("ERROR")

def fixArtistNames(artist):
    # Specific artist names
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'&', ', ', artist)
    artist = re.sub(r'-', ' ', artist)
    artist = re.sub(r'  ', ' ', artist)

    # Specific artist names
    artist = re.sub(r'ar ', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kk ', 'K K ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kj ', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Spb ', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r',', ';',artist, flags=re.IGNORECASE)
    artist = re.sub(r'/', ';',artist, flags=re.IGNORECASE)
    artist = re.sub(r'\\', ';',artist, flags=re.IGNORECASE)
    artist = artist.title().lstrip().rstrip()
    artist = artist.title()
    return artist

def set_id3(filename):
    """Module to read MP3 Meta Tags.

    Accepts Path like object only.
    """
    audio = eyed3.load(filename)
    # =========================================================================
    # Set Variables
    # =========================================================================
    try:
        audio.tag.read_only = False
        # Updating Title
        title = audio.tag.title
        title_ = re.sub(r' - TamilTunes.com', '',audio.tag.title)
        if ddebug:
            print(title, "---->", title_)
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
            audio.tag.album_artist = fixArtistNames(audio.tag.album_artist)
            if ddebug:
                print(album_artist,  "---->", audio.tag.album_artist)
        
        # Updating Arist
        artist = audio.tag.artist
        if not audio.tag.artist or audio.tag.artist == audio.tag.composer:
            if audio.tag.album_artist != audio.tag.artist:
                audio.tag.artist = audio.tag.album_artist
        if audio.tag.artist:
            audio.tag.artist = fixArtistNames(audio.tag.artist)
        
        if ddebug:
            print(artist, "---->", audio.tag.artist)

        # Updating Comments
        if audio.tag.comments:
            comments = audio.tag.comments[0].text
            audio.tag.comments.set(u"")
            if ddebug:
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
            if ddebug:
                year_= ""
                if audio.tag.recording_date:
                    year_ = audio.tag.recording_date
                if not year_ == "":
                    print(year, "---->", year_)

        # Updating Album
        album = audio.tag.album
        audio.tag.album = re.sub(r' \(\b[12]{1}[0-9]{3}\b\)', '', audio.tag.album)

        if ddebug:
            print(album, "---->", audio.tag.album)

        audio.tag.genre = 'Tamil'
        # if debug:
        #     input("Press Enter to confirm...")
        audio.tag.save(version=(2, 3, 0))
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
        if ddebug:
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
            print("copyright: ", mp3.copyright)
            print("url: ", mp3.url)
            print("publisher: ", mp3.publisher)
            mp3.set_version(VERSION_2)
            mp3.save()
        # renamed_file = os.path.join(os.path.dirname(filename), audio.tag.title) + ".mp3"
        # print("renaming file: ", filename, " to ",renamed_file)
        # os.rename(filename, renamed_file)
    except:
        print ("Failed to edit metadata for file: ",filename)
        pass


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
                print ("Creation of the directory %s failed" % path)
        else:
            if debug == True:
                print ("Successfully created the directory %s " % path)
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

def getFromTamilTunesPro(link):
    # print("Downloading from ", link)
    # return
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
        if 'title' in list(l):
            if 'mp3' in l['title']:
                music_url = l['href'].replace('\\\'','%27').replace(' ','%20').replace('(','%28').replace(')','%29')
                music_file = music_url.split("/")[-1].replace('%28','(').replace('%29',')').replace('%27','\'').replace('%20', '').replace('%E2%80%93Single','').replace('-TamilTunes.com', '')
                music_folder = "TamilTunes/" + music_url.split("/")[-2].replace('%28','(').replace('%29',')').replace('%20', '').replace('%E2%80%93Single','')
                create_folder(music_folder)
                music_path = music_folder + '/' + music_file
                # if debug == True:
                    # print(music_url, " -----> ", music_path)
                if os.path.exists(music_path):
                    print ("Already Downloaded: ", music_file)
                else:
                    try:
                        music_request=urllib2.Request(music_url, None, headers)
                        with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
                            shutil.copyfileobj(response, out_file)
                        print("BUFFERED WRITER?: ", ( re.sub(r'.*\/', '', out_file).strip('\'>')))
                    except:
                        # print ("URL ERROR: Failed to download: ", music_url)
                        continue
                set_id3(music_path)

def getFromSenSongs(link):
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
    print("")
    for l in parser.links:
        if 'mp3' in l['href']:
            music_url = l['href'].replace('\\\'','%27').replace(' ','%20').replace('(','%28').replace(')','%29')
            music_file = music_url.split("/")[-1].replace('%28','(').replace('%29',')').replace('%20', '').replace('%E2%80%93Single','').replace('-SenSongsMp3.Co', '')
            music_folder = "TeluguTunes/" + music_url.split("/")[-2].replace('%28','(').replace('%29',')').replace('%20', '').replace('-320Kbps','').replace('zip','').replace('-SenSongs.Co', '')
            create_folder(music_folder)
            music_path = music_folder + '/' + music_file
            if debug == True:
                print(music_url, " -----> ", music_path)
            music_path = music_folder + '/' + music_file
            if os.path.exists(music_path):
                if debug == True:
                    print ("File already downloaded")
            else:
                music_request=urllib2.Request(music_url, None, headers)
                with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

def getFromSongsPK(link):
    music_folder = "HindiTunes/" + link.split("/")[-1].replace('%20', '').replace('.html','').replace('-mp3-songs-spp04','').replace('-hindi','')
    create_folder(music_folder)
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
    songlist=[]
    rejects=[]
    for l in parser.links:
        try:
            if 'html' in l['href'] and 'song-' in l['href']:
                songlist.append(l['href'])
                if 'image-hover' in l['class']:
                    rejects.append(l['href'])
        except:
            pass
    songlist = [x for x in list(set(songlist)) if x not in rejects]
    print (songlist)
    for song in songlist:
        song_title=song.replace('/','').replace('-mp3-song-spp04.html','')
        headers={'User-Agent':user_agent,}
        request=urllib2.Request('https://songspk.mobi'+song, None, headers)
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
            try:
                if 'mp3slash' in l['href']:
                    music_url = l['href']
                    music_file=song_title+"-"+music_url.split("/")[-1]+".mp3"
                    music_path = music_folder + '/' + music_file
                    if debug == True:
                        print(music_url, " -----> ", music_path)
                    if os.path.exists(music_path):
                        if debug == True:
                            print ("File already downloaded")
                    else:
                        if 'mp3slash' in music_url:
                            print ("YES")
                            music_request=urllib2.Request(music_url, None, headers)
                            with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
                                shutil.copyfileobj(response, out_file)
            except:
                pass

def downloadSongsFromFile():
    album_file="albums.txt"
    if len(sys.argv) > 2:
        print('Usage: {} URL'.format(sys.argv[0]))
        return
    else:
        if len(sys.argv) == 2:
            album_file = sys.argv[1]
        print("album file %s" % album_file)

    with open(album_file) as f:
        albums = f.readlines()
        albums = [x.strip() for x in albums]

    for link in albums:
        print("Downloading Album %30s - " % link.split("/")[3].split("-20")[0], end="", flush=True)
        if "youtube" in link:
            getFromYoutube(link)
            print("DONE - Youtube")
        elif "tamiltunes" in link:
            getFromTamilTunesPro(link)
            print("DONE - TamilTunes")
        elif "sensongs" in link:
            getFromSenSongs(link)
            print("DONE - Sensongs")
        elif "songspk" in link:
            getFromSongsPK(link)
            print("DONE - SongsPK")
        else:
            print("not supported yet")

def downloadTamilSongsOld():
    link = "https://tamiltunes.page/"
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
        if 'html' in l['href'] and 'title' in l.keys() and len(l.keys()) == 2:
            getFromTamilTunesPro(l['href'])



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
            link = self.queue.get()
            try:
                getFromTamilTunesPro(link)
            finally:
                self.queue.task_done()

# Mind the "if" instruction!
def downloadTamilSongs():
    queue = Queue()
    for i in range(multiprocessing.cpu_count()):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()

    link = "https://tamiltunes.page/"
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
        if 'html' in l['href'] and 'title' in l.keys():
            download_link = (re.sub(r'\\\'', '', l['href']))
            # download_link = "https://tamiltunes.page/vijayakanth-hits-59-tamil-songs.html"
            if download_link not in download_links:
                download_links.append(download_link)
                queue.put(download_link)
    # print (download_links)
    queue.join() # starting workers

downloadTamilSongs()