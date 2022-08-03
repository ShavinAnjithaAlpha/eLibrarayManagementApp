import os.path
import sys

from PyQt5.QtWidgets import (QApplication ,QWidget, QStackedLayout ,QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QDesktopWidget, QScrollArea, QLineEdit, QFileDialog, QInputDialog)
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor , QFont

from style_sheets.content_style_sheet import style_sheet

from util.collection import Collection
from util.book import Book
from widgets.collection_widget import CollectionWidget
from widgets.book_wigdet import BookWidget
from file_manager.db_manager import DBManager

class MainContentPage(QWidget):

    vertical_space = 50
    horizontal_space = 50

    def __init__(self, title = "", index = ""):
        super(MainContentPage, self).__init__()
        # widget positions variables
        self.x = 150
        self.y = 200
        self.i = 0
        self.index = index

        self.books = []
        self.collections = []

        self.title = title
        # setup the page
        self.setObjectName("content_page")
        self.setContentsMargins(0, 0, 0, 0)

        # create the main widget of content
        self.content_widget = QWidget()
        self.content_widget.setObjectName("main_content_page")
        self.content_widget.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.content_widget)

        # create the main vbox
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addLayout(self.createTop())
        vbox.addWidget(self.scroll_area)
        self.setLayout(vbox)

        self.setUpConetent()
        self.setStyleSheet(style_sheet)

    def createTop(self):

        # create the back button
        back_button = QPushButton("<-")
        back_button.setObjectName("back_button")
        back_button.setMaximumWidth(150)
        back_button.setMinimumHeight(100)

        # create the main title label
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("title_label")
        self.title_label.setMinimumHeight(100)

        # create the h box for pack this
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(back_button)
        hbox.addWidget(self.title_label)

        return hbox

    def setUpConetent(self):

        # create the add buttons
        add_collection_button = QPushButton("Add Collection", self.content_widget)
        add_collection_button.setObjectName("add_collection_button")
        add_collection_button.pressed.connect(self.getCollectionData)
        add_collection_button.move(10, 10)

        add_book_button = QPushButton("Add Books", self.content_widget)
        add_book_button.setObjectName("add_book_button")
        add_book_button.move(180, 10)
        add_book_button.pressed.connect(self.addBooks)

        # create the search bar
        self.search_bar = QLineEdit(self.content_widget)
        self.search_bar.setPlaceholderText("<i>search anything...</i>")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.resize(900, 60)

        searchBar_x = (1700 - self.search_bar.width()) // 2
        self.search_bar.move(searchBar_x, 100)

        # load the collections and books
        self.loadCollections()
        self.loadBooks()

    def loadCollections(self):

        # get the collection list first
        colls = DBManager.getCollections(self.index)
        for coll in colls:
            widget = CollectionWidget(self.content_widget, coll)
            widget.collectionOpenSignal.connect(self.openCollection)
            self.collections.append(widget)
            # move to the right places
            widget.move(self.x , self.y)
            self.i += 1
            # update the x and y
            if (self.i%5 == 0):
                self.i = 0
                self.x = 150
                self.y += (widget.height + widget.max_text_height + self.vertical_space)
            else:
                self.x += (widget.width + self.horizontal_space)

    def loadBooks(self):

        books = DBManager.getBooks(self.index)
        for book in books:
            widget = BookWidget(self.content_widget, book)
            self.books.append(widget)
            # move to the right places
            widget.move(self.x, self.y)
            self.i += 1
            # update the x and y
            if (self.i % 5 == 0):
                self.i = 0
                self.x = 150
                self.y += (widget.height + widget.text_max_height + self.vertical_space)
            else:
                self.x += (widget.width + self.horizontal_space)

    def addBook(self, book : str , tags = []):

        # update the data base
        id = DBManager.addBook(book , self.index , False , tags)
        # create the book widget
        widget = BookWidget(self.content_widget, Book(self.getBookName(book), self.index, book, False, id))
        self.books.append(widget)
        widget.move(self.x , self.y)

        self.i += 1
        # update the x and y
        if (self.i % 5 == 0):
            self.i = 0
            self.x = 150
            self.y += (widget.text_max_height + widget.height + self.vertical_space)
        else:
            self.x += (widget.width + self.horizontal_space)

    def addCollection(self, name , image , tags = []):

            DBManager.addCollection(name, self.index , image, False , tags)
            # create the widget and add to the content
            widget = CollectionWidget(self.content_widget, Collection(name, image, self.index))
            widget.collectionOpenSignal.connect(self.openCollectcion)
            self.collections.append(widget)
            widget.move(self.x, self.y)

            self.i += 1
            # update the x and y
            if (self.i % 5 == 0):
                self.i = 0
                self.x = 150
                self.y += (widget.max_text_height + widget.height + self.vertical_space)
            else:
                self.x +=( widget.width + self.horizontal_space)


    def setTitle(self, title):
        self.title = title
        self.title_label.setText(title)

    def addBooks(self):

        files, ok = QFileDialog.getOpenFileNameileNames(self, "open books", "", "PDF Files (*.pdf)")
        if ok:
            for book in files:
                self.addBook(book)


    def getCollectionData(self):

        text , ok = QInputDialog.getText(self, "collection name", "Enter the Collection Name : ")
        if ok:
            image, ok = QFileDialog.getOpenFileName(self, "Collection Cover Image", "D:/Gallery", "PNG FILE(*.png);;JPEG FILE(*.jpg)")
            if ok:
                self.addCollection(text, image)

    def getBookName(self, path : str):

        # print(os.path.splitext(os.path.split(path)[1])[0])
        return os.path.split(path)[1]

    def clearPage(self):

        for widget in [*self.collections, *self.books]:
            widget.deleteLater()
        # clear the lists
        self.collections.clear()
        self.books.clear()

        self.content_widget.deleteLater()
        # create the main widget of content
        self.content_widget = QWidget()
        self.content_widget.setObjectName("main_content_page")
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.content_widget)


    def openCollection(self, collection : Collection):

        # reset the coordinates
        self.x = 150
        self.y = 200
        self.i = 0
        # open the new page
        self.clearPage()
        # set the new current index
        self.index = collection.index

        self.setUpConetent()
