

import sys, random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 900
        self.width = 1000
        self.height = 800
        self.title = "Create Circles"
        self.InitWindow()
        
        self.label = QLabel()
        canvas = QPixmap(1000, 800)
        canvas.fill()
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.circle = None
        # self.statusBar()
        self.circles = []
        self.show()

    def CreateMenu(self):
        mainMenu = self.menuBar()

        self.adAction=QAction('Add',self)
        mainMenu.addAction(self.adAction)
        self.adAction.triggered.connect(lambda: self.drawCircle())

        generate_reportAction=QAction('Generate Report',self)
        mainMenu.addAction(generate_reportAction)

        saveAction = QAction('Save', self)
        mainMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save_image)

    def paintEvent(self, event):
        if self.circle is not None:
            painter = QPainter(self.label.pixmap())
            painter.begin(self)
            # print("called")
            # self.circle.paint(painter)
            painter.setPen(QPen(self.circle.color, 4, Qt.SolidLine))
            x, y = self.circle.position.x(), self.circle.position.y()
            painter.drawEllipse(x, y, self.circle.length, self.circle.length)
            painter.end()
            self.circle = None

    def drawCircle(self):
        self.circle = Circle()
        self.update()
    
    def save_image(self):
        fileName = QFileDialog.getSaveFileName(self, 'some text', "image.png", '*.png')
        pixmap = self.label.pixmap()
        pixmap.save(fileName[0], "PNG")

    
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.CreateMenu()






class Circle():
    def __init__(self):
        self.color = QtGui.QColor(*random.choices(range(256), k=3))
        self.position = QtCore.QPoint(*random.choices(range(800), k=2))
        self.length = random.randrange(200)
        self.textlable=QLabel()

    # def paint(self, painter):
    #     painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
    #     x, y = self.position.x(), self.position.y()
    #     painter.drawEllipse(x, y, self.length, self.length)
        # print("should execute")



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())