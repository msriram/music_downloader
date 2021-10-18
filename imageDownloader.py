import re
import os
import urlParser
def getAlbumLink(album_link, filename):
    img_dl = urlParser.parse(album_link, values = ['jpg', 'png', 'jpeg'])
    if len(img_dl) == 0:
        print ("Invalid album link")
        return

    image_link =  "https://en.wikipedia.org" + img_dl[0]
    img_link  = urlParser.parse(image_link, values = ['jpg', 'png', 'jpeg'])

    album_art_path = os.path.dirname(filename)
    # album_art_name = os.path.basename(os.path.dirname(filename)).replace(' ','_') + os.path.splitext(img_link[0])[1]
    image_file = os.path.join(album_art_path, album_art_name)
    image_url = re.sub(r'^\/\/', 'https://', img_link[0])         
    # print ("ALBUM ART LINK: ", album_art_url)
    # print ("ALBUM ART PATH: ", album_art_path)
    # print ("ALBUM ART NAME:", album_art_name)
    # print ("ALBUM ART FILE:", image_file)

    return getAlbumArt(image_url, image_file)

def getAlbumArt(image_url, image_file):
    

    # download album art file
    if not os.path.exists(image_file):

        with open(image_file, 'wb') as handle:
            img_resp = requests.get(image_url, stream=True)

            if not img_resp.ok:
                print (img_resp)

            for block in img_resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    return image_file
    