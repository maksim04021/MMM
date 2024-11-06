import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from check import *
from des import *
import uuid

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('auth.ui', self)
        self.sup.clicked.connect(self.auth)
        self.sin.clicked.connect(self.register)
        self.base_line_edit = [self.Login, self.Password]
        self.check = CheckThread()
        self.check.Mysignal.connect(self.signal_handler)
    
    #Проверка правильности ввода
    def check_in(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)
    
    @check_in
    def auth(self):
        name = self.Login
        passw = self.Password
        self.check.thr_login(name, passw)
    
    @check_in
    def register(self):
        name = self.Login
        passw = self.Password
        self.check.thr_register(name, passw)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())