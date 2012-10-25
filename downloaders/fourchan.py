from image_downloader import ImageBoardDownloader

class FourChanDownloader(ImageBoardDownloader):
    def setup(self):
        self.name = '4chan'
        self.image_regex = '(/[A-Za-z]+/src/\d+\.)(jpeg|jpg|png|gif)'
        self.image_url = 'http://images.4chan.org'

    def make_url(self, board, tread):
        """Return the absolute URL derived from the board and tread number."""
        return 'http://boards.4chan.org/' + board + '/res/' + tread
