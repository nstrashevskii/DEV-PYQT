import sys, os, re, time, subprocess, json
from PyQt5 import QtWidgets, QtGui, QtCore
import PingMonitor_design, PingMonitorSettings_design, Tracert_design
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal


# class LineEditIpAdd():
#     clicked = pyqtSignal()
#
#     def __init__(self, parent=None):
#         super(LineEditIpAdd, self).__init__(parent)
#
#         self.setMinimumSize(QtCore.QSize(480, 80))
#         self.setWindowTitle("Add IP Address")
#         layout = QtWidgets.QVBoxLayout()
#         label = QtWidgets.QLabel('Введите ip адрес', self)
#
#         ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
#         ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
#         ipValidator = QRegExpValidator(ipRegex, self)
#
#         self.lineEdit = QtWidgets.QLineEdit()
#         self.lineEdit.setValidator(ipValidator)
#         self.push_button_ok = QtWidgets.QPushButton('Добавить')
#         self.push_button_ok.setMinimumSize(100, 50)
#         self.push_button_ok.setMaximumSize(100, 50)
#         layout.addWidget(label)
#         layout.addWidget(self.lineEdit)
#         layout.addWidget(self.push_button_ok)
#         self.setLayout(layout)
#
#         self.push_button_ok.clicked.connect(self.onPushButtonOkClicked)

# def onPushButtonOkClicked(self):
#     text = self.lineEdit.text()
#
#     self.close()


class TracerWindow(QtWidgets.QWidget, Tracert_design.Ui_Form):
    def __init__(self, parent=None):
        super(TracerWindow, self).__init__(parent)
        self.setupUi(self)

        self.threadTracer = AllThread()
        self.threadTracer.started.connect(lambda: print("Поток запущен"))
        self.threadTracer.finished.connect(lambda: print("Поток завершен"))

        self.pushButton.clicked.connect(self.stopThread)
        self.threadTracer.current_count.connect(self.setTextTracer, QtCore.Qt.QueuedConnection)

    def setTextTracer(self):
        with open("IP.txt", "r") as f:
            text = f.read()
        try:
            response = subprocess.check_output(
                ['traceroute', text],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        except subprocess.CalledProcessError:
            response = None
        print(response)
        self.plainTextEdit.appendPlainText(response)

    @QtCore.Slot()
    def stopThread(self):
        self.threadTracer.status = False




# class PingMonitorSettings(QtWidgets.QWidget, PingMonitorSettings_design.Ui_Form):
#     def __init__(self, parent=None):
#         super(PingMonitorSettings, self).__init__(parent)
#         self.setupUi(self)
#
#         self.pushButton.clicked.connect(self.showDialog)
#
#     def showDialog(self):
#         text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
#                                                   'Введите ip адрес:')
#
#         if ok:
#             self.listWidget.addItem(str(text))
#
#     # def onPushButtonAddClicked(self):
#     #     self.add = LineEditIpAdd()
#     #     self.add.show()
#
#     def list_widget_add(self, text):
#         self.listWidget.addItem(text)


class PingMonitor(QtWidgets.QWidget, PingMonitor_design.Ui_Form):
    def __init__(self, parent=None):
        super(PingMonitor, self).__init__(parent)

        self.t = AllThread()

        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.onPushButtonTracerClicked)
        self.pushButton_4.clicked.connect(self.onPushButtonInputIPClicked)

        self.pushButton.clicked.connect(self.startThread)
        self.pushButton_2.clicked.connect(self.stopThread)

        self.t.started.connect(lambda: print("Поток запущен"))
        self.t.finished.connect(lambda: print("Поток завершен"))
        self.t.current_count.connect(self.setTextTable, QtCore.Qt.QueuedConnection)

    @QtCore.Slot()
    def stopThread(self):
        self.t.status = False

    @QtCore.Slot()
    def startThread(self):
        if self.tableWidget.item(0, 0) is None:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не введен ip адрес')
            return
        self.t.start()

    @QtCore.Slot()
    def onPushButtonTracerClicked(self):
        self.trace = TracerWindow()
        self.trace.show()
        self.trace.threadTracer.start()
        if self.trace.closeEvent:
            self.trace.threadTracer.status = False

    @QtCore.Slot()
    def onPushButtonInputIPClicked(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                  'Введите ip адрес:')

        ipRegex = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

        if ok and ipRegex.match(text):
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(text)))
            with open("IP.txt", "w") as f:
                f.writelines(str(text))
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Введен некорректный ip адрес!')
            error_dialog.exec_()

    def setTextTable(self, response):
        try:
            response1 = subprocess.check_output(
                ['ping', '-c', '3', self.tableWidget.item(0, 0).text()],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        except subprocess.CalledProcessError:
            response1 = None
        self.plainTextEdit.appendPlainText(response1)
        response = os.system("ping -c 1 " + self.tableWidget.item(0, 0).text())
        if response == 0:
            self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem('Host is UP'))

        else:
            self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem('Host is DOWN'))


class AllThread(QtCore.QThread):
    current_count = QtCore.pyqtSignal(str)

    def run(self) -> None:
        self.status = True
        count = 10
        while self.status:
            count -= 1
            self.current_count.emit('')
            time.sleep(3)
            if count == 0:
                break


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_form = PingMonitor()
    my_form.show()
    sys.exit(app.exec_())
