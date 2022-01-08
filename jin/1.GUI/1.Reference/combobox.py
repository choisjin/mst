import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from datetime import datetime

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        self.lbl = QLabel('Camera Select', self)
        self.lbl.move(100, 100)
        
        cb = QComboBox(self)
        cb.addItem('Camera1')
        cb.addItem('Camera2')
        #cb.move(50, 50)
        cb.activated[str].connect(self.onActivated)

        self.setWindowTitle('QComboBox')
        self.setGeometry(300, 300, 100, 100)
        self.show()

    def CamViewer(self):
        QtWidgets.setCurrentIndex(QtWidgets.currentIndex()+1)

#class Cam1Viewer():

    # def initUI(self):
        # self.lbl = QLabel('Camera Select', self)
        # self.lbl.move(100, 100)
        # 
        # cb = QComboBox(self)
        # cb.addItem('Camera1')
        # cb.addItem('Camera2')
        #cb.move(50, 50)
# 
        # cb.activated[str].connect(self.onActivated)
# 
        # self.setWindowTitle('QComboBox')
        # self.setGeometry(300, 300, 300, 200)
        # self.show()

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())