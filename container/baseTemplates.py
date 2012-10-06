from base import InfoBase, Container

from lxml.cssselect import CSSSelector
from lxml.html import fromstring, tostring

class InfoBaseTemplateA(InfoBase):
    '''
    Many case on tr contains all info for specified number. So we will
    extrat information from tr tag.

    '''

    url_format = None
    base_url = None
    base_selector = None
    number_selector = None
    title_selector = None
    url_selector = None

    def __init__(self, page=None):

        if page: self.setPage(page)
        else: self.setPage(1)

        super(InfoBaseTemplateA, self).__init__(self.url)
        self.elements = None


    def get(self):
        if not self.url:
            raise AttributeError("Object has None url")
        self.container = Container(self.url, 'euc-kr', webkit=True)
        self.elements = self._getBaseElements()
        self._getAll()

    def setPage(self, page=None):
        if page:
            self.url = self.url_format % str(page)

    def _getBaseElements(self):
        selector = (self.base_selector)
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        print self.url
        print "sel_list", sel_list
        return sel_list

    def _getBase(self, selector):
        result = []
        for element in self.elements:
            sel = CSSSelector(selector)
            sel_list = sel(element)
            print tostring(sel_list[0])
            result.append(sel_list[0].text)
        return result

    def _getBaseGetAttr(self, selector, attr):
        result = []
        for element in self.elements:
            sel = CSSSelector(selector)
            sel_list = sel(element)
            # sel_list has only one element
            result .append(sel_list[0].get(attr))
        return result
    
    def getNumbers(self):
        return self._getBase(self.number_selector)

    def getTitles(self):
        return self._getBase(self.title_selector)

    def getUrls(self):
        return [self.base_url + url for url in self._getBaseGetAttr(self.url_selector, 'href')]


class InfoBaseTemplateATesting(InfoBaseTemplateA):
    '''
    >>> aa = InfoBaseTemplateATesting()
    >>> aa.get()
    >>> aa.infos

    '''
    url_format = 'http://www.parkoz.com/zboard/zboard.php?id=images2&page=%s'
    base_url = 'http://www.parkoz.com/zboard/'
    base_selector = 'tr.TRBG'
    number_selector = "td.thm8 font"
    title_selector = "td.thm9 a"
    url_selector = "td.thm9 a"

    def getTitles(self):
        result = []
        for element in self.elements:
            sel = CSSSelector(self.title_selector)
            sel_list = sel(element)
            #print tostring(sel_list[0], encoding='utf-8')
            # aa = sel_list[0].text_content()
            # print aa
            # text_content will returns only text part
            result.append(sel_list[0].text_content())
        return result
