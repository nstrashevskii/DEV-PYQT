import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class MyFirstWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyFirstWindow, self).__init__(parent)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstWindow()
    myform.show()
    sys.exit(app.exec_())
