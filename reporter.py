#!/usr/bin/python
# coding: utf-8

import os.path
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header

from container import IutopiaMovieContainer, MovieInfo, \
    YtnBreakingContainer, \
    ParkozImageContainer

from db import StripString
from sfilter import getTitle
import var


# TODO: subject couldn't support unicode.
class Mailer(object):
    """

    >>> mailer = Mailer()
    >>> mailer.test()
    """
    def __init__(self, subject=None, sender=None, receiver=None, url=None):
        self.subject = subject
        self.sender = sender
        self.receiver = receiver
        self.url = url

        self.outer = MIMEMultipart()

    def attachText(self, text):
        try:
            data = MIMEText(text)
        except UnicodeEncodeError:
            data = MIMEText(text.encode(sys.getfilesystemencoding()))
        self.outer.attach(data)

    def attachImage(self, image):
        data = MIMEImage(image)
        self.outer.attach(data)

    def send(self):
        self.outer['Subject'] = Header(self.subject, sys.getfilesystemencoding())
        self.outer['To'] = self.receiver
        self.outer['From'] = self.sender
        self.outer['X-Gnus-Url'] = self.url

        s = smtplib.SMTP('localhost')
        s.sendmail(self.sender, self.receiver, self.outer.as_string())
        s.quit()

    def test(self):
        self.subject = Header("ssssubject 한글 되남.", 'utf-8')
        self.sender = "aa@aa"
        self.receiver = "ptmono@localhost"

        data = MIMEText("jasldfsdfdsklflkdffkdsflsdfkl 이건한글 되남")
        self.outer.attach(data)

        fd = open('img.jpg', 'r')
        img = MIMEImage(fd.read())
        fd.close()
        self.outer.attach(img)
        self.outer['Subject'] = self.subject
        self.outer['To'] = self.receiver
        self.outer['From'] = self.sender

        s = smtplib.SMTP('localhost')
        s.sendmail("aa@aa", "ptmono@localhost", self.outer.as_string())
        s.quit()


class ReporterCommon(object):
    """
    Basic methods for reporter.

    >>> aa = ReporterCommon()		#doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    NameError: name 'ReporterCommonContainer' is not defined
    """

    start_page = 1
    page_count = 1
    maximum_page = 4

    def __init__(self):
        self.container = self.getContainer()
        self.container.setPage(self.start_page)
        self.container.get()
        #self.container.reverse()

        self.sender = self.getSenderName()

        self.latest_number_filename = self.getLatestNumberName()
        self.latest_number = self.getLatestNumber()
        self.latest_number_candidate = None
        self.we_meet_latest_number = False
        self.latest_number_saved = False

    def getSenderName(self):
        sender_name = self.__class__.__name__ + "@localhost"
        return sender_name

    def getLatestNumberName(self):
        name = "latest_number_" + self.__class__.__name__
        return name

    def getContainer(self):
        container_name = self.__class__.__name__ + "Container"
        return eval(container_name + "()")

    def getLatestNumber(self):
        path = var.db_directory + '/' + self.latest_number_filename
        if not os.path.exists(path):
            self.saveLatestNumber('0')
        fd = file(path, 'r')
        result = fd.read()
        fd.close()
        return result

    def saveLatestNumber(self, num):
        path = var.db_directory + '/' + self.latest_number_filename
        fd = file(path, 'w')
        fd.write(str(num))
        fd.close()

    def report(self):
        try:
            latest_number = int(self.latest_number)
        except:
            self.saveLatestNumber('0')
            latest_number = int(self.latest_number)

        for info in self.container:
            try:
                if int(info['numbers']) <= latest_number:
                    self.we_meet_latest_number = True
                    continue
            except ValueError:
                continue
            self._report(info)

        if not self.latest_number_candidate:
            for a in range(len(self.container), 0, -1):
                try:
                    self.latest_number_candidate = self.container[a]['numbers']
                    int(self.latest_number_candidate)
                    break
                except:
                    continue

        if not self.we_meet_latest_number and self.page_count is not self.maximum_page:
            self.page_count += 1
            self.container.setPage(self.page_count)
            self.container.get()
            self.report()

        if not self.latest_number_saved:
            self.saveLatestNumber(self.latest_number_candidate)
            self.latest_number_saved = True

    def _report(self):
        pass

