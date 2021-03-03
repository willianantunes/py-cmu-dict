from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.apps.core.models import Language


def create_dictionary(
    word_or_symbol,
    language,
    phoneme=None,
    phonemic=None,
    phonetic=None,
    classification=Dictionary.WordClassification.UNDEFINED,
    version=Dictionary.Version.V_1,
):
    return Dictionary.objects.create(
        word_or_symbol=word_or_symbol,
        classification=classification,
        version=version,
        phoneme=phoneme,
        phonemic=phonemic,
        phonetic=phonetic,
        language=language,
    )


def create_language(name):
    return Language.objects.create(name=name)
