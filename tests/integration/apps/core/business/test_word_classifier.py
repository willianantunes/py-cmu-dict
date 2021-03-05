import pytest

from django.core.management import call_command

from py_cmu_dict.apps.core.business.word_classifier import discover_homophones
from py_cmu_dict.apps.core.business.word_classifier import discover_rhymes
from tests.resources.resource_loader import resource_location


@pytest.fixture(autouse=True)
def create_database(mocker):
    mocker.patch("py_cmu_dict.settings.DJANGO_BULK_BATCH_SIZE", 20_000)
    cmu_file_location = resource_location("cmudict-0.7b.txt")
    call_command("seed", "--cmu-file-location", cmu_file_location)


@pytest.mark.django_db
def test_should_return_rhymes_from_word_function():
    word_to_be_analysed = "function"

    rhymes = discover_rhymes(word_to_be_analysed)

    assert rhymes == ["compunction", "conjunction", "dysfunction", "injunction", "junction", "malfunction"]


@pytest.mark.django_db
def test_should_return_rhymes_from_word_rhyming():
    word_to_be_analysed = "rhyming"

    rhymes = discover_rhymes(word_to_be_analysed)

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
