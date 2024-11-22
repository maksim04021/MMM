import sqlite3
import secrets
import hashlib
import logging


def hash_password(password):
    salt = secrets.token_hex(16)  # 16 байт соли (32 hex символа)
    salted_password = salt + password
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return salt + ":" + hashed_password  # Сохраняем соль вместе с хэшем


def update_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("SELECT id, name, password FROM user")
        rows = cur.fetchall()

        for row in rows:
            user_id, name, password = row
            if ":" not in password:  # проверка на наличие соли
                salt = secrets.token_hex(16)
                hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
                new_password = salt + ":" + hashed_password
                cur.execute("UPDATE user SET password = ? WHERE id = ?", (new_password, user_id))
                con.commit()
                print(f"Updated password for user {name} (id: {user_id})")

    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def login(login, password, signal):
    logging.debug(f"login function called with login: {login}, password: {password}")
    try:
        con = sqlite3.connect('HER.db')
        cur = con.cursor()
        logging.debug(f"Database connection established")

        cur.execute("SELECT password FROM user WHERE name = ?", (login,))
        result = cur.fetchone()
        logging.debug(f"Query executed. Result: {result}")

        if result:
            salt, stored_hash = result[0].split(":")
            generated_hash = hashlib.sha256((salt + password).encode()).hexdigest()
            if generated_hash == stored_hash:
                logging.debug(f"Login successful for user: {login}")
                signal.emit('Успешная авторизация')
            else:
                logging.debug(f"Incorrect password for user: {login}")
                signal.emit('Неверный пароль')
        else:
            logging.debug(f"User not found: {login}")
            signal.emit('Пользователь не найден')

    except (sqlite3.Error, ValueError) as e:
        logging.exception(f"Database or data error: {e}")
        signal.emit(f'Ошибка базы данных: {e}')
    finally:
        if cur:
            cur.close()
            logging.debug(f"Cursor closed")
        if con:
            con.close()
            logging.debug(f"Database connection closed")


def register(login, password, signal):
    logging.debug(f"register function called with login: {login}, password: {password}")
    try:
        con = sqlite3.connect('HER.db')
        cur = con.cursor()
        logging.debug(f"Database connection established")
        hashed_password = hash_password(password)

        cur.execute("SELECT COUNT(*) FROM user WHERE name = ?", (login,))
        count = cur.fetchone()[0]
        logging.debug(f"User count check result: {count}")

        if count > 0:
            logging.debug(f"Username already exists: {login}")
            signal.emit('Имя пользователя уже занято!')
        else:
            cur.execute("INSERT INTO user (name, password) VALUES (?, ?)", (login, hashed_password))
            con.commit()
            logging.debug(f"User registered: {login}")
            signal.emit('Регистрация прошла успешно!')

    except sqlite3.Error as e:
        logging.exception(f"Database error: {e}")
        signal.emit(f'Ошибка базы данных: {e}')
    finally:
        if cur:
            cur.close()
            logging.debug(f"Cursor closed")
        if con:
            con.close()
            logging.debug(f"Database connection closed")


update_database('HER.db')
