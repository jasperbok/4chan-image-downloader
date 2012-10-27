import ConfigParser

from image_downloader import ImageBoardDownloader

daemons = []
settings = {}
boards = []

def initialize():
    # Read settings from the settings.txt file.
    with open('settings.txt', 'r') as settings_file:
        for line in settings_file:
            setting_name, setting_value = line.strip().split(' = ')
            setting_value = setting_value.strip()
            settings[setting_name] = setting_value.replace('\n', '')

    # Read all available boards.
    with open('boards.txt', 'r') as boards_file:
        entry = {}
        counter = 0
        for line in boards_file:
            if not line.strip():  # An empty line indicates a new entry.
                entry['rescan_time'] = int(settings['rescan_time'])
                boards.append(entry)
                entry = {}
                counter = 0
            else:
                data = line.strip()
                if counter == 0:
                    entry['name'] = data
                elif counter == 1:
                    entry['regex'] = data
                elif counter == 2:
                    entry['image_url'] = data
                else:
                    entry['url_template'] = data
                counter = counter + 1

    # Ask user for a website to download from.
    add_downloader()

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

def add_downloader():
    print 'What website do you want to download from?'

    if (len(boards) is 0):
        print '\nOops, there are no boards available.\n\nAdd one or more boards to your boards.txt file.'
    else:
        for board in boards:
            print str(boards.index(board)) + ' = ' + board['name']
        website = int(raw_input('0 - ' + str(len(boards) - 1) + '?'))
    if isinstance(website, int) and website < len(boards):
        daemons.append(ImageBoardDownloader(boards[website]))
    else:
        print 'That\'s not a valid option. Please choose something else.'
        add_downloader()
    

if __name__ == '__main__':
    initialize()
