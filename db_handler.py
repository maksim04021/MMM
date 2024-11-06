import sqlite3
import time
import random


def login(login, password, signal):
    con = sqlite3.connect('HER.db')
    cur = con.cursor()

    # Проверка пользователя
    cur.execute("SELECT password FROM user WHERE name = ?", (login.text(),))
    value = cur.fetchall()

    if value != []:
        if value[0][0] == password.text():
            signal.emit('Успешная авторизация')
        else:
            signal.emit('Проверьте данные и повторите попытку')
    else:
        signal.emit('Логин не найден, проверьте правильность ввода или зарегистрируйтесь')
    
    cur.close()
    con.close()

def register(login, password, signal):
    con = sqlite3.connect('HER.db')
    cur = con.cursor()

    # Проверка пользователя
    cur.execute("SELECT password FROM user WHERE name = ?", (login.text(),))
    value = cur.fetchall()

    if value != []:
        signal.emit('Логин занят!')
    elif value == []:
        timestamp = int(time.time() * 1000)  # Текущая временная метка в миллисекундах
        random_number = random.randint(1000, 9999)  # Случайное число
        unique_id = f"{timestamp}-{random_number}"
        cur.execute("INSERT INTO user (id, name, password) VALUES (?, ?, ?)", (unique_id, login.text(), password.text()))
        signal.emit('Вы успешно зарегистрированы!')
        con.commit()
    
    cur.close()
    con.close()
