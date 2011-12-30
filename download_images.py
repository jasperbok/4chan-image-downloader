import os
import subprocess
import sys

def initialize():
    start_dir = os.getcwd()
    website = raw_input('From what board are we going to download?\n\n1 - 4chan\n2 - desuchan\n')
    if website == '1':
        website = '4chan'
        import fourchan_helper as helper
    elif website == '2':
        import desuchan_helper as helper
        website = 'desuchan'
    else:
        print 'That\'s not a valid option. Please choose something else.'
        initialize()
    board = raw_input('What board are we going to download from?\n')
    tread = raw_input('What tread are we going to download?\n')
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
    url = helper.make_url(board, tread)
    print 'We\'re going to download from ' + url
    img_urls = helper.find_image_urls(url)

    if not os.path.exists(os.path.join(start_dir, website, board, tread_alias)):
        os.makedirs(os.path.join(start_dir, website, board, tread_alias))

    os.chdir(os.path.join(start_dir, website, board, tread_alias))
    download_images(check_file_duplicates(img_urls))
    os.chdir(start_dir)

def download_images(urls):
    """Download all images in a list.

    Keyword arguments:
    urls -- a list containing image URLs

    """
    total_num_images = len(urls)
    current_image = 1

    for url in urls:
        print 'DOWNLOADING IMAGE ' + str(current_image) + ' OUT OF ' + str(total_num_images)
        subprocess.call(['wget', url])
        current_image = current_image + 1

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
