import pytest

from django.core.management import CommandError
from django.core.management import call_command

from tests.resources.resource_loader import resource_location


def test_should_raise_error_given_no_argument_was_provided_for_cmu_file_location_option():
    with pytest.raises(CommandError) as e:
        call_command("seed", "--cmu-file-location")

    assert e.value.args[0] == "Error: argument --cmu-file-location: expected one argument"


@pytest.mark.django_db
def test_should_create_database():
    cmu_file_location = resource_location("sample-part-cmudict-0.7b.txt")

    call_command("seed", "--cmu-file-location", cmu_file_location)
