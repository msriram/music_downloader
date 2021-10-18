import shutil
import re
import os
import eyed3
import sys
eyed3.log.setLevel("ERROR")

from fixNames import fixArtistNames, fixTitleNames, fixTag, spaceOutName, getTitle, getAlbum, getYear
# import tagSearcher
import shazam
import mp3Tagger
import logging
logger = logging.getLogger(__name__)

def clear_unwanted_tags(tag):
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
    return tag

def dump_eyed3_tag(tag):
    try:
        all_items = ['version', 'composer', 'comments', 'bpm', 'play_count', 'publisher', 'cd_id', 'images', 'lyrics', 'disc_num', 'objects', 'privates', 'popularities', 'genre', 'non_std_genre', 'user_text_frames', 'commercial_url', 'copyright_url', 'audio_file_url', 'audio_source_url', 'artist_url', 'internet_radio_url', 'payment_url', 'publisher_url', 'user_url_frames', 'unique_file_ids', 'terms_of_use', 'copyright', 'encoded_by', 'chapters', 'table_of_contents', 'album_type', 'artist_origin', 'original_artist']
        for i in all_items:
            tag_type = getattr(tag, i)
            if type(tag_type) == str and tag_type != '': # and "Mass" in tag_type:
                tag_type = fixTag(tag_type)
                logging.info("Tag1:\t %s\t:%s", i, tag_type)
        logging.error("[ %20s\t%20s\t%20s\t%5s\t%20s", tag.title, tag.album, tag.album_artist, tag.getBestDate(), tag.artist)
    except:
        pass
def setTag(filename):
    """Module to read MP3 Meta Tags.

    Accepts Path like object only.
    """
    if not ".mp3" in filename and not ".MP3" in filename:
        return
    audio = eyed3.load(filename)
    if not audio:
        logging.error('failed to add tag for %s, invalid load', filename)
        return
    # =========================================================================
    # Set Variables
    # =========================================================================
    audio.tag.read_only = False
    # Cleanup Tags
    audio.tag.title = spaceOutName(getTitle(audio.tag, filename))

    # dump_eyed3_tag(audio.tag)

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

    if audio.tag.album_artist:
        audio.tag.album_artist = fixArtistNames(fixTag(audio.tag.album_artist))
    # Updating Arist
    artist = audio.tag.artist
    if not audio.tag.artist or audio.tag.artist == audio.tag.composer:
        if audio.tag.album_artist != audio.tag.artist:
            audio.tag.artist = audio.tag.album_artist

    if audio.tag.artist:
        audio.tag.artist = fixArtistNames(fixTag(audio.tag.artist))

    # Split filename
    filename_split = os.path.dirname(filename).split('\\')
    if len(filename_split) == 1:
        filename_split = os.path.dirname(filename).split('/')

    # Updating Album
    audio.tag.album = fixArtistNames(fixTag(getAlbum(audio.tag, filename)))

    if audio.tag.artist == audio.tag.album:
        audio.tag.artist = ""

    if audio.tag.album_artist == audio.tag.album:
        audio.tag.album_artist = ""

    # Fixup Year
    try:
        if not audio.tag.recording_date:
            year = re.search(r'\b[12]{1}[0-9]{3}\b', audio.tag.album)
            if not year:
                year = getYear(audio.tag, filename)
            if year:
                audio.tag.release_date = year
                audio.tag.recording_date = year
    except:
        pass

    # Fixup Album Name
    if audio.tag.album:
        album = audio.tag.album
        audio.tag.album = re.sub(r' \(\b[12]{1}[0-9]{3}\b\)', '', audio.tag.album)

        # if debug:
        #     print(album, "---->", audio.tag.album)

    # Misc: Genre, Urls, Images etc
    audio.tag.genre = 'Tamil'
    for y in audio.tag.images:
        audio.tag.images.remove(y.description)


    # if debug:
    #     input("Press Enter to confirm...")
    # Save Tags
    audio.tag = clear_unwanted_tags(audio.tag)
    # audio.tag = tagSearcher.update(filename, audio.tag)
    audio.tag = shazam.update(filename, audio.tag)
    
    dump_eyed3_tag(audio.tag)

    try:
        audio.tag.save()
        audio.tag.save(version=(2, 3, 0))
        audio.tag.save(version=(1, 0, 0))
    except eyed3.id3.tag.TagException as e:
        logging.error('failed to save tag for %s, %s, Use %s', filename, e, audio.tag.version)
    
    # Using a different tool for addressing paranoia
    mp3tag = mp3Tagger.getMp3Tag(filename)
    mp3tag = mp3Tagger.clear(mp3tag, audio.tag.album, audio.tag.title, audio.tag.artist)
    mp3Tagger.dump(mp3tag)
    mp3tag.save()

    # renamed_file = os.path.join(os.path.dirname(filename), audio.tag.title) + ".mp3"
    # print("renaming file: ", filename, " to ",renamed_file)
    # os.rename(filename, renamed_file)
    # except:
        # print ("Failed to edit metadata for file: ",filename)

