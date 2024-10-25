from typing import Generator

from bs4 import BeautifulSoup

from interfaces import DictWordLink, DictWordSaveData


class GufoDictionaryPageParser:

    def __init__(self, domain: str, soup: BeautifulSoup):
        self.domain = domain
        self.soup = soup

    def parse_dict_words_links(self) -> Generator[DictWordLink, None, None]:
        words = self.soup.select('div.col-sm-12 > ul > li > a')
        for word in words:
            yield DictWordLink(f'{self.domain}{word["href"]}', word.text)

    @property
    def next_page_link(self) -> str | None:
        tag = self.soup.select_one('a[rel="next"]')
        if tag:
            return f'{self.domain}{tag["href"]}'


class GufoDictionaryDetailPageParser:

    def __init__(self, replace_link_base_url: str, soup: BeautifulSoup):
        self.replace_link_base_url = replace_link_base_url
        self.soup = soup

    def replace_word_url(self, word: str):
        return f'{self.replace_link_base_url}/{word}'

    def parse_word_description(self) -> DictWordSaveData:
        description_obj_parts = self.soup.select(
            '#dictionary-acticle article p span',
        )
        parts = []
        for tag in description_obj_parts:
            description_links = tag.find_all('a')
            text = tag.text
            for desc_link in description_links:
                text = text.replace(
                    desc_link.text,
                    str(desc_link).replace(
                        '/dict/psychologie_dict', self.replace_link_base_url
                    )
                )
            parts.append(text)
        description = '\n\n'.join(parts)
        word = self.soup.select_one('#dictionary-acticle h1').text
        return DictWordSaveData(
            self.replace_word_url(word), word, description
        )
