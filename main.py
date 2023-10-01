from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(1)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.showMaximized()

        navtb = QToolBar('Navigation')
        self.addToolBar(navtb)





        # Create a menu for bookmarks
        bookmark_menu = QMenu('Bookmarks', self)
        self.menuBar().addMenu(bookmark_menu)

        # Add a 'Add Bookmark' action to the bookmarks menu
        add_bookmark_action = QAction('Add Bookmark', self)
        add_bookmark_action.triggered.connect(self.addBookmark)
        bookmark_menu.addAction(add_bookmark_action)

        #bookmark buttton
        bookmarkbtn = QAction(QIcon('images/bookmark.png'), 'bookmark', self)
        bookmarkbtn.setStatusTip("bokmk")
        bookmarkbtn.triggered.connect(self.addBookmark)
        navtb.addAction(bookmarkbtn)











        # back button
        backbtn = QAction(QIcon('images/back.png'), 'back', self)
        backbtn.setStatusTip("Back to previous page")
        backbtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(backbtn)

        # forward btn
        forbtn = QAction(QIcon('images/for.png'), 'forward', self)
        forbtn.setStatusTip("forward to next page")
        forbtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forbtn)

        reload_btn = QAction(QIcon('images/reload.png'), 'reload', self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        #home_btn = QAction(QIcon('home.png'), 'home', self)
        #home_btn.setStatusTip("Go home")
        #home_btn.triggered.connect(self.navigate_home)
        #navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlBar)

        # stop btn
        stopbtn = QAction(QIcon('images/codd.png'), 'stop', self)
        stopbtn.setStatusTip("stop the loading")
        stopbtn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stopbtn)

        self.add_new_tab(QUrl('http://www.google.com'), 'homepage')
        self.show()
        self.setWindowTitle('Flashy Browser')
        #self.setWindowIcon(QIcon('logo.png'))

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):

        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - Browser" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlBar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)







    def addBookmark(self):
        # Create a dialog to get the URL and name of the new bookmark
        url, ok = QInputDialog.getText(self, 'Add Bookmark', 'URL:')
        if ok:
            name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Name:')
            if ok:
                # Add the bookmark to the bookmarks menu
                bookmark_action = QAction(name, self)
                bookmark_action.setData(QUrl(url))
                bookmark_action.triggered.connect(self.loadBookmark)
                self.menuBar().actions()[0].menu().addAction(bookmark_action)

    def loadBookmark(self):
        # Get the URL of the selected bookmark and load it in the WebEngineView
        bookmark_action = self.sender()
        url = bookmark_action.data()
        self.add_new_tab(QUrl(url))

















app = QApplication(sys.argv)
app.setApplicationName("flashy browser")
window = MainWindow()
app.exec_()

