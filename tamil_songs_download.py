################ DOWNLOAD TAMIL SONGS FROM TAMIL TAMILTUNES.PRO ###################
from __future__ import print_function
import urllib, sys
import urllib.request
from html.parser import HTMLParser
import shutil
import os
debug = False

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

def downloadTamilSongs():
	if len(sys.argv) != 2:
		print('Usage: {} URL'.format(sys.argv[0]))
		return
	headers={'User-Agent':user_agent,}
	request=urllib.request.Request(sys.argv[1], None, headers)

	try:
		response = urllib.request.urlopen(request)
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
				music_url = l['href']
				music_file = music_url.split("/")[-1].replace('%20', '').replace('-TamilTunes.com', '')
				music_folder = music_url.split("/")[-2].replace('%20', '')
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
					music_request=urllib.request.Request(music_url, None, headers)
					with urllib.request.urlopen(music_request) as response, open(music_path, 'wb') as out_file:
						shutil.copyfileobj(response, out_file)

downloadTamilSongs()
