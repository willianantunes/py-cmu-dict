import pytest

from django.core.management import CommandError
from django.core.management import call_command

from py_cmu_dict.apps.core.models import Dictionary
from tests.resources.resource_loader import resource_location


def test_should_raise_error_given_no_argument_was_provided_for_cmu_file_location_option():
    with pytest.raises(CommandError) as e:
        call_command("seed", "--cmu-file-location")

    assert e.value.args[0] == "Error: argument --cmu-file-location: expected one argument"


@pytest.mark.django_db
def test_should_create_database_with_sample_part():
    cmu_file_location = resource_location("sample-part-1-cmudict-0.7b.txt")

    call_command("seed", "--cmu-file-location", cmu_file_location)

    assert Dictionary.objects.count() == 74

    abandoned_dict_entry = Dictionary.objects.get(word_or_symbol="abandoned")

    assert abandoned_dict_entry.phoneme == "ah0bae1ndah0nd"
    assert abandoned_dict_entry.phonemic == "əˈbændənd"
    assert abandoned_dict_entry.phonetic is None
    assert abandoned_dict_entry.classification == Dictionary.WordClassification.UNDEFINED
    assert abandoned_dict_entry.version == Dictionary.Version.V_1


@pytest.mark.django_db
def test_should_create_database_with_entire_cmu_pronunciation_dictionary():
    cmu_file_location = resource_location("cmudict-0.7b.txt")

    call_command("seed", "--cmu-file-location", cmu_file_location)

    number_of_current_lines = 134429
    invalid_header_lines = 126
    invalid_footer_lines = 5
    correct_count_of_valid_lines = number_of_current_lines - invalid_header_lines - invalid_footer_lines

    assert Dictionary.objects.count() == correct_count_of_valid_lines
