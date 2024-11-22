# M Музыка

# Идея:
Аудио проигрыватель.
Я хочу создать аудио проигрыватель для более удобной работы с аудио файлами разбросанными по всему компьютеру.
Программа будет запоминать пути к аудио, будет удобный поиск по названию файлов, регулировка громкости, разделение на плейлисты.

# Тех. Задание:
1. Цель:
Разработка аудиоплеера с графическим интерфейсом на основе библиотеки PyQt, предоставляющего пользователю возможности выбора треков из коллекций, поиска по названию и управления воспроизведением.


2. Функциональные требования:

• Выбор трека из коллекций:

    * Плеер должен поддерживать организацию аудиофайлов в коллекции (возможно, несколько коллекций). Коллекции должны быть отображаемы в удобном для пользователя виде (например, список, дерево).
    
    * Пользователь должен иметь возможность выбирать отдельные треки из любой коллекции для воспроизведения.
    
    * Поддерживаемые форматы аудиофайлов: MP3, WAV (возможно расширение списка).
    
    * При выборе трека его название должно отображаться в интерфейсе плеера.
    
    * При изменении коллекции необходимо обновить список доступных треков.

• Поиск по названию:

    * Плеер должен иметь строку поиска, позволяющую пользователю искать треки по их названиям.
    
    * Поиск должен быть нечувствительным к регистру.
    
    * Результаты поиска должны отображаться в отдельном списке или обновлять основной список треков.
• Функциональные кнопки управления:

    * Кнопки "Play" (Воспроизведение), "Pause" (Пауза), "Stop" (Остановить), "Previous" (Предыдущий трек), "Next" (Следующий трек).
    
    * Кнопка регулировки громкости (slider).
    
    * Индикатор текущего времени воспроизведения и общей длительности трека.
    
    * Индикатор прогресса воспроизведения (progress bar).
• Обработка ошибок:

    * Плеер должен корректно обрабатывать ситуации, когда выбранный файл не существует, не является аудиофайлом или не поддерживается. В таких случаях должно выводиться соответствующее сообщение об ошибке.


3. Нефункциональные требования:

   • Платформа: Windows.

   • Интерфейс: Интуитивно понятный и удобный в использовании графический интерфейс.

   • Производительность: Быстрая загрузка и воспроизведение аудиофайлов.

   • Надежность: Стабильная работа без сбоев и зависаний.

   • Удобство использования: Простой и удобный интерфейс.

   • Эргономика: Размеры окна и расположение элементов должны обеспечивать комфортное использование.

   • Внешний вид: Современный и привлекательный внешний вид.


4. Архитектура:

   • Модель: Хранение данных о коллекциях и треках. Загрузка метаданных аудиофайлов (название, длительность).

   • Вид: Графический интерфейс пользователя (PyQt).

   • Контроллер: Обработка событий пользователя, управление воспроизведением, взаимодействие с моделью и видом.


5. Технологический стек:

   • Язык программирования: Python
   
   • Библиотека GUI: PyQt6

   • Библиотека для воспроизведения аудио: Playsound, PyAudio, Qt Multimedia (или подобная)


6. Тестирование:

   Необходимо провести модульное и интеграционное тестирование всех компонентов аудиоплеера. Тестирование должно включать проверку корректной работы всех функций, обработку ошибок и производительность.

7. Документация:

   К проекту должна быть предоставлена краткая документация, описывающая архитектуру приложения, инструкции по установке.


8. Декомпозиция:

   Проект можно разделить на следующие модули:

      • Модуль коллекций: Загрузка и управление коллекциями аудиофайлов.
   
      • Модуль поиска: Реализация поиска по названию трека.
   
      • Модуль воспроизведения: Управление воспроизведением аудиофайлов (Playsound или подобная библиотека).
   
      • Модуль интерфейса: Создание графического интерфейса на PyQt.


# Обновление 22.11.2024

Добавлено хэширование для упрощения поиска ошибок и дальнейшего исправления

Добавлено основное окно плеера

Добавлено хэширование паролей пользователей

Добавлено оповещение об ошибках* 

   *Вид ошибки(https://github.com/user-attachments/assets/e573ebc4-fe22-4c34-8d1d-defac2db2567)
