import datetime
import sys, os, re, time, subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
import PingMonitor_design, Tracert_design
import shutil


class PingMonitor(QtWidgets.QWidget, PingMonitor_design.Ui_Form):
    def __init__(self, parent=None):
        super(PingMonitor, self).__init__(parent)

        self.t = AllThread()
        self.setupUi(self)
        with open("IP.txt") as f:
            line_count = 0
            for line in f:
                line_count += 1
                self.tableWidget.setRowCount(line_count)
                self.tableWidget.setItem(line_count - 1, 0, QtWidgets.QTableWidgetItem(line))

        shutil.copyfile('IP.txt', 'Current_IP.txt')

        self.new_ip_row = self.tableWidget.rowCount()

        self.pushButton_3.clicked.connect(self.onPushButtonTracerClicked)
        self.pushButton_4.clicked.connect(self.onPushButtonInputIPClicked)

        self.pushButton.clicked.connect(self.startThread)
        self.pushButton_2.clicked.connect(self.stopThread)

        self.t.started.connect(lambda: print("Поток запущен"))
        self.t.finished.connect(lambda: print("Поток завершен"))
        self.t.current_count.connect(self.setTextTable, QtCore.Qt.QueuedConnection)

    def stopThread(self):
        self.t.status = False

    def startThread(self):
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0) is None:
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Не введен ip адрес')
                return
        self.t.start()

    def onPushButtonTracerClicked(self):
        self.saveCurrentIp()
        self.trace = TracerWindow()
        self.trace.show()
        self.trace.threadTracer.start()
        if self.trace.closeEvent:
            self.trace.threadTracer.status = False

    def onPushButtonInputIPClicked(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                                  'Введите ip адрес:')

        ipRegex = re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

        if ok and ipRegex.match(text):
            with open("Current_IP.txt", "a+") as f:
                f.writelines(f'{str(text)}\n')
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(text) + '\n'))
        elif ipRegex.match(text) is False:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Введен некорректный ip адрес!')
            error_dialog.exec_()

    def setTextTable(self, response):
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() == '':
                continue
            else:
                try:
                    response1 = subprocess.check_output(
                        ['ping', '-c', '1', self.tableWidget.item(i, 0).text()],
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                    )
                except subprocess.CalledProcessError:
                    response1 = None
                if response1 is None:
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('Host is DOWN'))
                    self.plainTextEdit.appendPlainText(
                        f'{datetime.datetime.now()} : Host {self.tableWidget.item(i, 0).text()} not responding')
                else:
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('Host is UP'))
                    self.plainTextEdit.appendPlainText(f'{datetime.datetime.now()} : {response1}')

    def saveIp(self):
        with open('IP.txt', 'w') as f:
            for i in range(self.tableWidget.rowCount()):
                f.writelines(self.tableWidget.item(i, 0).text())

    def saveLogs(self):
        time_logs = datetime.datetime.now()
        with open(f'log_{time_logs}.txt', 'w') as f:
            f.write(self.plainTextEdit.toPlainText())

    def saveCurrentIp(self):
        with open('Current_IP.txt', 'w') as f:
            for i in range(self.tableWidget.rowCount()):
                f.writelines(self.tableWidget.item(i, 0).text())

    def clearCurrentIP(self):
        with open('Current_IP.txt', 'w') as f:
            f.write('')

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        SaveOrNot = QtWidgets.QMessageBox.question(self, 'Сохранение IP адресов', 'Сохранить список IP адресов?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.Yes)
        if SaveOrNot == QtWidgets.QMessageBox.Yes:
            self.saveIp()
            self.saveLogs()
            self.clearCurrentIP()
            super().closeEvent(event)
        else:
            self.saveLogs()
            self.clearCurrentIP()
            super().closeEvent(event)


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
        with open('Current_IP.txt') as f:
            for line in f:
                try:
                    response = subprocess.check_output(
                        ['traceroute', line],
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                    )
                except subprocess.CalledProcessError:
                    response = None
                self.plainTextEdit.appendPlainText(response)

    def stopThread(self):
        self.threadTracer.status = False

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.threadTracer.status = False
        super().closeEvent(event)


class AllThread(QtCore.QThread):
    current_count = QtCore.pyqtSignal(str)

    def run(self) -> None:
        self.status = True
        while self.status:
            self.current_count.emit('')
            time.sleep(10)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_form = PingMonitor()
    my_form.show()
    sys.exit(app.exec_())
