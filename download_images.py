from downloaders import fourchan

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

if __name__ == '__main__':
    initialize()
