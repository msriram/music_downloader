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

def cleanhtml(raw_html):
    #   cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        self.links.append(attr)

    def handle_data(self, data):
        # return
        self.data.append(data)

def pullData(link, key='href', value='https', regex=''):
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

def parse(link, key='href', value='https', regex='', data = False):
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
