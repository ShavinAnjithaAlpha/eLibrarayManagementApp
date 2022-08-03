import sys, os

from PyQt5.QtWidgets import (QApplication ,QWidget, QStackedLayout ,QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QDesktopWidget)
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor , QFont

from style_sheets.main_style_sheet import style_sheet
from file_manager.db_manager import DBManager

from widgets.main_content_page import MainContentPage

class eLibrarySystem(QWidget):
    def __init__(self):
        super(eLibrarySystem, self).__init__()
        desktop = QDesktopWidget() # create the desktop instance
        self.setMinimumSize(desktop.screenGeometry().width() , desktop.screenGeometry().height())
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("e Library System v0.01")
        # setup the data bases
        if not os.path.exists("db"):
            DBManager.buildDatabase()
        # setup the content to of the main window
        self.setUpConetnt()
        # show the window
        self.show()


    def setUpConetnt(self):

        # create the stack layout for pack the main content and side bar for another task
        self.mainStackLyt = QStackedLayout()

        # create the content page
        self.main_content_page = MainContentPage("Physics")
        self.mainStackLyt.addWidget(self.main_content_page)
        # create the widget for side bar and setup task
        sideBar = self.setUpSideBar()

        # create the hbox
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        hbox.addWidget(sideBar)
        hbox.addLayout(self.mainStackLyt)
        self.setLayout(hbox)

        self.setObjectName("main")
        self.setStyleSheet(style_sheet)

    def setUpSideBar(self):

        # create the side bar
        self.sideBar = QWidget()
        self.sideBar.setObjectName("side_bar")
        self.sideBar.setContentsMargins(0, 0, 0, 0)
        self.sideBar.setMaximumWidth(300)

        # create the side button
        sideButton = QPushButton("=")
        sideButton.setObjectName("side_button")
        sideButton.setFixedSize(QSize(70, 50))
        sideButton.pressed.connect(lambda b = sideButton : self.animatedSideBar(b))

        hbox = QHBoxLayout()
        hbox.addWidget(sideButton)
        hbox.addStretch()

        # pack the side bar button
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)
        # vbox.addWidget(sideButton, alignment=Qt.AlignLeft)
        vbox.addStretch()

        self.sideBar.setLayout(vbox)
        return self.sideBar

    def animatedSideBar(self, button : QPushButton):

        # create the animation for this
        self.animation = QPropertyAnimation(self.sideBar , b'maximumWidth')
        self.animation.setStartValue(self.sideBar.width())
        self.animation.setEasingCurve(QEasingCurve.InCubic)

        if (self.sideBar.width() >= 300):
            self.animation.setEndValue(button.width())
        else:
            self.animation.setEndValue(300)

        self.animation.setCurrentTime(1000)
        self.animation.start()

    def addTaskToSideBar(self):

        pass



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = eLibrarySystem()
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
