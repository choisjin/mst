#-*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
                                          # 배경화면 셋팅
def background_set(self):
    #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    
    pal = QtGui.QPalette()
    pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
    self.setAutoFillBackground(True)
    self.setPalette(pal)