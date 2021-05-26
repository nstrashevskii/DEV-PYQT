import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import test_form


class MyFirstWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyFirstWindow, self).__init__(parent)

        self.InitUI()

        self.ui = test_form.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonOpen.clicked.connect(self.onPushButtonOpenClicked)
        self.ui.pushButtonAccept.clicked.connect(self.onPushButtonAcceptClicked)

    def onPushButtonOpenClicked(self):
        FilePath, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбор файла', '.')
        print(ok)
        if not ok:
            return
        print(FilePath)

    def onPushButtonAcceptClicked(self):
        print(self.ui.lineEdit.text())
        print(self.ui.lineEdit_2.text())
        print(self.ui.lineEdit_3.text())
        print(self.ui.lineEdit_4.text())

    def InitUI(self):
        # centralWidget = QtWidgets.QWidget()

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.textEdit_1 = QtWidgets.QTextEdit()

        self.textEdit_1.append('textEdit_1')

        textEdit_2 = QtWidgets.QTextEdit()
        textEdit_2.append('textEdit_2')

        textEdit_3 = QtWidgets.QTextEdit()
        textEdit_3.append('textEdit_3')

        splitter.addWidget(self.textEdit_1)
        splitter.addWidget(textEdit_2)
        splitter.addWidget(textEdit_3)

        self.setCentralWidget(splitter)

        self.textEdit_1.installEventFilter(self)

    def eventFiletr(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched == self.textEdit_1 and event.type() == QtCore.QEvent.Resize:
            print(self.textEdit_1.size().height())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstWindow()
    myform.show()
    sys.exit(app.exec_())
