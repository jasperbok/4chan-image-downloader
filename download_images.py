import os
import subprocess
import sys
import re
import urllib

class ImageBoardDownloader:
    """Finds images and downloads them from 4Chan."""

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

    def report(self):
        """
        Returns a single line in which the current status of the downloader
        is shown.

        """
        return 'Awaiting user input...' 

    def make_url(self, board, tread):
        """Return the absolute URL derived from the board and tread number."""
        return 'http://boards.4chan.org/' + board + '/res/' + tread

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
        # download_images(check_file_duplicates(img_urls))

    def find_image_urls(self, url):
        """
        Finds all the images that should be downloaded.

        """
        img_urls = []
        html = urllib.urlopen(url).read()
        tmp_urls = re.findall('(/[A-Za-z]+/src/\d+\.)(jpeg|jpg|png|gif)', html)

        for img in tmp_urls:
            img_urls.append('http://images.4chan.org' + img[0] + img[1])

        return list(set(img_urls))

    def remove_duplicates(self):
        """
        Removes URLs from the self.image_urls list that were previously
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

class FourChanDownloader(ImageBoardDownloader):
    def __init__(self):
        self.name = '4chan'

    def make_url(self, board, tread):
        """Return the absolute URL derived from the board and tread number."""
        return 'http://boards.4chan.org/' + board + '/res/' + tread

daemons = []

def initialize():
    website = raw_input('From what website are we going to download?\n\n1 - 4chan\n2 - desuchan\n')
    if website == '1':
        daemons.append(FourChanDownloader())
    elif website == '2':
        import desuchan_helper as helper
        website = 'desuchan'
    else:
        print 'That\'s not a valid option. Please choose something else.'
        initialize()
    '''
    tread_alias = ''
    with open('tread_aliases.txt', 'r') as alias_file:
        for line in alias_file:
            line = line.replace('\n', '')
            if '#' in line:
                continue
            tread_number, alias = line.split('=')
            if tread == tread_number:
                tread_alias = alias
                break
        if not tread_alias:
            user_entered_alias = raw_input('Do you want to give an alias to this tread number?\nEnter an alias or leave blank not to\n')
            if user_entered_alias:
                tread_alias = user_entered_alias
                with open('tread_aliases.txt', 'r') as alias_file:
                    contents = alias_file.read()
                contents = contents.rstrip()
                with open('tread_aliases.txt', 'w') as alias_file:
                    alias_file.write(contents + '\n' + tread + '=' + tread_alias)
            else:
                tread_alias = tread
    '''
    print 'We\'re going to download from ' + url
    img_urls = helper.find_image_urls(url)


def check_file_duplicates(files, directory=""):
    dupes = []
    if not directory:
        directory = os.getcwd()
    for file in files:
        if os.path.isfile(os.path.join(directory, file.split('/')[-1])):
            dupes.append(file)
    for file in dupes:
        files.remove(file)
    print str(len(dupes)) + ' files already exist on disk, so we\'re gonna download ' + str(len(files)) + ' files'
    return files


if __name__ == '__main__':
    initialize()
