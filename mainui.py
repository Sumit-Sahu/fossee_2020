
import sys, random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QLineEdit
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 900
        self.width = 1000
        self.height = 800
        self.title = "Create Circles"
        self.InitWindow()

        # self.label = QLabel()
        # canvas = QPixmap(1000, 800)
        # canvas.fill()
        # self.label.setPixmap(canvas)
        # self.setCentralWidget(self.label)
        # self.circle = None
        # self.statusBar()
        self.circles = []
        self.show()

    def CreateMenu(self):
        mainMenu = self.menuBar()

        self.adAction =QAction('Add' ,self)
        mainMenu.addAction(self.adAction)
        self.adAction.triggered.connect(lambda: self.drawCircle())

        generate_reportAction =QAction('Generate Report' ,self)
        mainMenu.addAction(generate_reportAction)

        saveAction = QAction('Save', self)
        mainMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save_image)

    def drawCircle(self):
        position = QtCore.QPoint(*random.choices(range(800), k=2))
        b = Circle(self)
        b.show()
        b.move(position)

    def save_image(self):
        fileName = QFileDialog.getSaveFileName(self, 'some text', "image.png", '*.png')
        pixmap = self.label.pixmap()
        pixmap.save(fileName[0], "PNG")


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.CreateMenu()






class Circle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        # self.setGeometry(30, 30, 600, 400)
        self.setGeometry(QRect(0,0,200,200))
        self.name = QLineEdit('cirA', self)
        self.color = QColor(*random.choices(range(256), k=3))
        # self.position = QtCore.QPoint(*random.choices(range(800), k=2))
        self.position=QPoint(4,30)
        self.length = 100
        self.name=QLineEdit('cirA',self)

    def paintEvent(self, event):
            painter = QPainter(self)
            # print("called")
            painter.setPen(QPen(self.color, 4, Qt.SolidLine))
            x, y = self.position.x(), self.position.y()
            painter.drawEllipse(x, y, self.length, self.length)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())