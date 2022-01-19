import sys
import time

from PyQt5 import QtWidgets,QtCore, QtGui

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui_lay = QtWidgets.QVBoxLayout()
        self.ui_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.ui_widget)
        self.ui_widget.setLayout(self.ui_lay)
        self.ui_btn = QtWidgets.QPushButton('Create Window', self)
        self.ui_lay.addWidget(self.ui_btn)
        self.ui_btn.clicked.connect(self.create_window)
        self.other_window = None

    def create_window(self):
        self.other_window = QtWidgets.QMainWindow(self)
        self.other_widget = QtWidgets.QWidget(self.other_window)
        self.other_window.setCentralWidget(self.other_widget)
        self.other_lay = QtWidgets.QVBoxLayout()
        self.other_widget.setLayout(self.other_lay)
        self.ui_chk = QtWidgets.QCheckBox('Link', self.other_window)
        self.other_lay.addWidget(self.ui_chk)
        self.other_window.show()
        self.position_other_window()

    def position_other_window(self):
        geo = self.geometry()
        geo.moveLeft(geo.left() + geo.width() + 10)
        self.other_window.setGeometry(geo)

    def moveEvent(self, event):
        super(MyWindow, self).moveEvent(event)
        if self.other_window and self.ui_chk.isChecked():
            self.position_other_window()
            # diff = event.pos() - event.oldPos()
            # geo = self.other_window.geometry()
            # geo.moveTopLeft(geo.topLeft() + diff)
            # self.other_window.setGeometry(geo)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()