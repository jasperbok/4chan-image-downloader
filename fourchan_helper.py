import re
import urllib

def make_url(board, tread):
    """Return the absolute URL derived from the board and tread number."""
    return 'http://boards.4chan.org/' + board + '/res/' + tread


def find_image_urls(url):
    img_urls = []
    html = urllib.urlopen(url).read()
    tmp_img_urls = re.findall('(/[A-Za-z]+/src/\d+\.)(jpeg|jpg|png|gif)', html)

    for img in tmp_img_urls:
        img_urls.append('http://images.4chan.org' + img[0] + img[1])

    return list(set(img_urls))
