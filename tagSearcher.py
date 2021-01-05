import requests
import shutil
import re
import os
import sys
from fixNames import fixArtistNames, fixTitleNames, fixTag, spaceOutName, getTitle, getAlbum, getYear
import urlParser
import imageDownloader
from bs4 import BeautifulSoup
try: 
    from googlesearch import search as searchGoogle
except ImportError:  
    print("No module named 'google' found") 

# def searchSaavn(query):

#     query.append("saavn")
#     try:
#         for url in searchGoogle("".join(query), tld="com", stop=10):
#             if "saavn" in url:
#                 metadata = urlDataParse(url, 'screen_name', 'song_screen')
#                 logging.info('title: %s', metadata['title'])
#                 logging.info('year: %s', metadata['year'])
#                 logging.info('album: %s', metadata['album'])
#                 logging.info('artist: %s', metadata['artist'])
#                 logging.info('album_artist: %s', metadata['album_artist'])
#                 logging.info('image_url: %s', metadata['image_url'])
#                 logging.info('genre: %s', metadata['genre'])
#                 return metadata
#             # else:
#             #     print("Did not return Saavn in search results")
#     except:
#         print("Failed to parse Saavn metadata")

def searchWikipedia(filename, tag):

    song_title = getTitle(tag, filename)
    album_title = getAlbum(tag, filename)
    album_year = getYear(tag, filename)
    query = [song_title, album_title, album_year]

    # print ("")
    metadata = {}
    metadata['title'] = " "
    metadata['artist'] = " "
    metadata['album_artist'] = " " 
        
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

    dl = urlParser.parse(link_to_parse, values = search_values) #, r'\b[12]{1}[0-9]{3}\b')

    if dl:
        link_to_parse = "https://en.wikipedia.org" + dl[0]
        album_art_file, album_art_name = imageDownloader.getAlbumArt(link_to_parse, filename)
        album_art_data = open(album_art_file,"rb").read()
        tag.images.set(3, album_art_data, "image/jpeg", album_art_name)

        r = requests.get(link_to_parse)
        try:
            album_artist_temp = re.search("Music by</th><td>(.*)</td></tr><tr>", r.text)
            if album_artist_temp:
                metadata['album_artist'] = re.sub(r'\;.*', '', BeautifulSoup(album_artist_temp.groups()[0].replace('<br', ', <br').replace('<tr>',' ; <tr>'), "lxml").text)
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
                    return re.sub(r';$','', re.sub(r'[0-9][0-9]:.*','', ';'.join(name)))

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
    if "Singer" in metadata['artist'] or "Artist" in metadata['artist']:
        print("Please verify tag:", query)
        metadata['artist'] = " "
    print (query,  "--> [", metadata['title'], ",", metadata['artist'], ",", metadata['album_artist'], "]")
    return metadata

def update(filename, tag):
    
    # Get Data from Saavn
    # logging.info('Getting from Web %s',query)
    # metadata = searchSaavn(query)
    # response = requests.get("https://i.imgur.com/ExdKOOz.png")

    # file = open("sample_image.png", "wb")
    # file.write(response.content)
    # file.close()
    # tag.images.set(type_=3, img_data=None, mime_type=None, description=saavnMetadata['album'], img_url=saavnMetadata['image_url'])
    metadata = searchWikipedia(filename, tag)
    if metadata is not None:
        if tag.title == "" or tag.title == None:
            if metadata['title'] is not " ":
                tag.title = metadata['title']
        if tag.artist == "" or tag.artist == " " or tag.artist == None or tag.artist == tag.album_artist:
            tag.artist = metadata['artist']
        if tag.album_artist == "" or tag.album_artist == " " or tag.album_artist == None or ';' in tag.album_artist:
            if metadata['album_artist'] is not " ":
                tag.album_artist = metadata['album_artist']
    return tag
