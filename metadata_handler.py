import logging
import sqlite3
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

db_path = 'music_database.db'  # Путь к вашей базе данных

def add_song_metadata(db_path, filepath):
    """Добавляет песню в базу данных, извлекая метаданные."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Проверяем, существует ли уже песня в базе данных
        cursor.execute("SELECT COUNT(*) FROM songs WHERE filepath = ?", (filepath,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return None  # Песня уже в базе

        # Извлекаем метаданные
        try:
            audio = MP3(filepath, ID3=EasyID3)
            title = audio.get("title", [os.path.basename(filepath)])[0]
            artist = audio.get("artist", ["Неизвестный исполнитель"])[0]
        except Exception as e:
            print(f"Ошибка извлечения метаданных для {filepath}: {e}")
            title = os.path.basename(filepath)
            artist = "Неизвестный исполнитель"

        # Добавляем песню в базу данных
        cursor.execute("INSERT INTO songs (filepath, title, artist) VALUES (?, ?, ?)", (filepath, title, artist))
        conn.commit()
        conn.close()
        return {'title': title, 'artist': artist}

    except Exception as e:
        print(f"Ошибка добавления песни в базу данных: {e}")
        conn.rollback()
        conn.close()
        return None

def get_songs_by_search_term(db_path, search_term):
    """
    Searches the songs database for songs matching the search term.

    Args:
        db_path: Path to the SQLite database file.
        search_term: The term to search for (case-insensitive).

    Returns:
        A list of tuples, where each tuple contains (filepath, title, artist).
        Returns an empty list if no matches are found or if there's a database error.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Case-insensitive search using LIKE
        cursor.execute("""
            SELECT filepath, title, artist 
            FROM songs 
            WHERE title LIKE ? OR artist LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%"))

        songs = cursor.fetchall()
        conn.close()
        return songs
    except sqlite3.Error as e:
        logging.exception(f"Ошибка базы данных при поиске: {e}")
        return []  # Return empty list on error
    except Exception as e:
        logging.exception(f"Unexpected error during search: {e}")
        return []

def get_all_songs(db_path):
    """Возвращает список всех песен из базы данных."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT filepath, title, artist FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return songs