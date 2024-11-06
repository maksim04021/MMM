from PyQt6 import QtCore, QtGui, QtWidgets
from db_handler import *


class CheckThread(QtCore.QThread):
    Mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, password):
        login(name, password, self.Mysignal)
    
    def thr_register(self, name, password):
        register(name, password, self.Mysignal)
