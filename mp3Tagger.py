from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from fixNames import fixArtistNames, fixTitleNames, fixTag

import logging
logger = logging.getLogger(__name__)

def getMp3Tag(filename):
    return MP3File(filename)

def clear(tag, album, title, artist):
    tag.copyright = ""
    tag.url = ""
    tag.publisher = ""
    tag.comment = ""
    tag.composer = ""
    if album:
        tag.album = album
    if title:
        tag.song = fixTitleNames(title)
    if artist:
        tag.artist = fixArtistNames(artist)
    tag.set_version(VERSION_2)
    return tag

def dump(tag):    
    all_items = ['artist','album','song','track','comment','year','genre','band','composer','copyright','url','publisher']
    for i in all_items:
        try:
            tag_type = getattr(tag, i)
            if type(tag_type) == str and tag_type != '': # and "Mass" in tag_type:
                tag_type = fixTag(tag_type)
                logging.info("Tag2:\t %s\t:%s", i, tag_type)
        except TypeError as e:
            logging.error("failed dumping tag %s %s -- %s", i, tag_type, e)
            continue
    logger.info("Tag2 [ %20s\t%20s\t%5s\t%20s", tag.song, tag.album, tag.year, tag.artist)
    return tag
