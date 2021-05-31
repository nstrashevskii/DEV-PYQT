from PyQt5 import QtCore, QtWidgets, QtGui
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.brashColor = QtCore.Qt.black
        self.brushSize = 2

        self.initUI()
        self.pbColor.clicked.connect(self.initBrush)
        self.sliderSize.valueChanged.connect(self.sliderSizeSet)

    def initUI(self):
        self.setWindowTitle('paint')
        self.setGeometry(QtCore.QRect(200, 200, 800, 500))
        self.setMinimumSize(300, 200)
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        self.pbColor = QtWidgets.QPushButton('цвет')
        self.pbColor.setMinimumWidth(50)

        self.sliderSize = QtWidgets.QSlider()
        self.sliderSize.setMinimumSize(2, 2)
        self.sliderSize.setMaximumSize(100, 100)
        self.sliderSize.setOrientation(QtCore.Qt.Horizontal)

        self.brushSizeline = QtWidgets.QLineEdit('2')
        self.brushSizeline.setAlignment(QtCore.Qt.AlignHCenter)
        self.brushSizeline.setMaximumWidth(30)
        self.brushSizeline.setEnabled(False)

        brushSizeLabel = QtWidgets.QLabel('Текущий размер кисти')
        brushSizeLabel.setMaximumSize(120, 120)

        self.image = QtGui.QImage(QtCore.QSize(800, 500), QtGui.QImage.Format_ARGB32_Premultiplied)
        self.image.fill(QtCore.Qt.gray)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))

        layontH = QtWidgets.QHBoxLayout()
        layontH.addWidget(self.pbColor)
        layontH.addWidget(self.sliderSize)
        layontH.addWidget(brushSizeLabel)
        layontH.addWidget(self.brushSizeline)
        layontH.setSpacing(10)

        layoutV = QtWidgets.QVBoxLayout()
        layoutV.addWidget(self.label)
        layoutV.addItem(layontH)

        centralWidget.setLayout(layoutV)

    def initBrush(self):
        dlg = QtWidgets.QColorDialog(self)
        dlg.show()
        dlg.exec_()
        self.brashColor = dlg.currentColor()
        self.lastPoint = QtCore.QPoint()

    def sliderSizeSet(self):
       self.brushSize = self.sliderSize.value()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            print(event.pos())
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() and QtCore.Qt.LeftButton:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(self.brashColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_form = Window()
    my_form.show()
    sys.exit(app.exec_())