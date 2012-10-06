#!/usr/bin/python
# coding: utf-8

from base import *

class ParkozImageContainer(InfoBase):
    """
    """
    url = "http://www.parkoz.com/zboard/zboard.php?id=images2&category=1"

        def __init__(self, page=None):
        super(YtnBreakingContainer, self).__init__(self.url)
        self.setPage(page)
        self.elements = None

    def get(self):
        if not self.url:
            raise AttributeError("Object has None url")
        self.container = Container(self.url, 'euc-kr')
        self.elements = self._getBaseElements()
        self._getAll()

    def setPage(self, page=None):
        if page:
            self.url = 'http://www.parkoz.com/zboard/zboard.php?id=images2&page=' + str(page)

    def _getBaseElements(self):
        selector = ('tr.TRBG')
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        return sel_list

    def getTitles(self):
        result = []
        for element in self.elements:
            # The element has 4 tags when there is video. There is no
            # video when the element has 3 tags.
            if len(element) == 4:
                result.append(element[1][0].text)
            else:
                result.append(element[0][0].text)
        return result
        
    def getUrls(self):
        result = []
        for element in self.elements:
            if len(element) == 4:
                videop = True
            else:
                videop = False
            # has the form '[2011-10-31 07:48]'
            #date = element[-1].text
            # has the form '/_ln/0102_201110310749257297'
            link = element[0][0].get('href')

            def createLink(link, videop):
                # The video link is
                # mms://nvod1.ytn.co.kr/general/mov/2011/1031/201110310357578021_s.wmv
                if not videop:
                    return "http://www.ytn.co.kr" + link
                filename_prefix = link[10:]
                year = filename_prefix[:4]
                month_day = filename_prefix[4:8]
                return "mms://nvod1.ytn.co.kr/general/mov/" + \
                    year + "/" + \
                    month_day + "/" + \
                    filename_prefix + "_s.wmv"
            
            result.append(createLink(link, videop))
        return result

    def getNumbers(self):
        result = []
        for element in self.elements:
            filename_prefix = element[0][0].get('href')[10:]
            result.append(filename_prefix)
        return result
            
            
