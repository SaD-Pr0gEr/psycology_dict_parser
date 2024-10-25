from dataclasses import dataclass


@dataclass
class DictWordLink:
    link: str
    word: str


@dataclass
class DictWordSaveData(DictWordLink):
    description: str
