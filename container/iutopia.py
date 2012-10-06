#!/usr/bin/python
# coding: utf-8

from base import *


class IutopiaMovieContainer(InfoBase):
    """

     - Get infos of (number, title, url, view, recommendation)

    >>> iutopia = IutopiaMovieContainer()
    >>> iutopia.get()
    >>> #iutopia._getBase('span[class="mw_basic_list_num"]')
    >>> #iutopia._getBase('td[class="mw_basic_list_subject"] a')
    >>> #iutopia._getBase('td font b')

    >>> len(iutopia.getNumbers())
    30
    >>> len(iutopia.getVotes())
    30
    >>> len(iutopia.getTitles())
    30
    >>> len(iutopia.getUrls())
    30

    >>> len(iutopia.infos)
    30

    >>> iutopia.setPage(3)
    >>> iutopia.get()
    >>> len(iutopia)
    30
    """
    url = 'http://iutopia.info/bbs/board.php?bo_table=movie_t'
    #url = 'http://iutopia.info/bbs/board.php?bo_table=movie_t&page=2'
    def __init__(self, page=None):
        super(IutopiaMovieContainer, self).__init__(self.url)
        self.notice_counter = None
        self.setPage(page)

    def get(self):
        if not self.url:
            raise AttributeError("Object has None url")
        self.container = Container(self.url)
        self.notice_counter = self._noticeCounter()
        self._getAll()

    def setPage(self, page=None):
        if page:
            self.url = self.url + '&page=' + str(page)

    def getNumbers(self):
        return self._getBase('span[class="mw_basic_list_num"]')

    def getTitles(self):
        result = []
        selector = ('td[class="mw_basic_list_subject"]')
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        # Remove notices
        sel_list = sel_list[self.notice_counter:]

        # The class of class contains two <a> tag. One is for title. Other
        # is for the number of comment. We does not need the number of
        # comment.
        for html in sel_list:
            selector = 'td a'
            sel = CSSSelector(selector)
            sel_list2 = sel(html)
            try:
                result.append(sel_list2[0].text)
            except UnicodeDecodeError:
                result.append("UnicodeDecodeError")
        return result

    def getUrls(self):
        result_prefix = "http://iutopia.info"
        result = []
        selector = ('td[class="mw_basic_list_subject"]')
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        sel_list = sel_list[self.notice_counter:]

        for html in sel_list:
            selector = 'td a'
            sel = CSSSelector(selector)
            sel_list2 = sel(html)
            try:
                comment_part_of_sel = sel_list2[0]
                href = comment_part_of_sel.get('href')
                # The link has the form
                # '../bbs/board.php?bo_table=movie_t&wr_id=1422791&rand=1319864275'
                href = result_prefix + href[2:]
                result.append(href)
            except UnicodeDecodeError:
                result.append("UnicodeDecodeError")
        return result

    def getHits(self):
        objs = self._getBase('td[class="mw_basic_list_hit"]')
        objs = objs[self.notice_counter:]
        return objs

    def getVotes(self):
        objs = self._getBase('td font b')
        objs = objs[self.notice_counter:]
        return objs


    def __for_test(self, selector):
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        return sel_list

    def _noticeCounter(self):
        """
        Our CSSSelector contains the notices. The number of notice is
        variable. And we don't need that. This function helps to remove
        the notices.
        """
        selector = 'span[class="notice"]'
        sel = CSSSelector(selector)
        sel_list = sel(fromstring(self.container.source))
        return len(sel_list)


