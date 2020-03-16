import random

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QGraphicsItem, QGraphicsEllipseItem, QGraphicsProxyWidget
from PyQt5.QtGui import QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, QPointF


class Circle(QGraphicsEllipseItem):
    radius = 50

    def __init__(self, x_coordinate, y_coordinate, parent=None):
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

    def getLines(self):
        """All lines connected to circle
        :return: list of lines
        """
        return self.connectedCircle.values()

    def addConnection(self, circle, line):
        """Add connection with circle
        :return:
        """
        self.connectedCircle[circle] = line

    def removeConnection(self, circle):
        """Remove connection with circle
        :return:
        """
        del self.connectedCircle[circle]

    def getCenter(self):
        """This function is used to calculate current center of circle
        :return: center of circle
        """
        return QPointF(self.sceneBoundingRect().x() + self.sceneBoundingRect().width() / 2.0,
                       self.sceneBoundingRect().y() + self.sceneBoundingRect().height() / 2.0)

    def addOnCanvas(self, scene):
        """This function is used to add circle on canvas with creating label
        :return:
        """
        scene.addItem(self)
        scene.addItem(self.textLabelProxy)
        self.textLabelProxy.setGeometry(QRectF(self.rect().x() + self.rect().width() / 4,
                                               self.rect().y() - self.pen().width() - 22,
                                               60, 22))

    def removeFromCanvas(self):
        """This function is used to remove circle from canvas
        :return:
        """
        for circle, line in self.connectedCircle.items():
            self.scene().removeItem(line)
            circle.removeConnection(self)

        self.scene().removeItem(self)
