import json
import time
from dataclasses import asdict

import requests
from bs4 import BeautifulSoup

from config import (
    SITE_DICT_PAGE_URL, DICT_LETTERS, SITE_BASE_URL, REPLACE_WORD_URL,
    WORDS_DIR_PATH, load_dirs
)
from parser import GufoDictionaryPageParser, GufoDictionaryDetailPageParser


def main():
    load_dirs(WORDS_DIR_PATH)
    for letter in DICT_LETTERS:
        response = requests.get(
            f'{SITE_DICT_PAGE_URL}',
            params={'letter': letter},
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        soup = BeautifulSoup(response.text, 'lxml')
        parser = GufoDictionaryPageParser(SITE_BASE_URL, soup)
        words = list(parser.parse_dict_words_links())
        next_page = parser.next_page_link
        while next_page:
            response = requests.get(
                next_page, headers={'User-Agent': 'Mozilla/5.0'}
            )
            soup = BeautifulSoup(response.text, 'lxml')
            parser.soup = soup
            for word in parser.parse_dict_words_links():
                words.append(word)
            next_page = parser.next_page_link
        words_save_list = []
        for word in words:
            response = requests.get(
                word.link, headers={'User-Agent': 'Mozilla/5.0'}
            )
            soup = BeautifulSoup(response.text, 'lxml')
            parser = GufoDictionaryDetailPageParser(REPLACE_WORD_URL, soup)
            description = parser.parse_word_description()
            words_save_list.append(asdict(description))
            time.sleep(.5)
        with open(WORDS_DIR_PATH / f'{letter}.json', 'w') as file:
            json.dump(words_save_list, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
