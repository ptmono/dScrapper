import re
import os
import imdb
import Image
from StringIO import StringIO
from subprocess import Popen, PIPE

import urllib2, time
try:
    from BeautifulSoup import BeautifulSoup
    MODULE_BEAUTIFULSOUP = True
except ImportError:
    MODULE_BEAUTIFULSOUP = False

from lxml.cssselect import CSSSelector
from lxml.html import parse, fromstring, tostring


from base_webkit import WebkitInterface

    

class Container(object):
    """

    >>> url = 'http://iutopia.info/bbs/board.php?bo_table=movie_t'
    >>> container = Container(url)
    >>> container.source[30]
    u'/'

    >>> url = 'http://news.naver.com/main/ranking/popularDay.nhn?date=20111114&sectionId=100'
    >>> n_container = Container(url)
    >>> n_container.char_set
    'EUC-KR'

    >>> url = 'http://iutopia.info/bbs/board.php?bo_table=movie_t'
    >>> container = Container(url, 'euc-kr', webkit=True)
    >>> container.source[30]
    '/'

    >>> url = 'http://news.naver.com/main/ranking/popularDay.nhn?date=20111114&sectionId=100'
    >>> n_container = Container(url, 'euc-kr', webkit=True)
    >>> n_container.char_set
    'euc-kr'
    """
    def __init__(self, url, charset=None, webkit=False):
        self.url = url
        self.char_set = charset
        self.webkit = webkit
        
        self.d = urllib2
        self.source = None
        self.get()

    def get(self, url=None):
        if url:
            self.url = url

        if self.webkit:
            self._getWithWebkit()
        else:
            self._getWithUrllib2()

    def _getWithUrllib2(self):
        fd = self._downAUrl(self.url)
        self.source = fd.read()
        self._setCharset(fd)

        # TODO: Automatically detect character encoding. We can get the
        # information from http request.
        
        # if chardet.detect(_content)['encoding'] == 'EUC-KR': _content =
        # unicode(_content, 'euc-kr').encode('utf-8')
        if self.char_set:
            try:
                self.source = self.source.decode(self.char_set)
            except LookupError:
                pass

    def _getWithWebkit(self):
        # webkit = WebkitInterface()
        # webkit.getSource(self.url, self.char_set)
        # self.source = webkit.source

        path_base = os.path.abspath(__file__)
        path = path_base[:os.path.dirname(path_base).rfind('/')] + "/dbs/uuwebkit.html"

        ab_base_webkit = os.path.dirname(path_base) + "/base_webkit.py"

        Popen(["python", ab_base_webkit, self.url, str(self.char_set), path],
              stdout=PIPE).communicate()[0]
        fd = open(path, 'r')
        self.source = fd.read()
        fd.close()

    def _setCharset(self, fd):
        try:
            content = fd.headers['content-type']
        except KeyError:
            pass

        pattern = re.compile('charset=(.*)')
        search = pattern.search(content)
        if search:
            self.char_set = search.group(1)

    def pretty(self, url=None):
        if url:
            self.get(self.url)
        if not self.source:
            return "We need pretty(url) or do get(url)"
            
        soup = BeautifulSoup(self.source)
        return soup.prettify()

    def save(self, path):
        fd = open(path, 'w')
        fd.write(self._downAUrl(self.url).read())
        fd.close()
    
    def _downAUrl(self, url):
        """There was urllib2.URLError 110. 110 is time out error. So we
        try 5 times more."""
        i = 0
        while i != 5:
            try:
                dn = self.d.urlopen(url)
                return dn
            except:
                time.sleep(1)
                i = i + 1
        raise 'urllib2.URLError', 'I think server is blocking you'


