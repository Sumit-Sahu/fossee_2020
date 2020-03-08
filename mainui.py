import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QLineEdit, QGraphicsView,\
    QMenu,QGraphicsScene, QGraphicsView, QGraphicsItem,QMenu
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor, QCursor, QBrush
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)

    def contextMenuEvent(self, event):
        scene=window.scene
        list = scene.selectedItems()
        contextMenu = QMenu()
        deleteAction = contextMenu.addAction("Delete")
        exitAction = contextMenu.addAction("Exit")
        action = contextMenu.exec_(event.globalPos())
        if action == deleteAction:
            for item in list:
                scene.removeItem(item)
        if action == exitAction:
            window.close()

    def wheelEvent(self, event):
        factor = 1.25 ** (-event.angleDelta().y()/ 240.0)
        self.scale(factor, factor)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 100
        self.left = 900
        self.width = 1000
        self.height = 800
        self.title = "Create Circles"
        self.InitWindow()

        self.graphicView = GraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 25, 1000, 800)


        self.graphicView.setScene(self.scene)
        self.graphicView.setGeometry(0, 25, 1000, 825)


    def CreateMenu(self):
        mainMenu = self.menuBar()

        self.adAction =QAction('Add' ,self)
        mainMenu.addAction(self.adAction)
        self.adAction.triggered.connect(lambda: self.drawCircle())

        generate_reportAction =QAction('Generate Report' ,self)
        mainMenu.addAction(generate_reportAction)

        saveAction = QAction('Save', self)
        mainMenu.addAction(saveAction)
        # saveAction.triggered.connect(self.save_image)

    def drawCircle(self):
        circle=Circle(self)
        circle.drawCircle(self.scene)


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.CreateMenu()

    # def mousePressEvent(self, QMouseEvent):
    #     # if QMouseEvent.button() == Qt.RightButton:
    #     print("clicked right")




class Circle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, light, *args, **kwargs):
        super(Circle, self).__init__(*args, **kwargs)

        self.color = QColor(*random.choices(range(256), k=3))
        self.position = QtCore.QPoint(*random.choices(range(800), k=2))
        self.pen = QPen(self.color, 4, Qt.SolidLine)
        self.length = 100

    def drawCircle(self,scene):
        x, y = self.position.x(), self.position.y()
        ellipse = scene.addEllipse(x, y, 100, 100, self.pen, QBrush())
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
        ellipse.acceptHoverEvents()

        # ellipse.acceptedMouseButtons()
        textLabel = scene.addWidget(QLineEdit('cirA'))
        textLabel.setGeometry(QRectF(x + 20, y - 25, 50, 10))
        textLabel.setParentItem(ellipse)






if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())