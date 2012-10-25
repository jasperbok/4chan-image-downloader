import os
import re
import subprocess
import sys
import urllib

class ImageBoardDownloader:
    """
    A base class that downloads images.
    
    This should not be used 'as is', but should be subclassed instead.
    
    """

    def __init__(self):
        self.setup()
        self.board = raw_input('What board should I download from?\n')
        self.tread = raw_input('What tread number?\n')
        self.base_url = self.make_url(self.board, self.tread)
        self.directory = self.make_directory()
        self.image_urls = self.find_image_urls(self.base_url)
        self.remove_duplicates()
        self.download_images()

    def setup(self):
        self.name = 'Dummy'
        self.image_regex = ''
        self.image_url = ''

    def report(self):
        """
        Returns a single line in which the current status of the downloader
        is shown.

        """
        return 'Awaiting user input...' 

    def make_url(self, board, tread):
        """
        Return the absolute URL derived from the board and tread number.

        This is a dummy function and should be overridden by any subclas.
        
        """
        return ''

    def make_directory(self):
        """
        Creates the directory path where the images will be saved. If the
        directory does not exist it will be created.
        
        TO-DO:
        alias support

        """
        directory = os.path.join(os.getcwd(), self.name, self.board, self.tread)

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory

    def find_image_urls(self, url):
        """
        Find all the images that should be downloaded.

        """
        img_urls = []
        html = urllib.urlopen(url).read()
        tmp_urls = re.findall(self.image_regex, html)

        for img in tmp_urls:
            img_urls.append(self.image_url + img[0] + img[1])

        return list(set(img_urls))

    def remove_duplicates(self):
        """
        Removes URLS from the self.image_urls list that were previously
        downloaded.

        """
        dupes = []

        for file in self.image_urls:
            if os.path.isfile(os.path.join(self.directory, file.split('/')[-1])):
                dupes.append(file)

        for file in dupes:
            self.image_urls.remove(file)

        print str(len(dupes)) + ' Files already exist on disk'

    def download_images(self):
        """
        Download all images from the URLs stored in self.image_urls.

        """
        total_num_images = len(self.image_urls)
        current_image = 1

        for url in self.image_urls:
            print 'DOWNLOADING IMAGE ' + str(current_image) + ' OUT OF ' + str(total_num_images)
            subprocess.call(['wget', '--directory-prefix=' + self.directory, url])
            current_image = current_image + 1
