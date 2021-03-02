import uuid

from datetime import date
from decimal import Decimal

import pytest

from django.core.exceptions import ValidationError

# from tests.resouces.utils import create_rs
from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.apps.core.models import Phoneset
from tests.support.models_utils import create_dictionary
from tests.support.models_utils import create_phoneset


@pytest.mark.django_db
def test_should_create_dictionaries():
    word_1, word_2, word_3 = "to", "two", "too"

    d_1, d_2, d_3 = create_dictionary(word_1), create_dictionary(word_2), create_dictionary(word_3)

    assert d_1.word_or_symbol == word_1
    assert d_2.word_or_symbol == word_2
    assert d_3.word_or_symbol == word_3
    assert Dictionary.objects.count() == 3


@pytest.mark.django_db
def test_should_create_phonetics_with_their_dictionaries():
    word_1, word_2, word_3, word_4, word_5 = "to", "two", "too", "tree", "three"
    phonemic_1, phonemic_2, phonemic_3 = "tuː", "tɹiː", "θɹiː"

    d_1, d_2, d_3 = create_dictionary(word_1), create_dictionary(word_2), create_dictionary(word_3)
    phoneset_1 = create_phoneset(phonemic=phonemic_1)
    phoneset_1.words_or_symbols.add(d_1, d_2, d_3)

    assert d_1.transcription.count() == 1 and d_2.transcription.count() == 1 and d_3.transcription.count() == 1
    assert phoneset_1.words_or_symbols.count() == 3

    d_4, d_5 = create_dictionary(word_4), create_dictionary(word_5)
    phoneset_2, phoneset_3 = create_phoneset(phonemic=phonemic_2), create_phoneset(phonemic=phonemic_3)
    phoneset_2.words_or_symbols.add(d_4)
    phoneset_3.words_or_symbols.add(d_5)

    assert d_4.transcription.count() == 1 and d_5.transcription.count() == 1
    assert phoneset_2.words_or_symbols.count() == 1
    assert phoneset_3.words_or_symbols.count() == 1

    assert Dictionary.objects.count() == 5
    assert Phoneset.objects.count() == 3


#
# @pytest.mark.django_db
# def test_should_accept_exactly_one_of_rs_or_group_for_goal():
#     rs = create_rs(id=uuid.uuid4(), cnpj="00472619000107")
#     group = create_grp(name="XPTO")
#
#     data_with_rs_and_group = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": "2019-01-01",
#         "end_at": "2019-01-15",
#         "points": "10.0000",
#         "retail_store": rs,
#         "group": group,
#     }
#     data_with_rs_only = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": "2019-01-01",
#         "end_at": "2019-01-15",
#         "points": "10.0000",
#         "retail_store": rs,
#     }
#     data_with_group_only = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": "2019-01-01",
#         "end_at": "2019-01-15",
#         "points": "10.0000",
#         "group": group,
#     }
#     data_without_rs_and_group = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": "2019-01-01",
#         "end_at": "2019-01-15",
#         "points": "10.0000",
#     }
#
#     message_validation_error = "Exactly one of RETAIL STORE or GROUP must be set."
#
#     with pytest.raises(ValidationError) as e_form_with_rs_and_group:
#         Goal.objects.create(**data_with_rs_and_group)
#     assert e_form_with_rs_and_group.value.messages[0] == message_validation_error
#
#     Goal.objects.create(**data_with_rs_only)
#     Goal.objects.create(**data_with_group_only)
#
#     with pytest.raises(ValidationError) as e_form_with_rs_and_group:
#         Goal.objects.create(**data_without_rs_and_group)
#     assert e_form_with_rs_and_group.value.messages[0] == message_validation_error
#
#
# @pytest.mark.django_db
# def test_should_save_only_unique_goals_scenario_1():
#     reference_date = date.today()
#     first_day, last_day = get_first_day(reference_date), get_last_day(reference_date)
#     rs_1 = create_rs()
#
#     configured_goal = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": first_day,
#         "end_at": last_day,
#         "points": Decimal("10.0000"),
#         "retail_store_id": rs_1.id,
#     }
#
#     Goal.objects.create(**configured_goal)
#     with pytest.raises(ValidationError) as e:
#         Goal.objects.create(**configured_goal)
#     assert "already exists" in e.value.messages[0]
#
#
# @pytest.mark.django_db
# def test_should_save_only_unique_goals_scenario_2():
#     reference_date = date.today()
#     first_day, last_day = get_first_day(reference_date), get_last_day(reference_date)
#     grp_1 = create_grp()
#
#     configured_goal = {
#         "id_company_ref": uuid.uuid4(),
#          "start_at": first_day,
#         "end_at": last_day,
#         "points": Decimal("10.0000"),
#         "group_id": grp_1.id,
#     }
#
#     Goal.objects.create(**configured_goal)
#     with pytest.raises(ValidationError) as e:
#         Goal.objects.create(**configured_goal)
#     assert "already exists" in e.value.messages[0]
#
#
# @pytest.mark.django_db
# def test_should_save_only_unique_goals_scenario_3():
#     reference_date = date.today()
#     first_day, last_day = get_first_day(reference_date), get_last_day(reference_date)
#     rs_1, grp_1 = create_rs(), create_grp()
#
#     configured_goal = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": first_day,
#         "end_at": last_day,
#         "points": Decimal("10.0000"),
#         "retail_store_id": rs_1.id,
#         "group_id": grp_1.id,
#     }
#
#     with pytest.raises(ValidationError) as e:
#         Goal.objects.create(**configured_goal)
#     assert e.value.messages[0] == "Exactly one of RETAIL STORE or GROUP must be set."
#
#
# @pytest.mark.django_db
# def test_should_save_only_unique_goals_scenario_4():
#     reference_date = date.today()
#     first_day, last_day = get_first_day(reference_date), get_last_day(reference_date)
#     rs_1 = create_rs()
#
#     configured_goal = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": first_day,
#         "end_at": last_day,
#         "points": Decimal("10.0000"),
#         "retail_store_id": rs_1.id,
#     }
#
#     Goal.objects.create(**configured_goal)
#     configured_goal["id_company_ref"] = uuid.uuid4()
#     Goal.objects.create(**configured_goal)
#     configured_goal["id_company_ref"] = uuid.uuid4()
#     Goal.objects.create(**configured_goal)
#     with pytest.raises(ValidationError) as e:
#         Goal.objects.create(**configured_goal)
#     assert "already exists" in e.value.messages[0]
#
#
# @pytest.mark.django_db
# def test_should_save_only_unique_goals_scenario_5():
#     reference_date = date.today()
#     first_day, last_day = get_first_day(reference_date), get_last_day(reference_date)
#     grp_1 = create_grp()
#
#     configured_goal = {
#         "id_company_ref": uuid.uuid4(),
#         "start_at": first_day,
#         "end_at": last_day,
#         "points": Decimal("10.0000"),
#         "group_id": grp_1.id,
#     }
#
#     Goal.objects.create(**configured_goal)
#     configured_goal["id_company_ref"] = uuid.uuid4()
#     Goal.objects.create(**configured_goal)
#     configured_goal["id_company_ref"] = uuid.uuid4()
#     Goal.objects.create(**configured_goal)
#     with pytest.raises(ValidationError) as e:
#         Goal.objects.create(**configured_goal)
#     assert "already exists" in e.value.messages[0]
