import sys
import logging

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from check import *


class SignalHandler(QObject):
    open_window2_signal = pyqtSignal()


class Auth(QMainWindow):
    def __init__(self, signal_handler):
        super().__init__()
        uic.loadUi('auth.ui', self)
        self.signal_handler = signal_handler
        self.sup.clicked.connect(self.auth)
        self.sin.clicked.connect(self.register)
        self.base_line_edit = [self.Login, self.Password]
        self.check = CheckThread()
        self.check.Mysignal.connect(self.handle_signal)
        self.check.start()

    # Проверка правильности ввода
    def check_in(func):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            func(self)

        return wrapper

    def handle_signal(self, value):
        try:
            if value == 'Успешная авторизация' or value == 'Регистрация прошла успешно!':
                self.signal_handler.open_window2_signal.emit()
                self.hide()
            else:
                QMessageBox.about(self, 'Оповещение', value)
        except Exception as e:
            logging.exception(f"Error in handle_signal: {e}")
            QMessageBox.critical(self, "Ошибка", f"Произошла критическая ошибка: {e}")

    @check_in
    def auth(self):
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_login(name, passw)

    @check_in
    def register(self):
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_register(name, passw)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    app = QApplication(sys.argv)
    signal_handler = SignalHandler()
    auth = Auth(signal_handler)
    main = Main()
    signal_handler.open_window2_signal.connect(main.show)
    auth.show()
    logging.info("Application started")
    sys.exit(app.exec())