class ReporterTypeA(ReporterCommon):
    '''
    Basic methods for reporter.

    >>> aa = ReporterCommon()		#doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    NameError: name 'ReporterTypeAContainer' is not defined
    '''
    start_page = 1
    page_count = 1
    maximum_page = 4

    def __init__(self):
        self.container = self.getContainer()
        self.container.setPage(self.start_page)
        self.container.get()
        #self.container.reverse()

        self.sender = self.getSenderName()

        self.latest_number_filename = self.getLatestNumberName()
        self.latest_number = self.getLatestNumber()
        self.latest_number_candidate = None
        self.we_meet_latest_number = False
        self.latest_number_saved = False

    def getSenderName(self):
        sender_name = self.__class__.__name__ + "@localhost"
        return sender_name

    def getLatestNumberName(self):
        name = "latest_number_" + self.__class__.__name__
        return name

    def getContainer(self):
        container_name = self.__class__.__name__ + "Container"
        return eval(container_name + "()")

    def getLatestNumber(self):
        path = var.db_directory + '/' + self.latest_number_filename
        if not os.path.exists(path):
            self.saveLatestNumber('0')
        fd = file(path, 'r')
        result = fd.read()
        fd.close()
        return result

    def saveLatestNumber(self, num):
        path = var.db_directory + '/' + self.latest_number_filename
        fd = file(path, 'w')
        fd.write(str(num))
        fd.close()

    def report(self):
        try:
            latest_number = int(self.latest_number)
        except:
            self.saveLatestNumber('0')
            latest_number = int(self.latest_number)

        for info in self.container:
            try:
                if int(info['numbers']) <= latest_number:
                    self.we_meet_latest_number = True
                    continue
            except ValueError:
                continue
            self._report(info)

        if not self.latest_number_candidate:
            for a in range(len(self.container), 0, -1):
                try:
                    self.latest_number_candidate = self.container[a]['numbers']
                    int(self.latest_number_candidate)
                    break
                except:
                    continue

        if not self.we_meet_latest_number and self.page_count is not self.maximum_page:
            self.page_count += 1
            self.container.setPage(self.page_count)
            self.container.get()
            self.report()

        if not self.latest_number_saved:
            self.saveLatestNumber(self.latest_number_candidate)
            self.latest_number_saved = True

    def _report(self, info):
        pass


class IutopiaMovie(ReporterCommon):
    """

    >>> iutopia = IutopiaMovie()
    >>> iutopia.report()
    """

    condition_hit = None
    condition_vote = None

    title_filter = None
    min_rating = 6

    def _report(self, info):
        assert(isinstance(info, dict))

        title = info['titles']
        try:
            title_en_l = getTitle(title)
        except TypeError:
            # May be title is 'None'
            return
        title_en = title_en_l[1]
        strip_title = title_en_l[0]
        
        movier = MovieInfo(strip_title)
        movier.get()
        movie_cover = movier.cover()
        movie_rating = movier['rating']
        movie_outline = movier['outline']
        try:
            movie_genres = movier['genres'][0] # has form [u'Comedy', u'Crime']
        except IndexError:
            movie_genres = movier['genres']

        if not self._require_rating(movie_rating):
            return
        subject = "(" + str(movie_rating) + ", " + info['votes'] + ", " + info['hits'] + ", " + movie_genres + ") " + title
        #print subject

        mailer = Mailer()
        mailer.sender = self.sender
        mailer.receiver = var.receiver
        mailer.url = info['urls']
        mailer.subject = subject
        mailer.attachText("====================")
        mailer.attachText(title)
        mailer.attachText("====================")
        mailer.attachText(movier['title'])
        mailer.attachText("\n\n")
        mailer.attachText(str(movie_rating))
        mailer.attachText("\n\n")

        try:
            mailer.attachText(movie_outline)
        except UnicodeEncodeError:
            mailer.attachText("The outline contains non-ascii character.")
            
        mailer.attachText("\n\n")
        if movie_cover:
            try:
                mailer.attachImage(movie_cover)
            except:
                pass
        mailer.send()

    def _require_rating(self, rating):
        if rating >= self.min_rating:
            return True
        return False


class YtnBreaking(ReporterCommon):
    """
    >>> ytn = YtnBreaking()
    >>> ytn.report()

    """
    def _report(self, info, virtual=False):
        assert(isinstance(info, dict))

        if info['videop']:
            media = "V"
        else:
            media = "T"

        date = info['numbers'][6:10]
        subject = "(" + media + ", " + date + ") "  + info['titles']

        if not virtual:
            mailer = Mailer()
            mailer.sender = self.sender
            mailer.receiver = var.receiver
            mailer.url = info['urls']
            mailer.subject = subject
            mailer.send()

class ParkozImage(ReporterCommon):
    def _report(self, info, virtual=False):
        assert(isinstance(info, dict))

        subject = info['titles']

        mailer = Mailer()
        mailer.sender = self.sender
        mailer.receiver = var.receiver
        mailer.url = info['urls']
        mailer.subject = subject
        mailer.send()

