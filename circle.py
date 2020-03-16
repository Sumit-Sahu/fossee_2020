import random

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QGraphicsItem, QGraphicsEllipseItem, QGraphicsProxyWidget
from PyQt5.QtGui import QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, QPointF


class Circle(QGraphicsEllipseItem):
    radius = 50

    def __init__(self, parent=None):
        position = QtCore.QPoint(*random.choices(range(800), k=2))
        x_coordinate, y_coordinate = position.x(), position.y()
        QGraphicsEllipseItem.__init__(self, QRectF(x_coordinate, y_coordinate, 2 * Circle.radius, 2 * Circle.radius),
                                      parent=parent)
        self.setZValue(1)
        self.color = QColor(*random.choices(range(256), k=3))
        self.setPen(QPen(self.color, 4, Qt.SolidLine))
        self.textLabel = QLineEdit('cirA')
        self.textLabelProxy = QGraphicsProxyWidget()
        self.textLabelProxy.setWidget(self.textLabel)
        self.textLabelProxy.setParentItem(self)
        self.textLabel.setStyleSheet("border: 1px solid blue; color:blue;"
                                     " selection-color:yellow; selection-background-color:green;")
        self.textLabel.setFont(QFont('Times New Roman', 12))
        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable)
        self.connectedCircle = {}

    def setMode(self, mode):
        Circle.myMode = mode

    def getLines(self):
        return self.connectedCircle.values()

    def addConnection(self, circle, line):
        self.connectedCircle[circle] = line

    def removeConnection(self, circle):
        del self.connectedCircle[circle]

    def getCenter(self):
        return QPointF(self.sceneBoundingRect().x() + self.sceneBoundingRect().width() / 2.0,
                       self.sceneBoundingRect().y() + self.sceneBoundingRect().height() / 2.0)

    def addOnCanvas(self, scene):
        scene.addItem(self)
        scene.addItem(self.textLabelProxy)
        self.textLabelProxy.setGeometry(QRectF(self.rect().x() + self.rect().width() / 4,
                                               self.rect().y() - self.pen().width() - 22,
                                               60, 22))

    def removeFromCanvas(self):
        for circle, line in self.connectedCircle.items():
            self.scene().removeItem(line)
            circle.removeConnection(self)

        self.scene().removeItem(self)
