import pygame
import sys
import logging
import os

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject, QSize, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt6.QtGui import QIcon
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

from check import CheckThread
from metadata_handler import * 

logging.basicConfig(filename='music_player.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Обработчик сигналов ---
class SignalHandler(QObject):
    open_window2_signal = pyqtSignal()

# --- Окно авторизации ---
class Auth(QMainWindow):
    def __init__(self, signal_handler):
        super().__init__()
        uic.loadUi('auth.ui', self)
        self.signal_handler = signal_handler
        self.sup.clicked.connect(self.auth)  # Подключение кнопки входа
        self.sin.clicked.connect(self.register)  # Подключение кнопки регистрации
        self.base_line_edit = [self.Login, self.Password]
        self.check = CheckThread()
        self.check.Mysignal.connect(self.handle_signal)  # Подключение сигнала от CheckThread
        self.check.start()

    def check_in(func):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if not line_edit.text():  # Проверка на пустые строки
                    QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
                    return
            func(self)
        return wrapper

    def handle_signal(self, value):
        try:
            if value == 'Успешная авторизация':
                self.signal_handler.open_window2_signal.emit()
                self.hide()
            elif value == 'Регистрация прошла успешно!':
                QMessageBox.information(self, 'Успех!', value)
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', value)
        except Exception as e:
            logging.exception(f"Ошибка в handle_signal: {e}")
            QMessageBox.critical(self, "Критическая ошибка", f"Произошла критическая ошибка: {e}")

    @check_in
    def auth(self):  # Обработка попытки входа
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_login(name, passw)

    @check_in
    def register(self):  # Обработка попытки регистрации
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_register(name, passw)

# --- Главное окно приложения ---
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        uic.loadUi('main.ui', self)
        self.init_buttons()
        self.muteF = True
        self.playF = False
        self.current_song = None
        self.is_paused = False
        self.playlist_filenames = get_all_songs('music_database.db')
        self.add_song_to_playlist = ()
        self.shuffle_mode = False
        self.repeat_mode = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_duration_slider)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.duration_slider.sliderPressed.connect(self.slider_pressed)
        self.duration_slider.sliderReleased.connect(self.slider_released)
        self.load_songs_from_db()
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_song)


    # --- Инициализация кнопок ---
    def init_buttons(self):
        self.sound_button.clicked.connect(self.mute)
        self.add_sound.clicked.connect(self.add_song) #Переименовано в add_song
        self.replay_button.clicked.connect(self.replay) # Необходимо реализовать эту функцию
        self.shuffle_button.clicked.connect(self.shuffle) # Необходимо реализовать эту функцию
        self.main_btn1.clicked.connect(self.run) # Необходимо реализовать эту функцию
        self.forw_button.clicked.connect(lambda: self.seek(15)) #Перемотка вперед на 15 секунд
        self.following_button.clicked.connect(self.play_next_song) # Воспроизвести следующую песню
        self.pre_button.clicked.connect(lambda: self.seek(-15)) #Перемотка назад на 15 секунд
        self.previous_button.clicked.connect(self.play_previous_song) # Воспроизвести предыдущую песню
        self.search_btn.clicked.connect(self.search_song) #Необходимо реализовать функцию поиска

        self.set_button_icon(self.sound_button, "icon/volumeup.png", QSize(20, 20))
        self.set_button_icon(self.add_sound, "icon/add_box.png", QSize(20, 20))
        self.set_button_icon(self.shuffle_button, "icon/shuffle.png", QSize(20, 20))
        self.set_button_icon(self.replay_button, "icon/replay.png", QSize(20, 20))
        self.set_button_icon(self.main_btn1, "icon/Логоав.png", QSize(20, 20))
        self.set_button_icon(self.play_button, "icon/play.png", QSize(20, 20))
        self.set_button_icon(self.forw_button, "icon/fast_forward.png", QSize(20, 20))
        self.set_button_icon(self.previous_button, "icon/skip_previous.png", QSize(20, 20))
        self.set_button_icon(self.pre_button, "icon/fast_rewind.png", QSize(20, 20))
        self.set_button_icon(self.search_btn, "icon/search.png", QSize(20, 20))
        self.set_button_icon(self.following_button, "icon/skip_next.png", QSize(20, 20))


    def set_button_icon(self, button, icon_path, icon_size):
        try:
            icon = QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(icon_size)
        except FileNotFoundError:
            logging.error(f"Файл иконки не найден: {icon_path}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить иконку: {icon_path}")

    # --- Длина песни и метаданные ---
    def get_song_length(self, filepath):
        try:
            audio = MP3(filepath)
            length = int(audio.info.length)
            self.duration_label_2.setText(self.format_time(length))
            self.duration_slider.setMaximum(length)
        except Exception as e:
            logging.exception(f"Ошибка при получении длины песни: {e}")
            self.duration_label_2.setText("Неизвестная продолжительность")
            self.duration_slider.setMaximum(0)
            QMessageBox.warning(self, "Error", f"Не удалось получить длину песни: {e}")

    def load_songs_from_db(self):
        try:
            songs = get_all_songs(db_path)
            self.playlist_widget.clear()
            for filepath, title, artist in songs:
                item = QtWidgets.QListWidgetItem(f"{title} - {artist}")
                item.setData(32, filepath)
                self.playlist_widget.addItem(item)
        except Exception as e:
            logging.exception(f"Ошибка загрузки песен из базы данных: {e}")
            QMessageBox.critical(self, "Ошибка базы данных", "Не удалось загрузить песни из базы данных.")


    # --- Управление воспроизведением ---
    def play_selected_song(self, item):
        filepath = item.data(32)
        self.play(filepath)
        self.playlist_widget.setCurrentItem(item)

    def play(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.current_song = filepath
            self.update_song_label(filepath)
            self.get_song_length(filepath)
            self.timer.start(1000)
            self.play_button.setIcon(QIcon("icon/pause.png"))
            self.is_paused = False
        except pygame.error as e:
            logging.exception(f"Ошибка воспроизведения песни Pygame: {e}")
            QMessageBox.critical(self, "Pygame Error", f"Ошибка воспроизведения песни: {e}")
        except Exception as e:
            logging.exception(f"Ошибка воспроизведения песни: {e}")
            QMessageBox.critical(self, "Error", f"Произошла ошибка: {e}")

    def toggle_play_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("icon/play.png"))
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.play_button.setIcon(QIcon("icon/pause.png"))
            self.is_paused = False

    def seek(self, seconds):
        if self.current_song:
            current_pos = pygame.mixer.music.get_pos() // 1000
            new_pos = max(0, min(current_pos + seconds, self.duration_slider.maximum())) # Удерживаем в пределах границ
            try:
                pygame.mixer.music.play(start=new_pos)
                self.duration_slider.setValue(new_pos)
                self.duration_label.setText(self.format_time(new_pos))
            except pygame.error as e:
                logging.exception(f"Ошибка перехода к позиции: {e}")
                QMessageBox.critical(self, "Pygame Error", f"Ошибка перехода к позиции: {e}")


    def slider_pressed(self):
        self.timer.stop() #Остановить обновление ползунка во время перетаскивания

    def slider_released(self):
        if self.current_song:
            position = self.duration_slider.value()
            self.seek(position) #Использовать seek для обработки изменения позиции, перезапуск таймера
            self.timer.start(1000)

    def mute(self):
        if self.muteF:
            self.set_button_icon(self.sound_button, "icon/volumeoff.png", QSize(20, 20))
            pygame.mixer.music.set_volume(0)
            self.muteF = False
        else:
            self.set_button_icon(self.sound_button, "icon/volumeup.png", QSize(20, 20))
            pygame.mixer.music.set_volume(self.volume_slider.value() / 100.0)
            self.muteF = True

    def replay(self):
        # Реализовать функционал повтора (воспроизведение текущей песни с начала)
        if self.current_song:
            self.play(self.current_song)

    def shuffle(self):
        # Реализовать функционал случайного воспроизведения
        pass

    def run(self):
        QMessageBox.information(self, "О проекте", "автор: Фролов Максим")
        QMessageBox.information(self, "О проекте", "https://github.com/maksim04021/MMM")

    def play_next_song(self):
          if len(self.playlist_filenames) > 0:
            current_index = self.playlist_filenames.index(self.current_song) if self.current_song else -1
            next_index = (current_index + 1) % len(self.playlist_filenames)
            self.play_song(next_index)

    def play_previous_song(self):
        if len(self.playlist_filenames) > 0:
            current_index = self.playlist_filenames.index(self.current_song) if self.current_song else 0
            prev_index = (current_index -1 ) % len(self.playlist_filenames)
            self.play_song(prev_index)
    
    def add_song_to_playlist(self, filepath):
        self.playlist_filenames = get_all_songs(db_path)
        
        item = QListWidgetItem(os.path.basename(filepath))
        self.playlist_widget.addItem(item)
        self.playlist.append(filepath)
        self.playlist_filenames.append(os.path.basename(filepath))


    
    def search_song(self):
        '''
        search_term = self.search_line_edit.text().lower()
        results = [song for song in self.playlist if search_term in song[1].lower() or search_term in song[2].lower()]
        self.playlist = results
        self.update_playlist_widget()
        '''

    # --- Форматирование времени ---
    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return "{:02d}:{:02d}".format(minutes, seconds)

    # --- Обновление ползунка длительности ---
    def update_duration_slider(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
            current_time = pygame.mixer.music.get_pos() // 1000
            self.duration_slider.setValue(current_time)
            self.duration_label.setText(self.format_time(current_time))
        elif not pygame.mixer.music.get_busy():
            self.timer.stop()

    # --- Регулировка громкости ---
    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100.0)

    # --- Добавление песни ---
    def add_song(self):
        file, _ = QFileDialog.getOpenFileName(parent=None, caption="Выбери песню",
                                              directory="c:",
                                              filter="music (*.mp3 *.wav)",
                                              initialFilter="music (*.mp3 *.wav)")
        if file:
            self.add_to_playlist(file)


    def add_to_playlist(self, file):
        song_metadata = self.get_song_metadata(file)
        if song_metadata:
            item = QtWidgets.QListWidgetItem(f"{song_metadata['title']} - {song_metadata['artist']}")
            item.setData(32, file)
            self.playlist_widget.addItem(item)

    def get_song_metadata(self, filepath):
        try:
            metadata = add_song_metadata(db_path, filepath)
            if metadata:
                return metadata
            else:
                return {'title': os.path.basename(filepath), 'artist': 'Unknown'}
        except Exception as e:
            logging.exception(f"Ошибка при получении метаданных: {e}")
            return {'title': os.path.basename(filepath), 'artist': 'Unknown'}

    def update_song_label(self, filepath):
        try:
            metadata = self.get_song_metadata(filepath)
            song_info = f"{metadata['title']} - {metadata['artist']}"
            self.song_label.setText(song_info)
        except Exception as e:
            logging.exception(f"Ошибка обновления метки песни: {e}")
            self.song_label.setText("Ошибка загрузки информации о песне.")

# --- Главное выполнение ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    signal_handler = SignalHandler()
    auth_window = Auth(signal_handler)
    main_window = Main()
    signal_handler.open_window2_signal.connect(main_window.show)
    auth_window.show()
    sys.exit(app.exec())
