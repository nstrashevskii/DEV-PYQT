import searching_ui
import sys, os, re, time, subprocess
from PyQt5 import QtWidgets, QtGui, QtCore


class SearchingFile(QtWidgets.QWidget, searching_ui.Ui_Form):
    def __init__(self, parent=None):
        super(SearchingFile, self).__init__(parent)

        self.t = AllThread()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.startThread)
        self.pushButton_2.clicked.connect(self.onPushButtonOpenClicked)

        self.t.started.connect(lambda: print("Поток запущен"))
        self.t.finished.connect(lambda: print("Поток завершен"))
        self.t.current_count.connect(self.addTextPlainText, QtCore.Qt.QueuedConnection)

    def startThread(self):
        if self.lineEdit.text() is None:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не введено содержимое файла')
            return
        elif self.lineEdit_2.text() is None:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не введена директория для поиска')
            return

        self.t.start()

    def stopThread(self):
        self.t.status = False

    def onPushButtonOpenClicked(self):
        self.FilePath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбор файла', '.')
        self.lineEdit_2.setText(self.FilePath)

    def addTextPlainText(self):
        text = self.lineEdit.text()
        files = os.listdir(self.FilePath)
        for file in files:
            print(file)
            with open(f'{self.FilePath}/{file}') as f:
                if text in f.read():
                    self.plainTextEdit.appendPlainText(file)


class AllThread(QtCore.QThread):
    current_count = QtCore.pyqtSignal(str)

    def run(self) -> None:
        self.status = True
        count = 1
        while self.status:
            count -= 1
            self.current_count.emit('')
            time.sleep(1)
            if count == 0:
                break


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_form = SearchingFile()
    my_form.show()
    sys.exit(app.exec_())
