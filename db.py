#!/usr/bin/python
# coding: utf-8

import os
import sys
import re
import pickle

from elixir import *
from container import IutopiaMovieContainer
from nltk import FreqDist

from sfilter import getTitle

class Movie(Entity):
    #numbers = Field(Integer, required=True, primary_key=True)
    numbers = Field(Integer)
    titles = Field(Text)
    links = Field(Text)
    hits = Field(Integer)
    votes = Field(Integer)


def init(filename):
    """The first time after designing database we need to create tables of
    database and initial database file """
    #TODO: Support abpath of sqlname
    sqlname = "sqlite:///" + filename
    metadata.bind = sqlname
    #metadata.bind = "sqlite:///exercise2.sqlite"
    metadata.bind.echo = False
    # Set up database table from designed classes
    setup_all(False)                    # True shows the query
    # Create the database file
    if not os.path.exists(filename):
        create_all()

def update():
    "Let's commit the database."
    session.commit()


class AnalysisIutopiaMovieDB2(object):
    """

    >>> obj = AnalysisIutopiaMovieDB2()
    >>> obj.saveTitleSet('full_title_set')

    >>> obj.FreqDisk()
    """

    def __init__(self):
        init('iutopia.sqlite')


    def FreqDisk(self):

        fd = file('full_title_set', 'r')
        title_set = pickle.load(fd)
        fd.close()

        fdist = FreqDist(title_set)
        print "===>best 100", repr(fdist.keys()[:20])
        print "==========================="


    def getTitleSet(self):
        dbs = Movie.query.all()
        from blist import blist
        result = blist([])
        for db in dbs:
            striped_string = getTitle(db.titles)
            result.append(striped_string)
        return result

    def saveTitleSet(self, path):
        title_set = self.getTitleSet()
        fd = file(path, 'w')
        pickle.dump(title_set, fd)
        fd.close()



class AnalysisIutopiaMovieDB(object):
    """

    >>> aim = AnalysisIutopiaMovieDB()

    >>> #os.remove('iutopia.sqlite')
    >>> #aim.createDb()

    >>> aim.show()				#doctest: +SKIP
    2970

    >>> bb = aim.getTitleSet(30)		#doctest: +SKIP
    >>> len(bb)					#doctest: +SKIP
    261

    >>> aim.saveTitleSet('title_set')		#doctest: +SKIP

    >>> aim.FreqDisk()

    >>> aim.saveVoteSet()			#doctest: +SKIP
    >>> aim.FreqDiskVote() #doctest: +SKIP

    >>> aim.FreqDistVote()
    >>> aim.FreqDistHit()

    """

    def __init__(self):
        init('iutopia.sqlite')

    def createDb(self):
        iutopia = IutopiaMovieContainer()
        for a in range(1,100):
            iutopia.page(a)
            for element in iutopia.infos:
                movie = Movie()
                movie.from_dict(element)
                update()
                
    def show(self):
        #return session.query(Movie.votes)
        bb = Movie.query.all()
        return len(bb)

    def getTitleSet(self, number):
        result = []
        dbs = Movie.query.all()
        counter = 0

        for b in dbs:
            striped_string = self.strip(b.titles)
            list_striped_string = re.compile(" +").split(striped_string)
            result = result + list_striped_string
            if counter == number:
                break
            else:
                counter += 1
        return result

    def strip(self, s):
        if not s:
            return "None"
        s = s.lower()

        s_filter = StripString()
        s = s_filter.kor(s)

        # Strip
        s_filter.control_chars = "[]"
        s = s_filter.strip(s)

        # Replace to space
        s_filter.control_chars = ".-()"
        s_filter.repl = " "
        s = s_filter.strip(s)

        return s

    def saveTitleSet(self, path):
        title_set = self.getTitleSet(2970)
        fd = file(path, 'w')
        pickle.dump(title_set, fd)
        fd.close()

    def FreqDisk(self):

        fd = file('title_set', 'r')
        title_set = pickle.load(fd)
        fd.close()

        fdist = FreqDist(title_set)
        print "===>best 100", repr(fdist.keys()[:50])
        print "==========================="


    def getVoteSet(self):
        result = []
        dbs = Movie.query.all()

        for b in dbs:
            result.append(b.votes)
        return result

    def saveVoteSet(self):
        vote_set = self.getVoteSet()
        fd = file('vote_set', 'w')
        pickle.dump(title_set, fd)
        fd.close()

    def FreqDistVote(self):
        db = self.getVoteSet()

        fdist = FreqDist(db)
        
        print "FreqDistVote. The number"
        print "========================"
        print len(fdist.items())
        print "\n\n"

        print "FreqDistVote. Top votes"
        print "========================"
        print repr(fdist.items()[:50])
        print "\n\n"

        print "FreqDistVote. Most votes"
        print "========================"
        print repr(sorted(fdist.keys()[-50:], reverse=True))
        print "\n\n"

        print "FreqDistVote. Most votes and frequence"
        print "======================================"
        print repr(sorted(fdist.items()[-50:], reverse=True))
        print "\n\n"

    def getHitSet(self):
        result = []
        dbs = Movie.query.all()

        for b in dbs:
            result.append(b.hits)
        return result

    def FreqDistHit(self):
        db = self.getHitSet()

        fdist = FreqDist(db)
        
        print "FreqDistVote. The number"
        print "========================"
        print len(fdist.items())
        print "\n\n"

        print "FreqDistVote. Top votes"
        print "========================"
        print repr(fdist.items()[:50])
        print "\n\n"

        print "FreqDistVote. Most votes"
        print "========================"
        print repr(sorted(fdist.keys()[-50:], reverse=True))
        print "\n\n"

        print "FreqDistVote. Most votes and frequence"
        print "======================================"
        print repr(sorted(fdist.items()[-50:], reverse=True))
        print "\n\n"





