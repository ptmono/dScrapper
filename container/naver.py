#!/usr/bin/python
# coding: utf-8

from base import *
import time

#http://news.naver.com/main/ranking/popularDay.nhn?date=20111114&sectionId=100 정치
class NaverPopularNewsIds:
    politics		= '100'
    finance		= '101'
    community		= '102'
    living		= '103'                # living/art
    world		= '104'
    science		= '105'
    entertainment	= '106'
    sports		= '107'
    photo		= '003'
    tv			= '115'
       



class NaverPopularNewsBase(InfoBase):
    """

    >>> naverpoli = NaverPopularNewsBase()
    >>> naverpoli.get()

    >>> naverpoli.container.char_set
    'euc-kr'

    >>> len(naverpoli)
    30

    >>> # _getTop3Base
    >>> aa = naverpoli._getTop3Base()
    >>> len(aa)
    3

    >>> aa = naverpoli._getOtherBase()
    >>> len(aa)
    27

    >>> aa = naverpoli.getTitle()
    >>> len(aa)
    30

    >>> aa = naverpoli.getUrl()
    >>> len(aa)
    30

    >>> del aa
    """
    base_url = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=%s&date=%s'
    section_id = NaverPopularNewsIds.politics

    def __init__(self):
        self.date = None
        self.url = None
        super(NaverPopularNewsBase, self).__init__(self.url)
        self.elements_top3 = None
        self.elements_other = None
        self.setUrl()

    def setPage(self, date=None):
        self.setUrl(date)

    def setUrl(self, date=None):
        if date:
            self.date = date
        else:
            self.date = self.currentDate()

        self.url = self.base_url % (self.section_id, str(self.date))

    @classmethod
    def currentDate(self):
        # Naver popular news fixed in pm 12. Current date news are
        # updated on a hour.
        return self._currentDate(-1)

    @classmethod
    def _currentDate(self, forward=None):
        date = time.strftime("%Y%m%d")
        if forward:
            date = str(int(date) + forward)
        return date

    def get(self):
        if not self.url:
            raise AttributeError("Object has None url")
        self.container = Container(self.url, charset='euc-kr', webkit=True)
        self.elements_top3 = self._getTop3Base()
        self.elements_other = self._getOtherBase()
        self._getAll()

    def _getTop3Base(self):
        selector = 'div[class="ranking_top3 "] dt a'
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        return sel_list


    def _getOtherBase(self):
        selector = 'ol[class="all_ranking"] dt a'
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        return sel_list

    def getTitle(self):
        result = []
        for element in self.elements_top3:
            result.append(element.get('title'))

        for element in self.elements_other:
            result.append(element.get('title'))
        return result
            
    def getUrl(self):
        result = []
        for element in self.elements_top3:
            result.append(element.get('href'))

        for element in self.elements_other:
            result.append(element.get('href'))
        return result



# TODO: Is other way to create containers?
class NaverPopularNewsScienceContainer(NaverPopularNewsBase):
    '''
    >>> aa = NaverPopularNewsWorldContainer()
    >>> aa.get()
    >>> len(aa)
    30
    '''
    section_id = NaverPopularNewsIds.science

class NaverPopularNewsPoliticsContainer(NaverPopularNewsBase):

    section_id = NaverPopularNewsIds.politics

class NaverPopularNewsWorldContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.world

class NaverPopularNewsFinanceContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.finance

class NaverPopularNewsCommunityContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.community

class NaverPopularNewsLivingContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.living

class NaverPopularNewsPhotoContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.photo

class NaverPopularNewsTvContainer(NaverPopularNewsBase):
    section_id = NaverPopularNewsIds.tv

