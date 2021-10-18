import multiprocessing as mp
import numpy as np
import requests
import time
import re
import os
import sys
import eyed3
eyed3.log.setLevel("ERROR")

hexaPattern = r'%[0-9a-fA-F]{2}'
bitratePattern = r'[0-9]{3}kbps'
yearPattern = r'[12]{1}[0-9]{3}'
def fixTag(tag):
    # Preliminary change, must modify for each website
    def fixWebsiteName(file):
        file = re.sub(r'Masstamilan\.in','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Masstamilan','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Starmusiq\.la', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Starmusiq', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'www\.', '', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'\. In', '', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r' In\$', '', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'\.info', '', file, flags=re.IGNORECASE).lstrip()
        return file

    # Common stuff
    def fixPunctuation(file):
        file = re.sub(hexaPattern, '', file)
        file = re.sub(bitratePattern, '', file, flags=re.IGNORECASE)
        file = re.sub(yearPattern, '', file)
        file = re.sub('_','', file)
        file = re.sub(r'\:','', file)
        file = re.sub(r'\[','', file)
        file = re.sub(r'\]','', file)
        file = re.sub(r'\(\)', '', file)
        file = re.sub(r'\.+', '.', file)
        file = re.sub(r'^ ', '', file)
        file = re.sub(r'-\.', '.', file)
        file = re.sub(r'-', '', file)
        # file = re.sub(r'-+$', '', file)
        return file.title().lstrip().rstrip()

    m = re.match(' a r ', tag, flags=re.IGNORECASE)
    if m:
        print ("FIX THIS NAME!!: ", m.groups())

    return fixPunctuation(fixWebsiteName(tag))
def fixTitleNames(title):
    title = re.sub(r'^[0-9]{2}', '', title).lstrip()
    title = re.sub(r'^.+', '', title).lstrip()
    return title

def fixArtistNames(artist):
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'&', ', ', artist)
    artist = re.sub(r'  ', ' ', artist)

    # Specific artist names
    artist = re.sub(r' and', ';', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a\.r\.', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kj ', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'k\.j\.', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'spb ', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r's\.p\.b.', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\ Lasubrahmanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubrahmanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubramaniam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubramanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;La', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubrahmanyam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubramaniam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubramanyam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\; Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Shanka R', 'Shankar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sanka R', 'Shankar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sridha R', 'Sridhar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sekha R', 'Sekhar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'kakka R', 'Kakkar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aalaa R Ja', 'Aalap Raja',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Dhanya R', 'Dhanyasri',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Srika R', 'Srikar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Kuma R', 'Kumar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vanija R M', 'Vani Jayaram',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vani ja R M', 'Vani Jayaram',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Deepan Cha R Varthy', 'Deepan Chakravarthy',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S\. P\. Balasubrahmanyam', 'S P B',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S Janki', 'S Janaki',artist, flags=re.IGNORECASE)
    artist = re.sub(r'La ;', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'G V Nd', 'Govind', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Wa R Er', 'Warrier', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ba R R', 'Basrur', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ha R S', 'Harris', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jayaraj', 'Jeyaraj', artist, flags=re.IGNORECASE)
    artist = re.sub(r'B; Charan', 'B Charan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'B;Charan', 'B Charan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ba R M', 'Balram', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Niza R', 'Nizar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Chola R Saya', 'Solar Sai', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aiva R', 'Aivar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sola R', 'Solar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'sheka R', 'Shekar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'sunda R', 'Sundar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Snda R', 'Sundar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aishwa r a', 'Aishwarya', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sathya r kash', 'Sathya Prakash', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Uma R Manan', 'Uma Ramanan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B ', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P Ba ', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P Ba\;', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Subramaniyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'gv ', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Chorus', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'g\.v\.', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S A R Jkumar', 'S A Rajkumar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sa R Jkumar', 'S A Rajkumar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Varsha R Njith', 'Varsha Ranjith', artist, flags=re.IGNORECASE)
    artist = re.sub(r'5Eli Com', '', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Vathu', 'Aaravathu', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Yaan', 'Aariyaan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Am', 'Aarvam', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Sh Ganash', 'Amresh Ganesh', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Tha', 'Amrutha', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Arrorahman', 'A R Rahman', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Isaignani Illayaraaja', 'Ilaiyaraaja', artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;La\;', 'S P B;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R T', 'Amrit', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Mili Na R A R T', 'Milli Nair; Amrit', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Hi', 'Aarthi', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R An', 'Aryan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Ag V Ntira', 'A Raaga Ventira', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Pa R Pazhanisamy','Pa Ra Pazhanisamy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Seka R','Sekar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a R\;','ar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sega R','Segar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Cha R','Chakri', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sudhaka R','Sudhakar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Nambia R','Nambiar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sowmta R O','Sowmya Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ranina R Ddy','Ranina Reddy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Gopa R O','Gopal Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'P Suseela','P Susheela;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'ks chitra','K S Chitra;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'jairam','jayaram;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'R O','Rao', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jeya R E','Jeyashree;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vijaya R Ash','Vijay Prakash;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vija R Kash','Vijay Prakash;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jaya R','Jayashree;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'La R Nce','Lawrence;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sa R M','Sargam;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ragovinda R', 'Raghavendra;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Nambiya R','Nambiar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Maria R E','Maria Roe;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Maa R M','Maatram;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Na R','Nair;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Shilpa R O','Shilpa Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Rao','Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Viswanathan Ramamoorthy','M S Viswanathan; T K Ramamoorthy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Viswanathan\–Ramamoorthy','M S Viswanathan; T K Ramamoorthy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a R Shnan','akrishnan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a R Shan','akrishnan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vidyasaga R','Vidyasagar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sudha R Ghunathan', 'Sudha Raghunathan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Steeve Vatz A K A R Ky',' Steevevatz',artist, flags=re.IGNORECASE)
    artist = re.sub(r'R Jeshwaran', 'Rajeshwaran;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Ham','Abraham', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Dha R J','Dhiraj',artist, flags=re.IGNORECASE)
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'-', ' ', artist)
    artist = re.sub(r'<', ' ', artist)
    artist = re.sub(r'>', ' ', artist)
    artist = re.sub(r'{', ' ', artist)
    artist = re.sub(r'}', ' ', artist)
    artist = re.sub(r'/', ' ',artist)
    artist = re.sub(r'\\', ' ',artist)
    artist = re.sub(r' +', ' ', artist)
    artist = re.sub(r',', ';',artist)
    artist = re.sub(r' ;', ';',artist)
    artist = re.sub(r';+', ';',artist)
    artist = re.sub(r';$', '',artist)
    artist = artist.title().lstrip().rstrip()
    return artist

def spaceOutName(name_title):
    for w in re.findall(r'[A-Z]', name_title):
        name_title = re.sub(w, ' ' + w, name_title)
    return fixTag(re.sub(r' +',' ', name_title).lstrip())
def getTitle(tag, filename):
    if tag.title:
        return spaceOutName(tag.title)
    name_title = os.path.basename(filename.strip('.mp3'))
    return spaceOutName(name_title)

def getAlbum(tag, filename):
    if tag.album:
        return tag.album
    filename_split = os.path.dirname(filename).split('\\')
    if len(filename_split) == 1:
        filename_split = os.path.dirname(filename).split('/')
    if len(filename_split) == 1:
        print("Failed to split filename")
        return ""
    else:
        return spaceOutName(filename_split[-1])

def getYear(tag, filename):
    if tag.getBestDate():
        return str(tag.getBestDate())
    filename_split = os.path.dirname(filename).split('\\')
    if len(filename_split) == 1:
        filename_split = os.path.dirname(filename).split('/')
    if len(filename_split) == 1:
        print("Failed to split filename")
        return ""
    else:
        return filename_split[-2]

def getAlbumArt(image_url, image_file):
    # download album art file
    if not os.path.exists(image_file):
        with open(image_file, 'wb') as handle:
            img_resp = requests.get(image_url, stream=True)
            if not img_resp.ok:
                print (img_resp)
            for block in img_resp.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    return image_file

try:
    import urllib.request as urllib2
except ImportError:
    import urllib

from html.parser import HTMLParser
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
from bs4 import BeautifulSoup

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        if attr not in self.links:
            self.links.append(attr)

    def handle_data(self, data):
        # return
        self.data.append(data)

def parseLinks(values, parserlinks, key):
    for value in set(values):
        for l in parserlinks:
            try:
                if value in l[key]:
                    # print (value, l[key])
                    download_link = re.sub(r'\\\'', '', l[key])
                    # print(download_link)
                    return download_link
            except:
                pass

def urlParse(link, key='href', values=['https'], regex='', data = False):
    # print ("Parsing " , link, "with value ", values, " at ", key)
    headers={'User-Agent':user_agent,}
    request=urllib2.Request(link, None, headers)
    try:
        response = urllib2.urlopen(request)
        html = response.read()
        response.close()
    except urllib2.HTTPError as e:
        print(e, 'while fetching url ', link)
        return
    parser = MyHTMLParser()
    parser.links = []
    parser.data = []
    parser.feed(str(html))
    # print (html)
    download_links = []
    if data:
        for d in parser.data:
            cleantext = BeautifulSoup(d, "lxml").text
            soundtrack = re.search(r'Soundtrack.*', cleantext.replace('\n',' '))
            if soundtrack:
                print(soundtrack.groups())
    else:
        # print ("Parsing Links: ", values, " from: ", parser.links, " with key: ", key)
        download_link = parseLinks(values, parser.links, key)
        try:
            if download_link not in download_links and re.search(regex, download_link):
                download_links.append(download_link)
        except:
            pass
    return download_links

def searchWikipedia(metadata, filename, tag):

    song_title = getTitle(tag, filename)
    album_title = getAlbum(tag, filename)
    album_year = getYear(tag, filename)

    # print ("")
    #TODO: USE GOOGLE SEARCH TO UPDATE METADATA
    # metadata = audio.tag.title + " " + audio.tag.artist.split(",")[0]
    # print ("Searching Google for metadata", metadata)
    # try:
    #     for url in searchGoogle(metadata, stop=1):
    #         r = requests.get(url)
    #         title = re.search('<title>(.*)</title>', r.text)
    #         print(title.group(1))
    # except:
    #     print ("Failed to search google ")
    #     pass

    link_to_parse = "https://en.wikipedia.org/wiki/List_of_Tamil_films_of_" + album_year
    search_values = []
    search_values.append("wiki/" + album_title.replace(' ', '_'))
    search_values.append("wiki/" + album_title.split(' ')[0])
    search_values.append("wiki/" + album_title.split(' ')[0][:5])

    dl = urlParse(link_to_parse, values = search_values) #, r'\b[12]{1}[0-9]{3}\b')

    if dl:
        link_to_parse = "https://en.wikipedia.org" + dl[0]
        # album_art_file, album_art_name = getAlbumArt(link_to_parse, filename)
        # album_art_data = open(album_art_file,"rb").read()
        # if album_art_data:
        # metadata['image_url'] = "https://en.wikipedia.org" + dl[0]
        # print("[W:image_url]", "https://en.wikipedia.org" + dl[0])

            # print (album_art_data)
        #     tag.images.set(3, album_art_data, "image/jpeg", album_art_name)

        r = requests.get(link_to_parse)
        try:
            album_artist_temp = re.search("Music by</th><td>(.*)</td></tr><tr>", r.text)
            if album_artist_temp:
                metadata['album_artist'] = re.sub(r'\;.*', '', BeautifulSoup(album_artist_temp.groups()[0].replace('<br', ', <br').replace('<tr>',' ; <tr>'), "lxml").text)
                # print("[W:album_artist]", metadata['album_artist'])
        except:
            print ("Failed to get album artist info")
        short_titles = []
        orig_title = song_title.split(' ')[0]
        short_titles.append(orig_title[:5])
        try:
            short_titles.append(orig_title.replace('l', 'zh')[:5])
            short_titles.append(orig_title.replace('al', 'aazh')[:5])
            short_titles.append(orig_title.replace('aal', 'azh')[:5])
            short_titles.append(orig_title.replace('zh', 'l')[:5])
            short_titles.append(orig_title.replace('aazh', 'al')[:5])
            short_titles.append(orig_title.replace('azh', 'aal')[:5])
            short_titles.append(orig_title.replace('dh', 'th')[:5])
            short_titles.append(orig_title.replace('th', 'dh')[:5])
            short_titles.append(orig_title.replace('aa', 'a')[:5])
            short_titles.append(orig_title.replace('a', 'aa')[:5])
            short_titles.append(orig_title[:4])
            short_titles.append(orig_title[1:5])
            short_titles.append(orig_title[2:6])
        except:
            pass
        # print (r.text)
        artist_temp=re.compile("id=\"Soundtrack\"" + "(.*)" + "id=\"References", re.DOTALL).search(r.text)
        if not artist_temp:
            artist_temp=re.compile("id=\"Music\"" + "(.*)" + "id=\"References", re.DOTALL).search(r.text)
        if artist_temp:
            raw_html = re.sub(r'Critical.*', '', re.sub(r'References.*','', re.sub(r'Release.*','', re.sub(r'Reception.*','', artist_temp.groups()[0])))).replace('</th>',',</th>').replace('</td>',',</td>').replace('</tr>',';</tr>')
            # print (raw_html)
            bs = re.sub(r'\,+\;', ';', BeautifulSoup(raw_html, "lxml").text.replace('\n', '').replace('Track No',';Track No').replace('No.',';No.').replace('Track',';Track').replace('S/N',';S/N').replace('Song N',';Song N').replace('SN.',';SN.').replace('No,',';No,').replace('\"',''))
            artist_description = bs.replace(';','\n').split('\n')

            title_row = []
            for row in artist_description:
                # print(row)
                if len(row) < 100:
                    if "Singer" in row or "Artist" in row:
                        # print (len(row))
                        title_row = row.split(',')
            # print ("TITLE ROW ", title_row)

            def find_artist_details(data, keys):
                def find_index(keys):
                    for i, val in enumerate(title_row):
                        for key in keys:
                            if key in val:
                                return i
                artist_id = find_index(['Singer', 'Artist'])
                title_id = find_index(['Song', 'Title'])

                def cleanArtistNames(name):
                    return re.sub(r';$','', re.sub(r'[0-9]:.*','', re.sub(r'[0-9][0-9]:.*','', ';'.join(name))))

                for i, row in enumerate(data):
                    # print ("ROW:", row)
                    for short_title in keys:
                        if short_title in row and len(row) < 140:
                            row_items = row.split(',')
                            if metadata['title'] == " ":
                                try:
                                    metadata['title'] = row_items[title_id].replace('\"','')
                                except:
                                    pass

                            if metadata['artist'] == " " and artist_id:
                                if len(row_items) > artist_id:
                                    metadata['artist'] = cleanArtistNames(row_items[artist_id:])
                                else:
                                    # Search previous or next row
                                    j = i - 1
                                    while j >= 0:
                                        # print(j, i)
                                        prev_row = artist_description[j].split(',')
                                        if len(prev_row) > artist_id:
                                            metadata['artist'] = cleanArtistNames(prev_row[artist_id:])
                                        j = j - 1
                            if metadata['title'] != " " and metadata['artist'] != " ":
                                return

            find_artist_details(artist_description, short_titles)

    if metadata['title'] == " ":
        metadata['title'] = song_title
    if "Singer" in metadata['artist'] or "Artist" in metadata['artist'] or "composed" in metadata['artist']:
        metadata['artist'] = " "
    # print("[W:title]", metadata['title'])
    # print("[W:artist]", metadata['artist'])
    return metadata

from collections import defaultdict
from ShazamAPI import Shazam

def searchShazam(metadata, filename):
    # if metadata['title'] != " " and metadata['album'] == " " and metadata['artist'] == " " and metadata['album_artist'] == " " and metadata['image_url'] == " ":
    #     return metadata

    song_info = open(filename, 'rb').read()
    shazam = Shazam(song_info)
    recognize_generator = shazam.recognizeSong()
    dict = {}
    for i in range (len(next(recognize_generator))):
        song_dict = next(recognize_generator)[i]
        try:
            dict = song_dict['track']
            break
        except:
            continue
    for d in dict:
        if d == "title":
            title_album = dict[d].split("(From")
            if metadata['title'] == " ":
                metadata['title'] = title_album[0]
                # print("[S:title " , metadata['title'], "]")
            if metadata['album'] == " " and len(title_album) > 1:
                metadata['album'] = re.sub(r'\"','', title_album[1].strip(")"), flags=re.IGNORECASE).lstrip()
                # print("[S:album " , metadata['album'], "]")
        if d == "subtitle":
            if metadata['artist'] == " ":
                metadata['artist'] = dict[d]
                # print("[S:artist " , metadata['artist'], "]")
        if d == "sections":
            album_artist = next(x['name'] for x in dict[d] if "ARTIST" in x['type'])
            if metadata['album_artist'] == " ":
                metadata['album_artist'] = album_artist
                # print("[S:album_artist " , metadata['album_artist'], "]")
        if d == "images":
            image_url = next(dict[d][x] for x in dict[d] if "coverart" in x)
            if metadata['image_url'] == " ":
                metadata['image_url'] = image_url
                # print("[S:image_url " , metadata['image_url'], "]")

    return metadata

def updateSongMetaData(filename, tag):
    md = {}
    md['title'] = " "
    md['artist'] = " "
    md['album'] = " "
    md['album_artist'] = " "
    md['image_url'] = " "
    md = searchWikipedia(md, filename, tag)
    md = searchShazam(md, filename)
    try:
        print(filename + " [" + tag.title + "," + tag.album + "," + tag.artist + "," + tag.album_artist + "] --> [" + md['title'] + "," +  md['album'] + "," + md['artist'] + "," + md['album_artist'] + "]")
    except:
        pass
    if md:
        if md['title'] != " ":
            if not tag.title or tag.title == " ":
                tag.title = md['title']
        if md['artist'] != " ":
            if not tag.artist or tag.artist == " ":
                tag.artist = md['artist']
        if md['album_artist'] != " ":
            if tag.album_artist == " ":
                tag.album_artist = md['album_artist']
        if md['album'] != " ":
            if not tag.album or tag.album == " ":
                tag.album = md['album']
        if md['image_url'] != " ":
            image_file = getAlbumArt(md['image_url'], os.path.join(os.path.dirname(filename), getAlbum(tag, filename) + ".jpg"))
            image_data = open(image_file,"rb").read()
            # tag.images.set(3, image_data, "image/jpeg", tag.title)
            # print ("WIKIPEDIA image_url: ", tag.images, "->", md['image_url'])
    return tag


import logging
logger = logging.getLogger(__name__)
class eyed3Tagger:
    def clearUnwantedTagEntries(self, tag):
        tag.copyright = ""
        tag.encoded_by = ""
        tag.publisher = ""
        tag.original_artist = ""
        tag.artist_url = ""
        tag.composer = ""
        tag.commercial_url = ""
        tag.audio_file_url = ""
        tag.audio_source_url = ""
        tag.internet_radio_url = ""
        tag.publisher_url = ""
        tag.copyright_url = ""
        tag.comments.set(u"")
        tag.lyrics.set(u"")
        
        if not tag.title or tag.title ==  "" or "Song" in tag.title or "Track" in tag.title or "Uncategorized" in tag.title or "Untitled" in tag.title or "Unknown" in tag.title:
            tag.title = " "
        if not tag.album or tag.album ==  "" or "Movie" in tag.album or "Uncategorized" in tag.album or "Untitled" in tag.album or "Unknown" in tag.album:
            tag.album = " "
        if not tag.artist or tag.artist ==  "" or "Singer" in tag.artist or "Artist" in tag.artist or "composed" in tag.artist or "Untitled" in tag.artist or "Unknown" in tag.artist:
            tag.artist = " "
        if not tag.album_artist or tag.album_artist ==  "" or "Singer" in tag.album_artist or "Artist" in tag.album_artist or "composed" in tag.album_artist or "Untitled" in tag.album_artist or "Unknown" in tag.album_artist:
            tag.album_artist = " "

        return tag

    def dump_eyed3_tag(self, tag):
        all_items = ['version', 'composer', 'comments', 'bpm', 'play_count', 'publisher', 'cd_id', 'images', 'lyrics', 'disc_num', 'objects', 'privates', 'popularities', 'genre', 'non_std_genre', 'user_text_frames', 'commercial_url', 'copyright_url', 'audio_file_url', 'audio_source_url', 'artist_url', 'internet_radio_url', 'payment_url', 'publisher_url', 'user_url_frames', 'unique_file_ids', 'terms_of_use', 'copyright', 'encoded_by', 'chapters', 'table_of_contents', 'album_type', 'artist_origin', 'original_artist']
        for i in all_items:
            tag_type = getattr(tag, i)
            if type(tag_type) == str and tag_type != '': # and "Mass" in tag_type:
                tag_type = fixTag(tag_type)
                logging.info("Tag1:\t %s\t:%s", i, tag_type)
        logging.error("[ %20s\t%20s\t%20s\t%5s\t%20s", tag.title, tag.album, tag.album_artist, tag.getBestDate(), tag.artist)

    def cleanUpTags(self, filename, tag):
        tag.title = spaceOutName(getTitle(tag, filename))

        # Updating Album-Artist
        album_artist = tag.album_artist if tag.album_artist else ""
        if not tag.album_artist:
            if tag.composer:
                tag.album_artist = tag.composer
                tag.composer = None
            elif tag.artist:
                tag.album_artist = tag.artist.split(",")[0]
        if tag.album_artist:
            tag.album_artist = fixArtistNames(tag.album_artist)

        if tag.album_artist:
            tag.album_artist = fixArtistNames(fixTag(tag.album_artist))
        # Updating Arist
        artist = tag.artist
        if not tag.artist or tag.artist == tag.composer:
            if tag.album_artist != tag.artist:
                tag.artist = tag.album_artist

        if tag.artist:
            tag.artist = fixArtistNames(fixTag(tag.artist))

        # Split filename
        filename_split = os.path.dirname(filename).split('\\')
        if len(filename_split) == 1:
            filename_split = os.path.dirname(filename).split('/')

        # Updating Album
        tag.album = fixArtistNames(fixTag(getAlbum(tag, filename)))

        if tag.artist == tag.album:
            tag.artist = " "

        if tag.album_artist == tag.album:
            tag.album_artist = " "

        if tag.album == tag.title:
            tag.album = " "

        if not tag.title or tag.title ==  "" or "Song" in tag.title or "Track" in tag.title or "Uncategorized" in tag.title or "Untitled" in tag.title or "Unknown" in tag.title:
            tag.title = " "

        # Fixup Year
        if not tag.recording_date:
            year = re.search(r'\b[12]{1}[0-9]{3}\b', str(tag.album))
            if not year:
                year = getYear(tag, filename)
            if year:
                try:
                    tag.release_date = year
                    tag.recording_date = year
                except:
                    pass

        # Fixup Album Name
        if tag.album:
            album = tag.album
            tag.album = re.sub(r' \(\b[12]{1}[0-9]{3}\b\)', '', tag.album)

        return tag

    def setTag(self, filename):
        """Module to read MP3 Meta Tags.

        Accepts Path like object only.
        """
        if not ".mp3" in filename and not ".MP3" in filename:
            return

        audio = eyed3.load(filename)
        if not audio:
            logging.error('failed to add tag for %s, invalid load', filename)
            return
        # print ("Processing ", filename)
        # =========================================================================
        # Set Variables
        # =========================================================================
        if not audio.tag:
            return
        audio.tag.read_only = False

        for y in audio.tag.images:
            audio.tag.images.remove(y.description)

        # if debug:
        #     input("Press Enter to confirm...")
        # Save Tags
        audio.tag = self.clearUnwantedTagEntries(audio.tag)
        audio.tag = self.cleanUpTags(filename, audio.tag)
        audio.tag = updateSongMetaData(filename, audio.tag)
        audio.tag = self.cleanUpTags(filename, audio.tag)
        # Optional step to dump the tags
        # self.dump_eyed3_tag(audio.tag)

        try:
            audio.tag.save()
            audio.tag.save(version=(2, 3, 0))
            audio.tag.save(version=(1, 0, 0))
        except eyed3.id3.tag.TagException as e:
            logging.error('failed to save tag for %s, %s, Use %s', filename, e, audio.tag.version)

        # Using a different tool for addressing paranoia

        # renamed_file = os.path.join(os.path.dirname(filename), audio.tag.title) + ".mp3"
        # print("renaming file: ", filename, " to ",renamed_file)
        # os.rename(filename, renamed_file)
        # except:
            # print ("Failed to edit metadata for file: ",filename)

def singleThreaded(fileList):
    results = []
    for fileName in fileList:
        # print (fileName)
        results.append(eyed3Tagger().setTag(fileName))
    return results

def multiThreaded(fileList):
    results = []
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(eyed3Tagger().setTag, [f for f in fileList])
    pool.close()
    return results

if __name__ == '__main__':
    fileList = []
    startpath = "D:\\Music\\Tamil\\1950"
    if sys.argv[1:]:
        startpath = "".join(sys.argv[1:])

    _start = time.time()

    for root, dirs, files in os.walk(startpath): #os.getcwd()):
        for file in files:
            filePath = os.path.join(os.path.abspath(root), file)
            if (os.path.exists(filePath)):
                fileList.append(filePath)

    print("Preprocessing {0} files took {1} seconds".format(len(fileList), time.time() - _start))
    # print(fileList[:5])
    _start = time.time()
    results = multiThreaded(fileList)
    # results = singleThreaded(fileList)

    print("Tag editing took {0} seconds".format(time.time() - _start))
    # print("Result: ", results[:10])
