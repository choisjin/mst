#-*- coding:utf-8 -*-
import sys, os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

import window_background_set
import window_main


class LoginForm(QtWidgets.QDialog):                     # 로그인 화면
    app = QtWidgets.QApplication(sys.argv)
    def __call__(self):                                 # 로그인 화면 셋팅
        #super(LoginForm, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        window_background_set.background_set(self)
        
        width = 265
        height = 110
        self.setFixedSize(width, height)

        logo_label = QtWidgets.QLabel(self)
        logo_label.resize(100, 100)
        logo_label.move(160, 5)
        
        image_path = os.path.dirname(os.path.realpath(__file__))    # 현재파일 경로
    
        pixmap = QtGui.QPixmap('%s/Data/Image/Logo.png' %image_path)
        logo_label.setPixmap(pixmap)

        self.label_name = QtWidgets.QLabel('<font size="2"> ID </font>', self)
        self.label_name.resize(20, 30)
        self.label_name.move(10, 5)

        self.lineEdit_username = QtWidgets.QLineEdit(self)
        self.lineEdit_username.setPlaceholderText('Enter your ID')
        self.lineEdit_username.resize(125, 30)
        self.lineEdit_username.move(30, 5)                
        
        self.label_password = QtWidgets.QLabel('<font size="2"> PW </font>', self)
        self.label_password.resize(20, 30)
        self.label_password.move(5, 40)   

        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText('Enter your pw')
        self.lineEdit_password.resize(125, 30)
        self.lineEdit_password.move(30, 40)

        self.button_login = QtWidgets.QPushButton('Login', self)
        self.button_login.clicked.connect(self.check_password)
        self.button_login.resize(60, 30)
        self.button_login.move(30, 75)
        self.button_login.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        self.button_exit = QtWidgets.QPushButton('Exit', self)
        self.button_exit.clicked.connect(self.close)
        self.button_exit.resize(60, 30)
        self.button_exit.move(95, 75)
        self.button_exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        
        self.center()
        
        self.position = self.qr.topRight()
        self.show()
    def check_password(self):                           # ID, PW 확인
        msg = QtWidgets.QMessageBox()

        if self.lineEdit_username.text() == 'choi3206' and self.lineEdit_password.text() == '0608':
            self.hide()
            self.main = window_main.MainWindow(self.position)
        else :
            msg.setText('Check your ID, PW')
            msg.exec_()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topRight())    

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.check_password()
        
        elif e.key() == Qt.Key_Escape:
            sys.exit()        

    sys.exit(app.exec_())
# if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # init = LoginForm()
    # init.show()
    # sys.exit(app.exec_())
    