# TODO: I don't like this class. Consider more.
class StripString(object):
    """

    >>> msg = "가나아 ffs 우가가 1234 abcd efgh ijkl mnop qrst uvwx yz 가 마마마!@#$%^&*()}{[]\|"
    >>> snp = StripString()

    >>> snp.charset = 'utf-8'
    >>> snp.kor(msg)
    ' ffs  1234 abcd efgh ijkl mnop qrst uvwx yz  !@#$%^&*()}{[]\\\\|'

    >>> ud = snp.nonKor(msg)
    >>> print ud
    가나아우가가가마마마

    >>> ul = snp.nonLatin(msg)
    >>> print ul
    ffsabcdefghijklmnopqrstuvwxyz

    >>> # Our input string msg is encoded with utf-8
    >>> snp.charset = 'utf-8'
    >>> snp.set(snp.unicode_kor_range + snp.unicode_symbol_range)
    >>> snp.strip(msg)
    'ffsabcdefghijklmnopqrstuvwxyz'

    """
    unicode_kor_range = range(0xac00, 0xd7a3 + 1)
    unicode_symbol_without_space_range = range(0x0021, 0x002f + 1) + \
        range(0x0030, 0x0039 + 1) + \
        range(0x003a, 0x0040 + 1) + \
        range(0x005b, 0x0060 + 1) + \
        range(0x007b, 0x007e + 1)				# space is 0x0020
    unicode_symbol_range = range(0x0020, 0x002f + 1) + \
        range(0x0030, 0x0039 + 1) + \
        range(0x003a, 0x0040 + 1) + \
        range(0x005b, 0x0060 + 1) + \
        range(0x007b, 0x007e + 1)				# space is 0x0020
    unicode_lcl_range = range(0x0041, 0x005a + 1)		# latin capital letters
    unicode_lsl_range = range(0x0061, 0x007a + 1)		# latin small letters

    def __init__(self):
        self.control_chars = None
        self.charset = None
        self.repl = ""

    def check_control_chars(self):
        if not self._check_control_chars():
            raise AttributeError("We has no control_chars.")
        
    def _check_control_chars(self):
        if self.control_chars:
            return True
        return False

    def nonKor(self, s):
        control_chars = ''.join(map(unichr, self.unicode_symbol_range + self.unicode_lcl_range + self.unicode_lsl_range))
        self.control_char_re = re.compile('[%s]' % re.escape(control_chars))
        return self.control_char_re.sub("", s)

    def nonKorAndSpace(self, s):
        self.control_chars = ''.join(map(unichr, self.unicode_symbol_without_space_range + \
                                             self.unicode_lcl_range + \
                                             self.unicode_lsl_range))
        return self.strip(s)

    def nonLatin(self, s):
        self.control_chars = ''.join(map(unichr, self.unicode_symbol_range + self.unicode_kor_range))
        # We have to encode the unicode characters
        return self.strip(s)

    def kor(self, s):
        self.control_chars = ''.join(map(unichr, self.unicode_kor_range))
        return self.strip(s)

    def set(self, chars):
        self.control_chars = ''.join(map(unichr, chars))

    def strip(self, s):
        control_char_re = self._getCompiler()
        return control_char_re.sub(self.repl, s)

    def _getCompiler(self):
        if self.charset:
            return re.compile('[%s]' % re.escape(self.control_chars.encode(self.charset)))
        return re.compile('[%s]' % re.escape(self.control_chars))

    



class Ttest(object):
    anc = 'bbbbb'

def ttestt():
    """
    >>> ttestt()
    'bbbbb'
    """
    tobj = Ttest()
    t = getattr(tobj, 'anc')
    return t
