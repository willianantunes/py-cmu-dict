import logging

from dataclasses import dataclass
from typing import List
from typing import Optional

from django.db.models import QuerySet

from py_cmu_dict.apps.core.models import Dictionary

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Homophone:
    word_or_symbol: str
    phonemic = str
    phonetic = str


def discover_rhymes(word_or_symbol: str, language_tag: str) -> Optional[List[str]]:
    base_query_set = Dictionary.objects.filter(language__language_tag=language_tag)
    word_from_database = base_query_set.filter(word_or_symbol=word_or_symbol).first()

    if not word_from_database:
        logger.debug(f"No entry for {language_tag} / {word_or_symbol}")
        return
    else:
        word_from_database: Dictionary
        if not word_from_database.ipa_phonemic_syllables:
            logger.debug(f"No phonemic syllable available for {language_tag} / {word_or_symbol}")
            return
        else:
            if language_tag == "en-us":
                return _discover_rhymes_for_cmu(word_from_database, base_query_set)

            separator_mark = Dictionary.syllable_separator_mark
            syllables = word_from_database.ipa_phonemic_syllables.split(separator_mark)
            number_of_syllables = len(syllables)
            logger.debug(f"The word '{word_or_symbol}' has {number_of_syllables} syllables")
            query_set_syllables = base_query_set.exclude(pk=word_from_database.pk)

            if number_of_syllables == 1:
                syllable_available = syllables[0]
                return list(query_set_syllables.filter(ipa_phonetic__endswith=syllable_available))
            else:
                raise NotImplementedError


def _discover_rhymes_for_cmu(word_or_symbol: Dictionary, base_query_set: QuerySet) -> Optional[List[str]]:
    logger.debug("Using CMU ARPABET strategy")
    # Some important variables
    arpabet_stress_mark = "1"
    separator_mark = Dictionary.arpanet_phoneme_separator_mark
    phonemes = word_or_symbol.arpanet_phoneme.split(separator_mark)
    # First try
    phoneme_to_be_used = None
    for index, phoneme in enumerate(phonemes):
        if arpabet_stress_mark in phoneme:
            phoneme_to_be_used = separator_mark.join(phonemes[index:])
    # Then we should fallback to the common strategy
    if not phoneme_to_be_used:
        raise NotImplementedError
    # Otherwise, we can try!
    result = base_query_set.filter(arpanet_phoneme__endswith=phoneme_to_be_used)
    cleaned_result = [tuple_entry[0] for tuple_entry in result.values_list("word_or_symbol")]
    return cleaned_result


def discover_homophones(word: str) -> List[Homophone]:
    raise NotImplementedError
