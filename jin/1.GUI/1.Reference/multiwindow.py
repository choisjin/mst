import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QDesktopWidget
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        #win = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        #label = QtWidgets.QLabel()

        btn_camera1 = QtWidgets.QPushButton("Camera 1")
        btn_camera2 = QtWidgets.QPushButton("Camera 2")
        btn_stop = QtWidgets.QPushButton("Stop") 

        #vbox.addWidget(label)
        vbox.addWidget(btn_camera1)
        vbox.addWidget(btn_camera2)
        vbox.addWidget(btn_stop)

        btn_camera1.clicked.connect(self.openCameraViewer)
        self.center()
        self.setLayout(vbox)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openCameraViewer(self):
        self.close()
        self.second = Cam1()
        self.second.exec_()
        self.show()
        
class Cam1(QDialog):
        def __init__(self) :
            super(Cam1, self).__init__()
            #win = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout()
            #label = QtWidgets.QLabel()

            btn_camera1 = QtWidgets.QPushButton("Camera 1")
            btn_stop = QtWidgets.QPushButton("Stop") 

            #vbox.addWidget(label)
            vbox.addWidget(btn_camera1)
            vbox.addWidget(btn_stop)

            #btn_camera1.clicked.connect(self.openCameraViewer)
            self.center()
            self.setLayout(vbox)
            self.show()
        
        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   widget = QtWidgets.QStackedWidget()
   sys.exit(app.exec_())