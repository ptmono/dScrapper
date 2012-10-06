#!/usr/bin/python
# coding: utf-8

# There is a problem in PyQt4 > 4.7. multiple QApplication instances cause
# a segment fault. See
# - http://www.riverbankcomputing.com/pipermail/pyqt/2011-June/029994.html
# - [[~/works/11torrent_merge/container/worknote2.muse#1111272048]]

# So current time I use Popen instead a instance to get the source of the
# webpage.

# This is v 1.8.1 of webparsing.

import sys
import os
import signal
import libs
from libs		import ListOfMethods


from PyQt4.QtCore	import QUrl, SIGNAL, QObject, QString, QTimer, QTextCodec
from PyQt4.QtGui 	import QApplication
from PyQt4.QtWebKit	import QWebPage, QWebView

from urllib2		import urlopen

JQUERY_URL = 'http://jqueryjs.googlecode.com/files/jquery-1.3.2.min.js'
JQUERY_FILE = JQUERY_URL.split('/')[-1]
JQUERY_PATH = os.path.join(os.path.dirname(__file__), JQUERY_FILE)


def get_jquery(jquery_url=JQUERY_URL, jquery_path=JQUERY_PATH):
    """
    Returns jquery source.

    If the source is not available at jquery_path, then we will download it from
    jquery_url.
    """
    if not os.path.exists(jquery_path):
        jquery = urlopen(jquery_url).read()
        f = open(jquery_path, 'w')
        f.write(jquery)
        f.close()
    else:
        f = open(jquery_path)
        jquery = f.read()
        f.close()
    return jquery


class WebPage(QWebPage):
    """
    QWebPage that prints Javascript errors to stderr.
    """
    def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
        sys.stderr.write('Javascript error at line number %d\n' % lineNumber)
        sys.stderr.write('%s\n' % message)
        sys.stderr.write('Source ID: %s\n' % sourceID)


class WebkitInterface(object):
    """

    >>> url = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=100&date=20111116'
    >>> aa = WebkitInterface()
    >>> aa.getSource(url, 'euc-kr')
    """
    show_web_viewp = True
    show_javascript_error = False
    limit_time_for_javascript = 5000 # msecond, 10second

    def __init__(self):
        self.timer = QTimer()
        self.app = QApplication(sys.argv)
        self.jquery = get_jquery()
        self.web_view = QWebView()
        self.web_page = self._webpage()
            
        self.web_view.setPage(self.web_page)

        QObject.connect(self.web_view, SIGNAL('loadFinished(bool)'), self._load_finished)
        #QObject.connect(self.web_view, SIGNAL('loadStarted()'), self.load_started)

        self.set_load_function(None)

        self.source = None
        self.charset = None

    def _webpage(self):
        if self.show_javascript_error:
            return WebPage()
        else:
            return QWebPage()


    def load(self, url, load_function=None):
        qurl = QUrl(url)
        self.set_load_function(load_function)
        current_frame = self.web_page.currentFrame()
        current_frame.load(qurl)

        if self.show_web_viewp:
            self.web_view.show()
        self.app_exec()

    def getSource(self, url):
        qurl = QUrl(url)
        QObject.disconnect(self.web_view, SIGNAL('loadFinished(bool)'), self._load_finished)
        QObject.connect(self.web_view, SIGNAL('loadFinished(bool)'), self._load_get_source)

        current_frame = self.web_page.currentFrame()
        current_frame.load(qurl)
        self.app_exec()

    def _load_get_source(self, ok):
        current_frame = self.web_page.currentFrame()
        self._get_source(current_frame)
        self.app_exit()

    def _get_source(self, current_frame):
        # TODO: Automatically detect charset from metadata.
        # qwebframe.metaData() seems poor.

        source = current_frame.toHtml()
        if self.charset == "euc-kr":
            # For euc-kr
            QTextCodec.setCodecForCStrings(QTextCodec.codecForName("EUC-KR"))
            self.source = unicode(source, 'euc-kr')
        else:
            self.source = unicode(source)

    def save(self, path):
        if not self.source:
            raise ValueError("Execute the mehod source to get source")
        fd = open(path, 'w')
        if self.charset:
            fd.write(self.source.encode(self.charset))
        else:
            fd.write(self.source)
        fd.close()


    def app_exec(self):
        self.timer.start(self.limit_time_for_javascript)
        QObject.connect(self.timer, SIGNAL('timeout()'), self._javascript_timeout_handler)
        self.app.exec_()

    def app_exit(self):
        self.timer.stop()
        self.app.exit()


    def _javascript_timeout_handler(self):
        print "javascript has a problem"
        self.app_exit()
        
    def evaluateJavaScript(self, script):
        current_frame = self.web_page.currentFrame()
        current_frame.evaluateJavaScript(self.jquery)
        result = current_frame.evaluateJavaScript(script)

        return result
            

    def _load_finished(self, ok):
        current_frame = self.web_page.currentFrame()
        current_frame.evaluateJavaScript(self.jquery)
        if self.load_function:
            self.load_function(*self.load_function_args,
                                **self.load_function_kwargs)


    def set_load_function(self, load_function, *args, **kwargs):
        self.load_function = load_function
        self.load_function_args = args
        self.load_function_kwargs = kwargs


