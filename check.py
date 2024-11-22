from PyQt6 import QtCore
from db_handler import *
import logging


class CheckThread(QtCore.QThread):
    Mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, password):
        logging.debug(f"CheckThread.thr_login: name = {name}, password = {password}")  # логирование
        if not name or not password:
            self.Mysignal.emit("Ошибка: Не все поля заполнены")
            return False
        login(name, password, self.Mysignal)
        return True

    def thr_register(self, name, password):
        logging.debug(f"CheckThread.thr_register: name = {name}, password = {password}")  # логирование
        if not name or not password:
            self.Mysignal.emit("Ошибка: Не все поля заполнены")
            return
        register(name, password, self.Mysignal)
