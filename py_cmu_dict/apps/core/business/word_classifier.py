from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Homophone:
    word_or_symbol: str
    phonemic = str
    phonetic = str


def discover_rhymes(word: str) -> List[str]:
    raise NotImplementedError


def discover_homophones(word: str) -> List[Homophone]:
    raise NotImplementedError
