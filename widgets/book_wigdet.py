import fitz, os

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QMouseEvent

from util.book import  Book

class BookWidget(QWidget):

    width = 200
    height = 250
    text_max_height = 80

    def __init__(self, parent, book : Book):
        super(BookWidget, self).__init__(parent)
        self.book = book
        self.setUpContent()

    def setUpContent(self):

        # create the book cover image label
        self.coverImageLabel = QLabel()
        self.coverImageLabel.setObjectName("image_label")
        self.coverImageLabel.setFixedSize(QSize(self.width, self.height))
        # lod the cover image
        self.loadCover()

        # create the book name label
        name = self.book.name
        if len(name) > 50:
            name = (name[:47] + "...")
        self.nameLabel = QLabel(name)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setObjectName("name_label")
        self.nameLabel.setMaximumSize(QSize(self.width, self.text_max_height))

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.coverImageLabel)
        vbox.addWidget(self.nameLabel)

        base = QWidget()
        base.setObjectName("base")
        base.setLayout(vbox)

        vbox2 = QVBoxLayout()
        vbox2.setContentsMargins(0, 0, 0, 0)
        vbox2.addWidget(base)
        self.setLayout(vbox2)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""

                            QLabel#name_label {font-size : 20px;
                                                padding : 5px;
                                                color : orange;
                                                border-bottom-left-radius : 5px;
                                                border-bottom-right-radius : 5px;}
                                                
                                                
                            QLabel#name_label:hover {background-color : rgba(250, 70, 10, 0.8);
                                                    color : black;}
                            
                            QLabel#image_label:hover {
                                        border-top : 2px solid red;}
                            """)

    def loadCover(self):

        self.image_dir = f"thumbs/{self.book.id}.png"
        if not os.path.exists(self.image_dir):
            try:
                # load the document
                doc = fitz.Document(self.book.path)
                page1 = doc.load_page(0)

                pic = page1.get_pixmap()


                pic.save(self.image_dir)
                # close the document
                doc.close()

                self.coverImageLabel.setPixmap(
                    QPixmap(self.image_dir).scaled(self.coverImageLabel.size(),
                                                   Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))
            except:
                pass
        else:
            self.coverImageLabel.setPixmap(
                QPixmap(self.image_dir).scaled(self.coverImageLabel.size(),
                                               Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))


    def mouseDoubleClickEvent(self, event : QMouseEvent) -> None:

        # open the book pdf use the adobe reader
        os.startfile(self.book.path)

    def __str__(self):

        return self.book.name