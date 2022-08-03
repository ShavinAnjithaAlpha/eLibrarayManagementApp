from PyQt5.QtWidgets import (QApplication, QWidget ,QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor , QFont, QPixmap, QMouseEvent

from util.collection import Collection
from style_sheets.collection_style_sheet import style_sheet

class CollectionWidget(QWidget):

    width = 200
    height = 250
    max_text_height = 70

    collectionOpenSignal = pyqtSignal(Collection)

    def __init__(self, parent, collection : Collection):
        super(CollectionWidget, self).__init__(parent)
        self.collection = collection

        # create the image and text label
        name_label = QLabel(self.collection.name)
        name_label.setWordWrap(True)
        name_label.setMaximumSize(QSize(self.width , self.max_text_height))
        name_label.setObjectName("name_label")

        image_label = QLabel()
        image_label.setObjectName("image_label")
        image_label.setFixedSize(QSize(self.width, self.height))
        image_label.setPixmap(QPixmap(self.collection.image).scaled(image_label.size() ,
                                        Qt.KeepAspectRatioByExpanding , Qt.FastTransformation))

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(image_label)
        vbox.addWidget(name_label)

        base = QWidget()
        base.setObjectName("base")
        base.setLayout(vbox)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(base)
        self.setStyleSheet(style_sheet)

    def mouseDoubleClickEvent(self, event : QMouseEvent):

        self.collectionOpenSignal.emit(self.collection)

    def __str__(self):
        return self.collection.name


if __name__ == "__main__":
    app = QApplication([])
    window = CollectionWidget(None , Collection("physics", "", 5))
    window.show()

    app.exec_()