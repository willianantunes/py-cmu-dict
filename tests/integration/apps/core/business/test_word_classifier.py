import pytest

from django.core.management import call_command

from py_cmu_dict.apps.core.business.word_classifier import discover_homophones
from py_cmu_dict.apps.core.business.word_classifier import discover_rhymes
from tests.resources.resource_loader import resource_location


@pytest.fixture
def create_database_rhymes_1():
    cmu_file_location = resource_location("sample-part-rhymes-1-cmudict-0.7b.txt")
    call_command("seed", "--cmu-file-location", cmu_file_location)


@pytest.fixture
def create_database_rhymes_2():
    cmu_file_location = resource_location("sample-part-rhymes-2-cmudict-0.7b.txt")
    # Using EN-GB just to force not using CMU logic. See word_classifier.py to understand more
    call_command("seed", "--cmu-file-location", cmu_file_location, "--use-language-tag", "en-gb")


@pytest.fixture
def create_database_rhymes_3():
    cmu_file_location = resource_location("sample-part-rhymes-3-cmudict-0.7b.txt")
    # Using EN-GB just to force not using CMU logic. See word_classifier.py to understand more
    call_command("seed", "--cmu-file-location", cmu_file_location, "--use-language-tag", "en-gb")


@pytest.fixture
def create_database_homophones_1():
    cmu_file_location = resource_location("sample-part-homophones-1-cmudict-0.7b.txt")
    call_command("seed", "--cmu-file-location", cmu_file_location)


@pytest.fixture
def create_database_homophones_2():
    cmu_file_location = resource_location("sample-part-homophones-2-cmudict-0.7b.txt")
    call_command("seed", "--cmu-file-location", cmu_file_location)


@pytest.mark.django_db
def test_should_return_rhymes_from_word_sold_with_cmu(create_database_rhymes_1):
    word_to_be_analysed, language_tag = "sold", "en-us"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["strolled", "told", "uncontrolled"]


@pytest.mark.django_db
def test_should_return_rhymes_from_word_function_without_cmu(create_database_rhymes_2):
    word_to_be_analysed, language_tag = "function", "en-gb"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["compunction", "conjunction", "dysfunction", "injunction", "junction", "sanction", "malfunction"]


@pytest.mark.django_db
def test_should_return_rhymes_from_word_rhyming_without_cmu(create_database_rhymes_3):
    word_to_be_analysed, language_tag = "rhyming", "en-gb"

    rhymes = discover_rhymes(word_to_be_analysed, language_tag)

    assert rhymes == ["roaming", "rooming", "climbing", "diming", "liming", "priming", "scheming", "timing"]


@pytest.mark.django_db
def test_should_return_homophones_from_word_their(create_database_homophones_1):
    word_to_be_analysed, language_tag = "their", "en-us"

    homophones = discover_homophones(word_to_be_analysed, language_tag)

    assert len(homophones) == 2
    homophone_1 = homophones[0]
    homophone_2 = homophones[1]
    assert homophone_1.word_or_symbol == "there"
    assert homophone_1.phonemic == "ð ɛ ɹ"
    assert homophone_2.word_or_symbol == "they're"
    assert homophone_2.phonemic == "ð ɛ ɹ"


@pytest.mark.django_db
def test_should_return_homophones_from_word_eight(create_database_homophones_2):
    word_to_be_analysed, language_tag = "eight", "en-us"

    homophones = discover_homophones(word_to_be_analysed, language_tag)

    assert len(homophones) == 2
    homophone_1 = homophones[0]
    homophone_2 = homophones[1]
    assert homophone_1.word_or_symbol == "ate"
    assert homophone_1.phonemic == "eɪ t"
    assert homophone_2.word_or_symbol == "aydt"
    assert homophone_2.phonemic == "eɪ t"
