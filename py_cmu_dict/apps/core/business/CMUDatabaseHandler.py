import re

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Generator

from py_cmu_dict.apps.core.business.exceps import DatabaseFileNotAvailable
from py_cmu_dict.apps.core.business.exceps import MoreVariantsThanWhatIsSupportedException
from py_cmu_dict.support.file_utils import each_line_from_file
from py_cmu_dict.support.text_utils import strip_left_and_right_sides


class Variant(Enum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4


@dataclass(frozen=True)
class CMULine:
    word_or_symbol: str
    phoneme: str
    variant: Variant


# https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary
class CMUDatabaseHandler:
    regex_for_variant = r"(\([0-9]\))"

    def __init__(self, database_file_location):
        path = Path(database_file_location)
        if not (path.exists() and path.is_file()):
            raise DatabaseFileNotAvailable
        self.database_file_location = database_file_location

    @classmethod
    def extract_data(cls, raw_line: str) -> CMULine:
        cleaned_line = strip_left_and_right_sides(raw_line.lower())
        word_or_symbol, phoneme = cleaned_line.split("  ")
        matches = list(re.finditer(cls.regex_for_variant, word_or_symbol))

        if not matches:
            return CMULine(word_or_symbol, phoneme, Variant.V1)
        else:
            match = matches[0]
            mark_that_was_matched = match.group()

            if "1" in mark_that_was_matched:
                variant_found = Variant.V2
            elif "2" in mark_that_was_matched:
                variant_found = Variant.V3
            elif "3" in mark_that_was_matched:
                variant_found = Variant.V4
            else:
                raise MoreVariantsThanWhatIsSupportedException

            word_or_symbol_without_variant_number = word_or_symbol[0 : match.start()]

            return CMULine(word_or_symbol_without_variant_number, phoneme, variant_found)

    def retrieve_lines(self) -> Generator[CMULine, None, None]:
        for line in each_line_from_file(self.database_file_location):
            # Only words are supported for now. Symbols maybe in the future...
            if not re.match("^[a-zA-Z]", line):
                continue
            yield self.extract_data(line)
