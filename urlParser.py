import re
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
        
def parse(link, key='href', values=['https'], regex='', data = False):
    # print ("Parsing " , link, "with value ", values, " at ", key)
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

# def urlDataParse(link, key='href', value='https', regex=''):
#     headers={'User-Agent':user_agent,}
#     request=urllib2.Request(link, None, headers)
#     try:
#         response = urllib2.urlopen(request)
#         html = response.read()
#         response.close()
#     except urllib2.HTTPError as e:
#         print(e, 'while fetching', url)
#         return
#     parser = MyHTMLParser()
#     parser.data = []
#     parser.feed(str(html))
#     metadata = {}

#     data = []
#     for d in parser.data:
#         if 'schema' in d:
#             # print (d)
#             data = d.lstrip('{').rstrip('}').replace('":"','","').replace('"','').replace('Thing, name', '').split('{')
#             # print (data)
    
#     def strip_details(data):
#         return re.sub(r'-[0-9]{2}-[0-3][0-9]','', re.sub(r'}.*','',re.sub(r'.*name,','',data)))
    
#     def list_to_dict(lst):
#         length = ((len(lst) - 1) // 2) * 2
#         res_dct = {lst[i]: lst[i + 1] for i in range(0, length, 2)}
#         return res_dct
    
#     dic = list_to_dict(re.sub('duration.*','',data[0]).split(','))
#     metadata['title'] = dic['name']
#     metadata['image_url'] = dic['image']
#     metadata['genre'] = dic['inLanguage']
#     metadata['album'] = strip_details(data[1])
#     metadata['artist'] = strip_details(data[2])
#     metadata['year'] = strip_details(data[3])
#     metadata['album_artist'] = strip_details(data[4])

#     return metadata
