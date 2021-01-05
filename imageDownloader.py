import re
import os
import urlParser

def getAlbumArt(album_link, filename):
    img_dl = urlParser.parse(album_link, values = ['jpg', 'png', 'jpeg'])
    if len(img_dl) == 0:
        print ("Invalid album link")
        return

    image_link =  "https://en.wikipedia.org" + img_dl[0]
    img_link  = urlParser.parse(image_link, values = ['jpg', 'png', 'jpeg'])

    album_art_path = os.path.dirname(filename)
    album_art_name = os.path.basename(os.path.dirname(filename)).replace(' ','_') + os.path.splitext(img_link[0])[1]
    album_art_file = os.path.join(album_art_path, album_art_name)
    album_art_url = re.sub(r'^\/\/', 'https://', img_link[0])         
    # print ("ALBUM ART LINK: ", album_art_url)
    # print ("ALBUM ART PATH: ", album_art_path)
    # print ("ALBUM ART NAME:", album_art_name)
    # print ("ALBUM ART FILE:", album_art_file)

    # download album art file
    if not os.path.exists(album_art_file):

        with open(album_art_file, 'wb') as handle:
            img_resp = requests.get(album_art_url, stream=True)

            if not img_resp.ok:
                print (img_resp)

            for block in img_resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    return album_art_file, album_art_name
    