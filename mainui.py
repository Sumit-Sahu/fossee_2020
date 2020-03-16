import sys
from random import randint, random

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsView, QAction, QToolButton, \
    QButtonGroup, QMessageBox, QLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QRectF, QFileInfo, QPoint, QRect, QSize

from canvas import Canvas
from circle import Circle
from connectingline import ConnectingLine


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.title = "Create Circles"
        self.InitWindow()

    def InitWindow(self):
        self.createActions()
        self.createToolbars()

        desktop = app.desktop()
        self.scene = Canvas()
        self.scene.setSceneRect(0, 0, desktop.width(), desktop.height()-self.editToolBar.height())

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

    def pointerGroupClicked(self):
        Canvas.myMode = self.connectionTypeGroup.checkedId()

    def createActions(self):
        self.addAction = QAction(QIcon('images/add.png'), "Add Circle", self)
        self.addAction.triggered.connect(self.addCircle)

        self.deleteAction = QAction(QIcon('images/delete.png'), "Delete circle", self)
        self.deleteAction.triggered.connect(self.deleteCircle)

        self.generateReportAction = QAction(QIcon('images/report.gif'), "Generate Report", self)
        self.generateReportAction.triggered.connect(self.saveAsPdf)

        self.saveAction = QAction(QIcon('images/image.png'), "Save", self)
        self.saveAction.triggered.connect(self.saveAsPng)

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setFixedHeight(100)
        self.editToolBar.setIconSize(QSize(50,50))
        self.editToolBar.addAction(self.addAction)
        self.editToolBar.addAction(self.deleteAction)
        self.editToolBar.addAction(self.generateReportAction)
        self.editToolBar.addAction(self.saveAction)
        self.editToolBar.setMovable(False)
        

        pointerButton = QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QIcon('images/pointer.png'))
        linePointerButton = QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QIcon('images/linepointer.png'))

        self.connectionTypeGroup = QButtonGroup()
        self.connectionTypeGroup.addButton(pointerButton, Canvas.MoveItem)
        self.connectionTypeGroup.addButton(linePointerButton, Canvas.InsertLine)
        self.connectionTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        self.lineToolbar = self.addToolBar("Pointer type")
        self.lineToolbar.setFixedHeight(100)
        self.lineToolbar.setIconSize(QSize(50, 50))
        self.lineToolbar.addWidget(linePointerButton)
        self.lineToolbar.addWidget(pointerButton)
        self.lineToolbar.setMovable(False)

    def addCircle(self):
        start = self.scene.sceneRect().x()
        end = self.scene.sceneRect().width()
        x_coordinate = randint(start, end)
        start = self.scene.sceneRect().y()+self.editToolBar.height()
        end = self.scene.sceneRect().height()
        y_coordinate = randint(start, end)
        circle = Circle(x_coordinate, y_coordinate)
        circle.addOnCanvas(self.scene)

    def deleteCircle(self):
        circles = self.scene.selectedItems()
        for circle in circles:
            circle.removeFromCanvas()

    def saveAsPng(self):
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save file', "image.png", '*.png')
            if not fileName:
                return
            if QFileInfo(fileName).suffix() != 'png':  # check if user type other extension with name
                fileName += '.png'
            pixmap = self.view.grab()
            pixmap.save(fileName, 'PNG')
        except:
            QMessageBox.information(self, 'Error', 'Image not saved')

    def saveAsPdf(self):
        try:
            from reportlab.pdfgen.canvas import Canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.lib.colors import red, blue

        except:
            QMessageBox.information(self, 'Alert', 'Process Declined \n import reportlab')
            return

        items = self.scene.items()
        fileName, _ = QFileDialog.getSaveFileName(self, directory='file.pdf',
                                                  filter='PDF Files *.pdf(*.pdf);;All Files *(*)')
        if not fileName:
            return
        if QFileInfo(fileName).suffix() != 'pdf':  # check if user type other extension with name
            fileName += '.pdf'

        canvas = Canvas(fileName, pagesize=A4)
        canvas.setFont("Times-Roman", 30)
        canvas.setFillColor(red)
        canvas.drawCentredString(4 * inch, 11 * inch, "Connection Report")
        canvas.setFillColor(blue)
        size = 20
        y = 10 * inch
        x = 1.5 * inch
        line = 1
        count = 1
        for item in items:
            if type(item) == ConnectingLine:
                connectionLine = item.textLabel.text()
                startCircle = item.getStartCircle().textLabel.text()
                endCircle = item.getEndCircle().textLabel.text()
                string = "{}:({},{})".format(connectionLine, startCircle, endCircle)

                if count > 20:
                    canvas.showPage()
                    canvas.setFillColor(blue)
                    size = 20
                    y = 11 * inch
                    x = 1.5 * inch
                    count = 1

                canvas.setFont("Helvetica", size)
                canvas.drawString(1 * inch, y, str(line) + '.')
                canvas.drawString(x, y, string)
                count += 1
                line += 1
                y = y - size * 2

        try:
            canvas.save()
        except:
            QMessageBox.information(self, 'Error', 'Error Generating Report \n'
                                                   'first close file {}'.format(fileName))


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        application = Window()
        application.showMaximized()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
