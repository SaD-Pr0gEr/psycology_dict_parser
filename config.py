import os
from pathlib import Path


BASE_DIR = Path(__file__).parent
WORDS_DIR_PATH = BASE_DIR / 'dump'
DICT_LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
SITE_BASE_URL = 'https://gufo.me'
SITE_DICT_PAGE_URL = f'{SITE_BASE_URL}/dict/psychologie_dict'
REPLACE_WORD_URL = 'https://talentsy.ru/dictionary'


def load_dirs(*dirs):
    for dir_ in dirs:
        if not os.path.exists(dir_):
            os.makedirs(dir_)