class NotifierBase(WebkitInterface):

    results = []
    maximumN = 5                # 5 means Mx5 matrix
    parsers = {}                # 'key : javascript' javascript for parsing
    parser_dic = {}
    login_script = None
    url = None


    def __call__(self, url=None):
        # TODO: create the return message
        self.detectParsers()
        if not self.parsers:
            libs.outputError("We must need parser. See doc.")

        self._setUrl(url)
        self.loadWithLogin(self.url)

        # if self.condition():
        #     self.action()

    def _setUrl(self, url):
        if url:
            self.url = url
        else:
            if not self.url:
                print "We need url."

    def loadWithLogin(self, url):
        self.setLoginScript()
        if self.login_script:
            self.load(url, load_function=self.__loadLogin)
        else:
            self.load(url, load_function=self.__loadParsing)

    def __loadLogin(self):
        """
        Let's login.

        It is used as load_function
        """
        self.set_load_function(self.__loadParsing)
        self.evaluateJavaScript(self.login())

    # Lastest loaded
    def __loadParsing(self):
        """
        Our purpose is parsing. The result is to be stored in
        self.results.
        
        It is used as load_function.
        """
        self.set_load_function(None)
        for key in self.parsers:
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print key
            script = self.parsers[key]
            result = self.evaluateJavaScript(script)
            self.results.append(result)
        self.app_exit()

    def setLoginScript(self):
        "Detect self.login method."
        self.login_script = self.login()
        
    def detectParsers(self):
        """
        Detect the functions of parserN. And self.parsers is the list of
        paser function.
        """
        # Our purpose is to build a dictionary self.parsers.
        if self.parser_dic:
            self._detectParsers_fromDictionary()
        else:
            self._detectParsers_fromFunctions()
            

    def _detectParsers_fromFunctions(self):
        for i in range(1, self.maximumN):
            i = str(i)
            try:
                func = getattr(self, 'parser' + i)
                self.parsers[func.__name__] = func()
                #self.parsers.append(func)
            except AttributeError:
                return

    def _detectParsers_fromDictionary(self):
        for key in self.parser_dic:
            script = self._create_script(self.parser_dic[key])
            self.parsers[key] = script
            print script



    def setParsersFrom(self, parsers):
        self.parser_dic = parsers

    def _create_script(self, selector):
        script = \
            r"""
            var titles = "";
            $("%s").each(function(i) {
                titles += $(this).text() + "\n";
            });
            titles;
            """ % selector
        return script



    def condition(self):
        pass

    def action(self):
        pass

    def login(self):
        pass


# class NotifierTestBase(NotifierBase):

#     def setParser(self, parsers):
#         pass
        

#     def testSelector(self, selector, url=None):
#         if not url:
#             url = self.url
        
#     def _test_load_function(self, selector):
#         script = \
#             r"""
#             var titles = "";
#             $("%s").each(function(i) {
#                 titles += $(this).text() + "\n";
#             });
#             titles;
#             """ % selector
#         self.evaluateJavaScript(script)



# class NotifierType1(NotifierBase):

#     def setParsersFrom(self, parsers):
#         for key in parsers:
#             self.parsers[key] = self._create_script(parsers[key])

#     def _create_script(self, selector):
#         script = \
#             r"""
#             var titles = "";
#             $("%s").each(function(i) {
#                 titles += $(this).text() + "\n";
#             });
#             titles;
#             """ % selector
#         return script


class Test(ListOfMethods):

    url = 'http://www.toshare.kr/?mid=board_etc'


    def __repr__(self):
        test_functions = self.list_of_methods('test')
        print test_functions

        for func in test_functions:
            func()
        

    class Toshare(NotifierBase):

        def parser1(self):
            return \
                r"""
                var titles = "";
                $("td[class=num]").each(function(i) {
                    titles += $(this).text() + "\n";
                });
                titles;
                """

        def login(self):
            return \
                r"""
                $("input[name=user_id]").val("cimationp");
                $("input[title=password]").val("uutss123");
                $("input[alt=login]").click();
                """

    def test_basic(self):
        
        # obj = Toshare()
        # obj(self.url)
        pass

def main():
    if len(sys.argv) > 4 :
        sys.stdout.write("ArgumentError")
        return
    url = sys.argv[1]
    charset = sys.argv[2]
    if charset == "None":
        charset = None
    path = sys.argv[3]

    aa = WebkitInterface()
    aa.charset = charset
    aa.getSource(url)
    aa.save(path)
    del aa

if __name__ == "__main__":
    main()
