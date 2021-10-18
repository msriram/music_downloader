################ DOWNLOAD TAMIL SONGS FROM TAMIL TAMILTUNES.PRO ###################
#TODO: Download lyrics
#TODO: Download images

from __future__ import print_function, unicode_literals
import sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib
from html.parser import HTMLParser
import logging
import requests
import shutil
import re
import os
try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
logging.basicConfig(filename='awesome_downloading.log',level=logging.DEBUG)

# def searchWikipedia(query, url):
#     # result = urlsParse(url)
#     album_artist = ""
#     artist = ""
#     try:
#         r = requests.get(url)
#         # print (r.text)
#         res  = re.search("Music by</th><td>(.*)</td></tr><tr>", r.text)
#         if res:
#             album_artist = (re.sub(r'<.*', '', res .groups()[0]))
#         res = re.search(query + "\" - (.*)</li>", r.text)
#         if res:
#             artist = res.groups()[0].replace(',',';')
#     except:
#         print ("failed to search wikipedia")
#         pass    
#     print(album_artist)
#     print (artist)
    #         print(title.groups())
import re

def cleanhtml(raw_html):
    #   cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

from bs4 import BeautifulSoup

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        self.links.append(attr)

    def handle_data(self, data):
        # return
        self.data.append(data)

def urlDataParse(link, key='href', value='https', regex=''):
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
    parser.data = []
    print (html)
    parser.feed(str(html))
    metadata = {}

    data = []
    for d in parser.data:
        print (d)
        if 'schema' in d:
            # print (d)
            data = d.lstrip('{').rstrip('}').replace('":"','","').replace('"','').replace('Thing, name', '').split('{')
            # print (data)
    
    def strip_details(data):
        return re.sub(r'-[0-9]{2}-[0-3][0-9]','', re.sub(r'}.*','',re.sub(r'.*name,','',data)))
    
    def list_to_dict(lst):
        length = ((len(lst) - 1) // 2) * 2
        res_dct = {lst[i]: lst[i + 1] for i in range(0, length, 2)}
        return res_dct
    
    dic = list_to_dict(re.sub('duration.*','',data[0]).split(','))
    metadata['title'] = dic['name']
    metadata['image_url'] = dic['image']
    metadata['genre'] = dic['inLanguage']
    metadata['album'] = strip_details(data[1])
    metadata['artist'] = strip_details(data[2])
    metadata['year'] = strip_details(data[3])
    metadata['album_artist'] = strip_details(data[4])

    return metadata

def searchSaavn(query):

    query.append("saavn")
    try:
        for url in search("".join(query), tld="com", stop=1):
            if "saavn" in url:
                metadata = urlDataParse(url, 'screen_name', 'song_screen')
                print ("title:" , metadata['title'])
                print ("year:", metadata['year'])
                print ("album:" , metadata['album'])
                print ("artist:" , metadata['artist'])
                print ("album_artist:" , metadata['album_artist'])
                print ("image_url:" , metadata['image_url'])
                print ("genre:" , metadata['genre'])
                return metadata
    except:
        print("Failed to parse Saavn metadata")

# query = ["Kondayil Thazhampoo", "Annamalai"]
# query = ["Saarale Saarale", "Vedikundu Murugesan"]
# print (query)
# searchSaavn(query)
# TODO: search https://mymazaa.com/
# import cProfile
# cProfile.run('getMetadata()')
# exit(1)

def urlParse(link, key='href', value='https', regex='', data = False):
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
    parser.data = []
    parser.feed(str(html))
    download_links = []
    if data:
        for d in parser.data:
            
            cleantext = BeautifulSoup(d, "lxml").text
            soundtrack = re.search(r'Soundtrack.*', cleantext.replace('\n',' '))
            if soundtrack:
                print(soundtrack.groups())
 
            # print (cleantext)

            # try:
            #     print (d)

            #     if value in d:
            #         print (d)
            # except:
            #     print ("Failed to locate ", value, " in the page")
    else:
        for l in parser.links:
            # print (l)
            try:
                if value in l[key]: # change to https
                    # print (l)
                    download_link = (re.sub(r'\\\'', '', l[key]))
                    if download_link not in download_links and re.search(regex, download_link):
                        download_links.append(download_link)
            except:
                pass
    return download_links

import multiprocessing
from queue import Queue
from threading import Thread

class DownloadWorker(Thread):
    filename = ""
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue


    def spaceOutName(self, name_title):
        for w in re.findall(r'[A-Z]', name_title):
            name_title = re.sub(w, ' ' + w, name_title)
        return re.sub(r' +',' ', name_title).lstrip()

    def getTitle(self):
        name_title = os.path.basename(self.filename.strip('.mp3'))
        return self.spaceOutName(name_title)

    def getAlbum(self):
        filename_split = os.path.dirname(self.filename).split('\\')
        if len(filename_split) == 1:
            filename_split = os.path.dirname(self.filename).split('/')
        if len(filename_split) == 1:
            print("Failed to split filename")
            return ""
        else:
            return self.spaceOutName(filename_split[-1])

    def getYear(self):
        filename_split = os.path.dirname(self.filename).split('\\')
        if len(filename_split) == 1:
            filename_split = os.path.dirname(self.filename).split('/')
        if len(filename_split) == 1:
            print("Failed to split filename")
            return ""
        else:
            return filename_split[-2]

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            self.filename = self.queue.get()

            try:
                # print (self.filename)
                query = [self.getTitle(), self.getAlbum()]
                print ("")
                print (query)
                title = ""
                artist = ""
                album_artist = ""
                link_to_parse = "https://en.wikipedia.org/wiki/List_of_Tamil_films_of_" + self.getYear()
                # link_to_parse = "https://en.wikipedia.org/wiki/List_of_Tamil_films_of_1951"
                # print (link_to_parse)
                # print("searching for album: ", self.getAlbum().split(' ')[0])
                # return 
                dl = urlParse(link_to_parse, value = self.getAlbum().split(' ')[0]) #, r'\b[12]{1}[0-9]{3}\b')
                if dl:
                    link_to_parse = "https://en.wikipedia.org" + dl[0]
                    print (link_to_parse)

                    r = requests.get(link_to_parse)
                    # print (r)
                    try:
                        album_artist_temp = re.search("Music by</th><td>(.*)</td></tr><tr>", r.text)
                        if album_artist_temp:
                            album_artist = re.sub(r'\;.*', '', BeautifulSoup(album_artist_temp.groups()[0].replace('<br', ', <br').replace('<tr>',' ; <tr>'), "lxml").text)
                    except:
                        print ("Failed to get album artist info")                
                    # def get_html_between(start_tag, end_tag):
                    #     yield "".join(start_tag.contents)
                    #     all_next = start_tag.find_all_next()
                    #     logging.info('%s', all_next)
                    #     for ele in takewhile(end_tag, all_next):
                    #         yield ele

                    # cond = lambda tag: tag.get("name") == "span" and tag.get("class") != ["mw-headline"]
                    # soup = BeautifulSoup(r.text, "lxml")

                    # for tag in soup.select("span.mw-headline"):
                    #     if "Soundtrack" in tag:
                    #         start_tag = tag
                    #     if "Reception" in tag:
                    #         end_tag = tag
                    # print (start_tag)
                    # print (end_tag)
                    short_titles = []
                    orig_title = self.getTitle().split(' ')[0]
                    short_titles.append(orig_title[:5])
                    short_titles.append(orig_title.replace('l', 'zh')[:5])
                    short_titles.append(orig_title[:4])
                    # print (r.text)
                    artist_temp=re.compile("id=\"Soundtrack\"" + "(.*)" + "id=\"References", re.DOTALL).search(r.text)
                    # print (artist_temp)
                    if not artist_temp:
                        artist_temp=re.compile("id=\"Music\"" + "(.*)" + "id=\"References", re.DOTALL).search(r.text)
                    if artist_temp:
                        raw_html = re.sub(r'Critical.*', '', re.sub(r'References.*','', re.sub(r'Release.*','', re.sub(r'Reception.*','', artist_temp.groups()[0])))).replace('</th>',',</th>').replace('</td>',',</td>').replace('</tr>',';</tr>')
                        # print (raw_html)
                        bs = re.sub(r'\,+\;', ';', BeautifulSoup(raw_html, "lxml").text.replace('\n', '').replace('No.',';No.').replace('S/N',';S/N').replace('SN.',';SN.').replace('No,',';No,'))
                        # print (bs)
                        artist_description = bs.replace(';','\n').split('\n')
                        # print (artist_description)
                        title_row = []
                        for row in artist_description:
                            # print(row)
                            if len(row) < 100:
                                if "Singer" in row or "Artist" in row:
                                    # print (len(row))
                                    title_row = row.split(',')
                        print ("TITLE ROW SIZE", title_row)
                        # if len(title_row) == 0:
                        #     print("Failed to parse artists_info")
                        #     return
                        def find_index(keys):
                            for i, val in enumerate(title_row):
                                for key in keys:
                                    if key in val:
                                        return i

                        idx_artist = find_index(['Singer', 'Artist'])
                        idx_title = find_index(['Song', 'Title'])
                        # print ("idx_title ", idx_title, "idx_artist ", idx_artist)
                        
                        for i, row in enumerate(artist_description):
                            # print ("ROW:", row)
                            for short_title in short_titles:
                                if short_title in row and len(row) < 100:
                                    row_items = row.split(',')
                                    if title == "":
                                        try:
                                            title = row_items[idx_title].replace('\"','')
                                        except:
                                            pass
                                            # print ("From ", row_items, " accessing:", idx_title)

                                    if artist == "":
                                        if len(row_items) > idx_artist:
                                            # print("idx_artist:", idx_artist, "row items length:", len(row_items))
                                            artist = row_items[idx_artist]
                                        else:
                                            j = i - 1
                                            while j >= 0:
                                                # print(j, i)
                                                prev_row = artist_description[j].split(',')
                                                if len(prev_row) > idx_artist:
                                                    artist = prev_row[idx_artist]
                                                j = j - 1
                                        
                print ("title: ", title)
                print ("artist: ", artist)  
                print ("album_artist:", album_artist)


                # SEARCH WIKI (year page)
                # searchSaavn(query)
                # ["Nona Nona", "Aanmai Thavarel"])

            finally:
                self.queue.task_done()

def list_files(startpath):
    queue = Queue()
    for i in range(20):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    for root, dirs, files in os.walk(startpath): #os.getcwd()):
        for file in files:
            filePath = os.path.join(os.path.abspath(root), file)
            if (os.path.exists(filePath)):
                # if debug:
                    # logging.info('Setting tag for %s', filePath)
                queue.put(os.path.abspath(filePath))
            queue.join()

if __name__ == "__main__":
    if sys.argv[1:]:
        path_to_check = "".join(sys.argv[1:])
        list_files(path_to_check)
    else:
        print ("Enter path")
        exit(1)
        for i in range(2010,2020):
            path_to_check = '123Music\\' + str(i)
            print (path_to_check)
            list_files(path_to_check)