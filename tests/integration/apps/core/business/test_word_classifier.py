import pytest

from django.core.management import call_command

from py_cmu_dict.apps.core.business.word_classifier import discover_homophones
from py_cmu_dict.apps.core.business.word_classifier import discover_rhymes
from tests.resources.resource_loader import resource_location


@pytest.fixture
def create_database_rhymes_1():
    cmu_file_location = resource_location("sample-part-rhymes-1-cmudict-0.7b.txt")
    call_command("seed", "--cmu-file-location", cmu_file_location)


@pytest.mark.django_db
def test_should_return_rhymes_from_word_sold_with_cmu(create_database_rhymes_1):
    word_to_be_analysed, language_tag = "sold", "en-us"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["sold", "strolled", "told", "uncontrolled"]


@pytest.mark.django_db
def test_should_return_rhymes_from_word_function_without_cmu():
    word_to_be_analysed, language_tag = "function", "en-us"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["compunction", "conjunction", "dysfunction", "injunction", "junction", "malfunction"]


@pytest.mark.django_db
def test_should_return_rhymes_from_word_rhyming_without_cmu():
    word_to_be_analysed, language_tag = "rhyming", "en-us"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["climbing", "diming", "liming", "priming", "timing"]


def test_should_return_homophones_from_word_their():
    word_to_be_analysed = "their"

    homophones = discover_homophones(word_to_be_analysed)

    assert len(homophones) == 2
    homophone_1 = homophones[0]
    homophone_2 = homophones[1]
    assert homophone_1.word_or_symbol == "there"
    assert homophone_1.phonemic == "ðɛr"
    assert homophone_2.word_or_symbol == "they're"
    assert homophone_2.phonemic == "ðɛr"
