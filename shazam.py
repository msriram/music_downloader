# if running in py3, change the shebang, drop the next import for readability (it does no harm in py3)
from collections import defaultdict
import os
import sys
import re
from ShazamAPI import Shazam
import json
import requests
import shutil
from fixNames import fixArtistNames, fixTitleNames, fixTag, spaceOutName, getTitle, getAlbum, getYear
import imageDownloader


def collect_info(dict):
    metadata = {}
    metadata['title'] = " "
    metadata['artist'] = " "
    metadata['album'] = " "
    metadata['album_artist'] = " " 
    metadata['image_url'] = " " 
    for d in dict:
        if d == "title":
            title_album = dict[d]
            title_album = title_album.split("(From")
            # print (title_album)
            try:
                metadata['title'] = title_album[0]
                metadata['album'] = re.sub(r'\"','', title_album[1].strip(")"), flags=re.IGNORECASE).lstrip()
            except:
                continue
        if d == "subtitle":
            metadata['artist'] = dict[d]
            
        if d == "images":
            for dd in dict[d]:
                if dd == "coverart":
                    metadata['image_url'] = dict[d][dd]
        if d == "sections":
            for l in dict[d]:
                if l['type'] == "ARTIST":
                    metadata['album_artist'] = l['name']


    return metadata
def findSong(full_path):
    song_info = open(full_path, 'rb').read()
    shazam = Shazam(song_info)
    recognize_generator = shazam.recognizeSong()
    try:
        song_dict = (next(recognize_generator)[1])['track'] # current offset & shazam response to recognize requests
        metadata = collect_info(song_dict)
        return metadata
    except:
        return {}

def check_tag(paths):
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if "mp3" in filename or "MP3" in filename:
                    full_path = os.path.join(dirpath, filename)
                    try:
                        # if the target is a symlink (soft one), this will 
                        # dereference it - change the value to the actual target file
                        full_path = os.path.realpath(full_path)
                        md = findSong(full_path)
                        print ("Filename:" + full_path)
                        if md:
                            print ("title: ", md['title'])
                            print ("album: ", md['album'])
                            print ("artist: ", md['artist'])
                            print ("album_artist: ", md['album_artist'])
                            print ("image_url: ", md['image_url'])
                        print ("---------")

                    except (OSError,):
                        # not accessible (permissions, etc) - pass on
                        continue

if __name__ == "__main__":
    if sys.argv[1:]:
        check_tag(sys.argv[1:])
    else:
        print("Please pass the paths to check as parameters to the script")


def searchShazam(filename, tag):
    # print (filename)
    # print(tag)
    md = findSong(filename)
    print ("Filename:" + filename)
    if md:
        print ("title: ", tag.title, "->", md['title'])
        print ("album: ", tag.album, "->", md['album'])
        print ("artist: ", tag.artist, "->", md['artist'])
        print ("album_artist: ", tag.album_artist, "->", md['album_artist'])
        print ("image_url: ", tag.images, "->", md['image_url'])
    print ("---------")
    if md:
        if md['title'] != " " and tag.title == " ":
            tag.title = md['title']

        if md['artist'] != " " and tag.artist == " ":
            tag.artist = md['artist']
            
        if md['album_artist'] != " " and tag.album_artist == " ":
            tag.album_artist = md['album_artist']
            
        if md['album'] != " " and tag.album == " ":
            tag.album = md['album']
        if md['image_url'] != " ":
            image_file = imageDownloader.getAlbumArt(md['image_url'], filename)
            image_data = open(image_file,"rb").read()
            tag.images.set(3, image_data, "image/jpeg", tag.title)
    return tag