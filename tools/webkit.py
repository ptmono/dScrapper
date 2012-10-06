#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

def webkitjs(url):
    "Test webkit with javascript"
    app = QApplication(sys.argv)
    web = QWebView()
    
    #web.settings().globalSettings()
    web.settings().setAttribute(QWebSettings.PluginsEnabled,True)
    web.settings().setDefaultTextEncoding(QString("euc-kr"))

    page = web.page()
    page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

    def linkClicked(url):
        web.load(QUrl(url))
    web.connect(web, SIGNAL("linkClicked (const QUrl&)"), linkClicked)
    
    tab = QGridLayout()
    tab.setSpacing(3)
    tab.addWidget(web, 1, 0, 1, 1)

    win = QWidget()
    size = QSize(800, 1200)
    win.resize(size)
    win.setLayout(tab)
    win.setWindowTitle('test')

    web.load(QUrl(url))

    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except:
        url = ''
    webkitjs(url)
