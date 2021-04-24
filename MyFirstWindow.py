import sys
# from PySide2 import QtWidgets
from PyQt5 import QtWidgets


class MyFirstWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        layout = QtWidgets.QVBoxLayout()
        button = QtWidgets.QPushButton('Кнопка')


        layout.addWidget(button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstWindow()
    myform.show()
    sys.exit(app.exec_())
