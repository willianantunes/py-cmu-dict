from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.apps.core.models import Phoneset


def create_dictionary(word_or_symbol):
    return Dictionary.objects.create(word_or_symbol=word_or_symbol)


def create_phoneset(phoneme=None, phonemic=None, phonetic=None):
    return Phoneset.objects.create(phoneme=phoneme, phonemic=phonemic, phonetic=phonetic)
