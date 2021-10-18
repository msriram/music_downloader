
from __future__ import print_function, unicode_literals
import sys

import eyed3Tagger

import shutil
import re
import os

import eyed3
import sys
import logger
eyed3.log.setLevel("ERROR")

import logging
logger = logging.getLogger(__name__)

# logging.basicConfig(filename='edit_tags.log',level=logging.INFO)
# logging.info('Sample Info Log')

debug = True


import multiprocessing
from queue import Queue
from threading import Thread

class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            file = self.queue.get()
            try:
                eyed3Tagger.setTag(file)
            finally:
                self.queue.task_done()

def list_files(startpath):
    queue = Queue()
    for i in range(128):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    for root, dirs, files in os.walk(startpath): #os.getcwd()):
        for file in files:
            filePath = os.path.join(os.path.abspath(root), file)
            if (os.path.exists(filePath)):
                # if debug:
                    # logging.info('Setting tag for %s', filePath)
                queue.put(os.path.abspath(filePath))
    queue.join()

if __name__ == "__main__":
    if sys.argv[1:]:
        path_to_check = "".join(sys.argv[1:])
        list_files(path_to_check)

    else:
        for i in range(1940, 2021):
            path_to_check = "D:\\Music\\Tamil\\" + str(i)
            print (path_to_check)
            list_files(path_to_check)
        # print("Please pass the paths to check as parameters to the script")

# list_files('123Music/1979')
# list_files('Bigil(2019)')
# set_id3("C:\\Users\Sriram\Documents\dev\music_downloader\TamilTunes\Dagaalty(2020)\AaliyahAaliyah.mp3")
