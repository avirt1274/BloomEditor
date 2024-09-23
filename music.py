from os import environ, listdir
from random import choice
from time import sleep
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# Инициализация pygame mixer
pygame.mixer.init()

# Папка с аудиофайлами
assets = 'assets/'

# Список файлов только с определенными расширениями
files = [f for f in listdir(assets) if f.endswith(('.mp3', '.wav'))]

# Проверка наличия файлов
if not files:
    # print("No audio files found!")
    pass
else:
    # print("Available files:", files)

    # Выбор случайного файла и его воспроизведение
    audio_file = choice(files)
    # print(f"Playing: {audio_file}")
    pygame.mixer.music.load(assets + audio_file)
    pygame.mixer.music.play()

    # Ожидание завершения воспроизведения
    while pygame.mixer.music.get_busy():
        sleep(1)  # Проверка каждую секунду
