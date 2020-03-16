from PyQt5.QtGui import QFont, QPen
from PyQt5.QtWidgets import QGraphicsLineItem, QLineEdit, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QPointF, QRectF


class ConnectingLine(QGraphicsLineItem):

    def __init__(self, startPoint, endPoint, parent=None):
        QGraphicsLineItem.__init__(self, startPoint.x(), startPoint.y(), endPoint.x(), endPoint.y(), parent=parent)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.startCircle = None
        self.endCircle = None
        self.textLabel = QLineEdit('CON1')
        self.textLabelProxy = QGraphicsProxyWidget()
        self.textLabelProxy.setWidget(self.textLabel)
        self.textLabelProxy.setParentItem(self)
        self.textLabel.setStyleSheet(
            "border: 1px solid black; color:black; selection-color:yellow; selection-background-color:green;")
        self.textLabel.setFont(QFont('Times New Roman', 12))

        self.setPen(QPen(Qt.black, 4, Qt.SolidLine))

    def setStartCircle(self, startCircle):
        self.startCircle = startCircle

    def setEndCircle(self, endCircle):
        self.endCircle = endCircle

    def getStartCircle(self):
        return self.startCircle

    def getEndCircle(self):
        return self.endCircle

    def updateLine(self, point):
        if self.startCircle and self.endCircle:
            item = self.startCircle
            self.startPoint = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                      item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
            item = self.endCircle
            self.endPoint = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                    item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
        else:
            self.endPoint = point

        self.setLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y())
        self.textLabelProxy.setGeometry(QRectF(self.boundingRect().x() + self.boundingRect().width() / 2,
                                               self.boundingRect().y() + self.boundingRect().height() / 2,
                                               60, 20))

    def addOnCanvas(self, scene):
        scene.addItem(self)
        scene.addItem(self.textLabelProxy)

    def removeFromCanvas(self):
        try:
            self.startCircle.removeConnection(self.endCircle)
            self.endCircle.removeConnection(self.startCircle)
        except Exception as e:
            pass
        finally:
            self.scene().removeItem(self)


