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
debug = True
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

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
	else:
		if debug == True:
			print ("Directory already present %s" % folder)

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
				music_file = music_url.split("/")[-1].replace('%28','(').replace('%29',')').replace('%20', '').replace('%E2%80%93Single','').replace('-TamilTunes.com', '')
				music_folder = "TamilTunes/" + music_url.split("/")[-2].replace('%28','(').replace('%29',')').replace('%20', '').replace('%E2%80%93Single','')
				create_folder(music_folder)
				if debug == True:
					print(music_url)
					print(music_file)
					print(music_folder)
				music_path = music_folder + '/' + music_file
				if os.path.exists(music_path):
					if debug == True:
						print ("File already downloaded")
				else:
					music_request=urllib2.Request(music_url, None, headers)
					with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
						shutil.copyfileobj(response, out_file)

def getFromTeluguSongs(link):
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
			if debug == True:
				print(music_url)
				print(music_file)
				print(music_folder)
			music_path = music_folder + '/' + music_file
			if os.path.exists(music_path):
				if debug == True:
					print ("File already downloaded")
			else:
				if '\.mp3' in music_url:
					music_request=urllib2.Request(music_url, None, headers)
					with urllib2.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
						shutil.copyfileobj(response, out_file)

def downloadTamilSongs():
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
			getFromTeluguSongs(link)
			print("DONE - Sensongs")
		else:
			print("not supported yet")

downloadTamilSongs()
