import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QLineEdit, QGraphicsView, \
    QMenu, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenu, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor, QCursor, QBrush, QIcon, QTransform
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QPointF

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Circle(QGraphicsEllipseItem):
    def __init__(self, radius, parent=None):
        position = QtCore.QPoint(*random.choices(range(800), k=2))
        x_coordinate, y_coordinate = position.x(), position.y()
        QGraphicsEllipseItem.__init__(self, QRectF(x_coordinate, y_coordinate, 2 * radius, 2 * radius), parent=parent)
        # self.scene.moveCircle.connect(self.mouseMoveEvent)
        self.line = None
        self.color = QColor(*random.choices(range(256), k=3))
        self.setPen(QPen(self.color, 4, Qt.SolidLine))

        self.connecting_lines = []
        self.setFlags(QGraphicsItem.ItemIsMovable)

    def connect(self):
        pass

    def contextMenuEvent(self, event):
        contextMenu = QMenu()
        deleteAction = contextMenu.addAction("Delete")
        quitAction = contextMenu.addAction("Exit")
        connectAction = contextMenu.addAction("Connect With")
        action = contextMenu.exec_(event.screenPos())
        if action == deleteAction:
            self.scene().removeItem(self)
        if action == quitAction:
            self.window().close()
        if action == connectAction:
            self.connect()

    def add_connecting_line(self):
        pass

    def add_line(self, circle):
        pass

    # def addLine(self, line, isPoint1):
    #     self.line = line
    #     self.isP1 = isPoint1

    # def move_toward_circle(self):
    #     x = self.x()
    #     y = self.y()
    #     newCenterPos = QPointF(x, y)
    #     p1 = newCenterPos if self.isP1 else self.line.line().p1()
    #     p2 = self.line.line().p2() if self.isP1 else newCenterPos
    #     self.line.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def draw_on_canvas(self, scene):
        scene.addItem(self)
        textLabel = scene.addWidget(QLineEdit('cirA'))
        textLabel.setParentItem(self)
        textLabel.setGeometry(
            QRectF(self.rect().x() + self.rect().width() / 4, self.rect().y() - self.pen().width() - 10, 50, 10))

    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return
        print(CanvasScene.myMode, CanvasScene.InsertLine, CanvasScene.MoveItem)
        if CanvasScene.myMode == CanvasScene.InsertLine:
            item = self.scene().itemAt(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), self.transform())
            print(item)
            if item :
                self.line = QGraphicsLineItem(QLineF(item.boundingRect().x()+item.boundingRect().width()/2,
                                                     item.boundingRect().y()+item.boundingRect().height()/2,
                                              mouseEvent.scenePos().x(), mouseEvent.scenePos().y()))


                self.line.setPen(QPen(Qt.black, 2))
                self.scene().addItem(self.line)
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.connecting_lines:
            self.move_toward_circle()
        if CanvasScene.myMode == CanvasScene.InsertLine and self.line:
            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        if CanvasScene.myMode == CanvasScene.MoveItem:
            print(self.rect())
            super().mouseMoveEvent(mouseEvent)
            self.update()
            print(self.rect())
            print(self.scene().sceneRect())

    def mouseReleaseEvent(self, mouseEvent):
        if CanvasScene.myMode == CanvasScene.InsertLine and self.line:
            item = self.scene().itemAt(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), self.transform())

        # self.removeItem(self.line)
        self.line = None
        super(Circle, self).mouseReleaseEvent(mouseEvent)


class CanvasScene(QGraphicsScene):
    MoveItem, InsertLine = 1, 2
    myMode = MoveItem

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

    def setMode(self, mode):
        CanvasScene.myMode = mode
        print(mode)

    # def mousePressEvent(self, mouseEvent):
    #     if (mouseEvent.button() != Qt.LeftButton):
    #         return
    #     if self.myMode == self.InsertLine:
    #         self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(),
    #                                              mouseEvent.scenePos()))
    #         self.line.setPen(QPen(self.myLineColor, 2))
    #         self.addItem(self.line)
    #     super().mousePressEvent(mouseEvent)

    # def mouseMoveEvent(self, mouseEvent):
    # if self.myMode == self.InsertLine and self.line:
    #     newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
    #     self.line.setLine(newLine)
    # if self.myMode == self.MoveItem:
    #     if self.itemAt(mouseEvent.scenePos, QTransform()):
    #         pass
    # self.itemAt(mouseEvent.scenePos, QTransform())
    # super(Circle, self.itemAt(mouseEvent.scenePos, QTransform())).mouseMoveEvent(mouseEvent)
    # self.moveCircle.emit(mouseEvent)

    # def mouseReleaseEvent(self, mouseEvent):
    #     #     if self.line and self.myMode == self.InsertLine:
    #     #         startItems = self.items(self.line.line().p1())
    #     #         if len(startItems) and startItems[0] == self.line:
    #     #             startItems.pop(0)
    #     #         endItems = self.items(self.line.line().p2())
    #     #         if len(endItems) and endItems[0] == self.line:
    #     #             endItems.pop(0)
    #
    #     # self.removeItem(self.line)
    #     self.line = None
    #     self.myMode = CanvasScene.MoveItem


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # self.top = 100
        # self.left = 900
        # self.width = 1000
        # self.height = 800
        self.title = "Create Circles"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.scene = CanvasScene()
        self.scene.setSceneRect(QRectF(0, 0, 1000, 1000))
        self.createActions()
        self.createToolbars()

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.connectionTypeGroup.checkedId())

    def createActions(self):
        self.adAction = QAction("Add", self, shortcut="Ctrl+N", statusTip="Add a new Circle")
        self.adAction.triggered.connect(lambda: self.drawCircle())
        self.generateReportAction = QAction("Generate Report", self, shortcut="Ctrl+G", statusTip="Pdf Report")
        self.saveAction = QAction(
            QIcon('images/bringtofront.png'), "Save",
            self, shortcut="Ctrl+S", statusTip="Save as Image")

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.adAction)
        self.editToolBar.addAction(self.generateReportAction)
        self.editToolBar.addAction(self.saveAction)

        pointerButton = QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QIcon('images/pointer.png'))
        linePointerButton = QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QIcon('images/linepointer.png'))

        self.connectionTypeGroup = QButtonGroup()
        self.connectionTypeGroup.addButton(pointerButton, CanvasScene.MoveItem)
        self.connectionTypeGroup.addButton(linePointerButton, CanvasScene.InsertLine)
        self.connectionTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        self.lineToolbar = self.addToolBar("Pointer type")
        self.lineToolbar.addWidget(linePointerButton)
        self.lineToolbar.addWidget(pointerButton)

    def drawCircle(self):
        radius = 50
        circle = Circle(radius)
        circle.draw_on_canvas(self.scene)

    def save_image(self):
        fileName = QFileDialog.getSaveFileName(self, 'caption', "image.png", '*.png')
        pixmap = QPixmap()
        pixmap = self.graphicView.grab(self.rect())
        pixmap.save(fileName[0], 'PNG')


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