class InfoBase(object):
    """
    The class return the list of line infomation some like
    [dictionary1,dictionary2 ...]
    where dictionary is like
    {'votes': '3', 'hits': '17', 'titles': 'Metallica RockInRio Brazil 26-09-2011', 'numbers': '17804'}

    From above dictionary the infomation is 'votes', 'hits', 'titles',
    'numbers'. We have to parse the information. We will separately parse
    each information on a page as list. The class merge the information as
    the list of dictionary.

    To get the list of 'titles' you have to create 'getTitles' method that
    returns the list of titles on the page. Write the methods for 'votes',
    'hits', 'numbers' as 'getVotes', 'getHits', 'getNumbers'. It also
    returns the list of that information.
    
    >>> info = InfoBase()
    >>> info.infos = [{'votes': '3', 'hits': '17', 'titles': 'Metallica RockInRio Brazil 26-09-2011', 'numbers': '17804', 'links': '../bbs/board.php?bo_table=movie_t&wr_id=1300054'}]

    """
    def __init__(self, url=None):
        self.url = url
        self.infos = []
        self.container = None
        self.iter_counter = 0

    def __iter__(self):
        return self

    def next(self):
        if self.iter_counter is len(self):
            self.iter_counter = 0
            raise StopIteration
        result = self.infos[self.iter_counter]
        self.iter_counter +=1
        return result
        
    def __len__(self):
        return len(self.infos)

    def __getitem__(self, key):
        return self.infos[key]

    def reverse(self):
        self.infos.reverse()

    def get(self):
        if not self.url:
            raise AttributeError("Object has None url")
        self.container = Container(self.url)
        self._getAll()

    def parsingMethods(self):
        result = []
        pattern = re.compile('get(\w+)')
        for a in dir(self):
            match = pattern.match(a)
            if match:
                element = match.group(1).lower()
                result.append(element)
        return result

    def _getAll(self):
        results = []
        self.infos = []
        p_methods = self.parsingMethods()
        methods_length = len(p_methods)
        for m in p_methods:
            method = getattr(self, 'get' + m.capitalize())
            db = method()
            results.append(db)

        method_length = len(results[0])
        for counter in range(method_length):
            element = {}
            for num in range(methods_length):
                element[p_methods[num]] = results[num][counter]
            self.infos.append(element)
        self.infos.reverse()

        
    def _getBase(self, selector):
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        #result = image_names = [name.get('value') for name in sel_list]
        return [name.text for name in sel_list]

    def _getBaseGetAttr(self, selector, attr):
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        #result = image_names = [name.get('value') for name in sel_list]
        return [name.get(attr) for name in sel_list]


class MovieInfo(object):
    """

    >>> movie = MovieInfo('superman')
    >>> movie.get()			#doctest: +ELLIPSIS
    {'rating': 7.3, 'votes': ..., 'outline': u"An alien orphan is sent from his dying planet to Earth, where he grows up to become his adoptive home's first and greatest super-hero.", 'title': u'Superman', 'image': u'http://ia.media-imdb.com/images/M/MV5BMjE4MDM1MzIwNF5BMl5BanBnXkFtZTYwNTc5MDQ5.jpg', 'genres': [u'Action', u'Adventure', u'Sci-Fi'], 'year': 1978}


    # >>> movie.next()		#doctest: +SKIP
    # >>> movie.get()		#doctest: +SKIP

    # >>> movie.infos		#doctest: +SKIP
    # >>> len(movie.cover())
    # 34511
    # >>> movie['image']
    # u'http://ia.media-imdb.com/images/M/MV5BMjE4MDM1MzIwNF5BMl5BanBnXkFtZTYwNTc5MDQ5.jpg'

    # # We couldn't found the result
    # >>> movie = MovieInfo('   ')
    # >>> movie.get()
    # {'rating': '', 'votes': '', 'outline': '', 'title': '', 'image': '', 'genres': '', 'year': ''}

    # >>> len(movie.cover())
    """
    # You can find full list in imdb.Movie.py file.
    require_infos = [('title', 'title'),
                     ('year', 'year'),
                     ('rating', 'rating'),
                     ('votes', 'votes'),
                     ('plot outline', 'outline'),
                     ('full-size cover url', 'image'),
                     ('genres', 'genres')]

    def __init__(self, title=None):
        self.infos = {}
        self.title = title
        self.imdbObj = imdb.IMDb()
        # Disable the loggers for testing.
        self.imdbObj._imdb_logger.propagate = False
        self.imdbObj._http_logger.propagate = False
        self.s_result = self.imdbObj.search_movie(self.title)
        self.s_result_counter = 0

    def get(self):
        "Returns the first result."
        try:
            s_obj = self.s_result[self.s_result_counter]
        except IndexError:
            # There is no movie data
            for key_imdb, key_info in self.require_infos:
                self.infos[key_info] = ''
            return self.infos

        self.imdbObj.update(s_obj)
        for key_imdb, key_info in self.require_infos:
            try:
                self.infos[key_info] = s_obj[key_imdb]
            except KeyError:
                self.infos[key_info] = ''
        return self.infos

    def next(self):
        self.s_result_counter += 1

    def __getitem__(self, key):
        return self.infos[key]
        
    def test(self):
        s_result = self.imdbObj.search_movie(self.title)
        return s_result
        
    def cover(self):
        # DONE: resize image. It requires info for image format.
        url = self.infos['image']

        if url:
            return self._cover(url)
        return ''

    def _cover(self, url):
        container = Container(url)
        container.save('imdb_image.jpg')

        im = Image.open('imdb_image.jpg')
        resize_resolution = self._coverResize(im.size, 430)

        out = im.resize(resize_resolution, Image.ANTIALIAS)
        fd = StringIO()
        out.save(fd, "JPEG")
        return fd.getvalue()


    def _coverResize(self, size, width):
        "Resize SIZE with WIDTH."
        xsize, ysize = size
        if xsize <= width:
            return size
        rate = float(width)/float(xsize)
        height = int(ysize*rate)
        return (width, height)
