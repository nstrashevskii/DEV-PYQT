import sys, time, psutil
# from PySide2 import QtCore
from PyQt5 import QtWidgets, QtCore


class MyFirstProgressBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyFirstProgressBar, self).__init__(parent)
        self.cpu_threed = CPUPercent()
        self.cpu_threed.start()
        self.initUi()

    def initUi(self):
        cpu_percent_list = psutil.cpu_percent(interval=1, percpu=True)
        self.layout = QtWidgets.QHBoxLayout()
        for cpu_num in range(psutil.cpu_count()):
            self.layout.addWidget(cpu_counting(cpu_num+1))
        self.setLayout(self.layout)
        self.cpu_threed.cpu_count.connect(self.update_pb, QtCore.Qt.QueuedConnection)

    def update_pb(self):
        cpu_percent_list = psutil.cpu_percent(interval=1, percpu=True)
        for w in range(self.layout.count()):
            l1 = self.layout.itemAt(w).widget()
            l2 = l1.layout().itemAt(0).widget()
            l2.setValue(cpu_percent_list[w])
            l3 = l1.layout().itemAt(1).widget()
            l3.setText(str(f'загрузка ядра {cpu_percent_list[w]} %'))



class cpu_counting(QtWidgets.QWidget):
    def __init__(self, cpu_num, parent=None):
        super(cpu_counting, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.qlablePercent = QtWidgets.QLabel(f'')
        self.qlable = QtWidgets.QLabel(f'CPU {cpu_num}')
        self.qlable.setAlignment(QtCore.Qt.AlignHCenter)
        self.prBar = QtWidgets.QProgressBar()
        self.prBar.setOrientation(QtCore.Qt.Vertical)
        self.prBar.setRange(0, 100)
        self.prBar.setValue(0)
        self.prBar.setTextVisible(True)
        self.prBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.prBar)
        layout.addWidget(self.qlablePercent)
        layout.addWidget(self.qlable)

        self.setLayout(layout)


class CPUPercent(QtCore.QThread):
    cpu_count = QtCore.pyqtSignal(list)

    def run(self) -> None:
        self.cpu_percent_list = psutil.cpu_percent(interval=1, percpu=True)
        while True:
            self.cpu_count.emit(self.cpu_percent_list)
            time.sleep(4)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstProgressBar()
    myform.show()
    sys.exit(app.exec_())
