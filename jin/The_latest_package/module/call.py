import sys, os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

import window_background_set

import window_logincall
from multiprocessing import Process

p1 = Process(target = window_logincall.LoginForm())

p1.start()