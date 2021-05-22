import sys, time
from PySide2 import QtCore
from PyQt5 import QtWidgets


class MyFirstThread(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.t = FirstThread()
        self.initUi()

    def initUi(self):
        layout = QtWidgets.QVBoxLayout()
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText('Осталось секунд')

        self.button_start = QtWidgets.QPushButton('Старт')
        self.button_start.clicked.connect(self.startThread)

        self.button_stop = QtWidgets.QPushButton('Стоп')
        self.button_stop.clicked.connect(self.stopThread)

        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_stop)

        self.setLayout(layout)

        self.t.started.connect(lambda: print("Поток запущен"))
        self.t.finished.connect(lambda: print("Поток завершен"))
        self.t.current_count.connect(self.set_text_lineedit,QtCore.Qt.QueuedConnection)

    @QtCore.Slot()
    def stopThread(self):
        self.t.status = False

    @QtCore.Slot()
    def startThread(self):
        if len(self.lineEdit.text()) == 0:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не введено время')
            return
        self.t.set_sec(self.lineEdit.text())
        self.t.start()

    def set_text_lineedit(self, text):
        self.lineEdit.setText(text)


class FirstThread(QtCore.QThread):
    current_count = QtCore.Signal(str)

    def set_sec(self, sec):
        self.seconds = sec

    def run(self) -> None:
        self.status = True
        count = int(self.seconds)
        while self.status:
            count -= 1
            self.current_count.emit(str(count))
            time.sleep(1)
            if count == 0:
                break


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstThread()
    myform.show()
    sys.exit(app.exec_())
