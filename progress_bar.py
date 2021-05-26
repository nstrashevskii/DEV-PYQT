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
        self.layout = QtWidgets.QHBoxLayout()
        for cpu_num in range(psutil.cpu_count()):
            self.layout.addWidget(cpu_counting(cpu_num+1))
        self.setLayout(self.layout)
        self.cpu_threed.cpu_count.connect(self.update_pb, QtCore.Qt.QueuedConnection)

    def update_pb(self, cpu_percent_list):
        for w in range(self.layout.count()):
            self.layout.itemAt(w).widget()


class cpu_counting(QtWidgets.QWidget):
    def __init__(self, cpu_num, parent=None):
        super(cpu_counting, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        self.qlable = QtWidgets.QLabel(f'CPU {cpu_num}')
        self.qlable.setAlignment(QtCore.Qt.AlignHCenter)
        self.prBar = QtWidgets.QProgressBar()
        self.prBar.setOrientation(QtCore.Qt.Vertical)
        self.prBar.setRange(0, 100)
        self.prBar.setValue(0)
        self.prBar.setTextVisible(True)
        self.prBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.prBar)
        layout.addWidget(self.qlable)

        self.setLayout(layout)


class CPUPercent(QtCore.QThread):
    cpu_count = QtCore.Signal(list)

    while True:



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = MyFirstProgressBar()
    myform.show()
    sys.exit(app.exec_())
