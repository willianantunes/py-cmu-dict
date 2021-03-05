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

            return _discover_rhymes_standard_way(word_from_database, base_query_set)


def _discover_rhymes_standard_way(word_or_symbol: Dictionary, base_query_set: QuerySet) -> Optional[List[str]]:
    logger.debug("Discovering rhymes through STANDARD strategy by syllable...")
    syllables = word_or_symbol.transform_ipa_syllable_entry_to_object()
    number_of_syllables = len(syllables)
    logger.debug(f"The word '{word_or_symbol}' has {number_of_syllables} syllables")
    query_set_syllables = base_query_set.exclude(pk=word_or_symbol.pk)

    # Naive implementation!
    # For certain there is something more technical in terms of linguistics...
    if number_of_syllables == 1:
        syllables_to_be_used = syllables[0]
    else:
        # Maybe only get the last syllable? Long words might bring problem...
        syllables_to_be_used = syllables[1::]

    syllables_to_consult_in_database = Dictionary.create_syllable_entry_ipa(syllables_to_be_used)
    result = query_set_syllables.filter(ipa_phonemic__endswith=syllables_to_consult_in_database)
    cleaned_result = [tuple_entry[0] for tuple_entry in result.values_list("word_or_symbol")]
    logger.debug(f"Total rhymes words found: {len(cleaned_result)}")

    return cleaned_result


def _discover_rhymes_for_cmu(word_or_symbol: Dictionary, base_query_set: QuerySet) -> Optional[List[str]]:
    logger.debug("Discovering rhymes through ARPABET strategy")
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
        return _discover_rhymes_standard_way(word_or_symbol, base_query_set)
    # Otherwise, we can try!
    result = base_query_set.filter(arpanet_phoneme__endswith=phoneme_to_be_used)
    cleaned_result = [tuple_entry[0] for tuple_entry in result.values_list("word_or_symbol")]
    return cleaned_result


def discover_homophones(word: str) -> List[Homophone]:
    raise NotImplementedError
