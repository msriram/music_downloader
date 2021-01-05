import os
import re
def rename(src_file):
    dst_file = src_file.replace("-.mp3", ".mp3")
    if not os.path.exists(dst_file):
        print ("GOOD! UPDATING")
        os.rename(src_file, dst_file)
    else:
        src_size = os.stat(src_file).st_size
        dst_size = os.stat(dst_file).st_size
        if src_size == dst_size:
            print ("DUPLICATE! SKIPPING")
            os.remove(src_file)
        else:
            diff = src_size - dst_size
            if abs(diff) < 512:
                if src_size <= dst_size:
                    print ("SMALL DIFFERENCE! UPDATING")
                    os.remove(dst_file)
                    os.rename(src_file, dst_file)
                else:
                    print ("SMALL DIFFERENCE! IGNORING")
                    os.remove(src_file)
            else:
                if src_size > dst_size:
                    print ("LARGE DIFFERENCE! UPDATING FILE")
                    os.remove(dst_file)
                    os.rename(src_file, dst_file)
                else:
                    print ("LARGE DIFFERENCE! DELETING BOTH FILES")
                    os.remove(src_file)
                    os.remove(dst_file)

def list_files(startpath):
    for root, dirs, files in os.walk(startpath): #os.getcwd()):
        for file in files:
            filePath = os.path.join(os.path.abspath(root), file)
            if (os.path.exists(filePath)):
                # print (filePath)
                fullPath = os.path.abspath(filePath)
                if "-.mp3" in fullPath:
                    rename(fullPath)

list_files('123Music')

# file = "AADAA---"
# print (file)
# print(re.sub(r'-+$', '', file))
