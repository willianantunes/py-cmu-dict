import logging
import os
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from py_cmu_dict.apps.core.management.commands.exceps import MoreVariantsThanWhatIsSupportedException
from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.support.file_utils import each_line_from_file
from py_cmu_dict.support.file_utils import number_of_lines
from py_cmu_dict.support.text_utils import strip_left_and_right_sides

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database with CMU pronunciation dictionary"

    def add_arguments(self, parser):
        parser.add_argument("--cmu-file-location", type=str, help="Full path where CMU database file is")

    def handle(self, *args, **options):
        self.cmu_file_location = options["cmu_file_location"]

        number_of_entries = number_of_lines(self.cmu_file_location)
        self.stdout.write(f"Number of entries: {number_of_entries}")

        if number_of_entries <= Dictionary.objects.count():
            self.stdout.write("No need to fill the table!")
        else:
            self.stdout.write("Translating to DTOs...")
            dtos_generator = _translation_to_dtos(self.cmu_file_location)
            assert list(dtos_generator) == 3
            # for dtos in chunker(dto_generator, 1000):
            #     with transaction.atomic():
            #         UserJsmInEvoxTemp.objects.bulk_create(dtos, batch_size)
            # logger.info(f"Total entries created: {UserJsmInEvoxTemp.objects.count()}")

        # for user_in_evox in UserJsmInEvoxTemp.select():
        #     user_data = UserData.objects.filter(metadata__cpf=user_in_evox.cpf).first()
        #
        #     user_in_evox: UserJsmInEvox
        #     user_data: UserData
        #
        #     if user_data:
        #         logger.info("User in Ishtar Gate!")
        #         if user_data.user_id_ref == user_in_evox.id_ref:
        #             logger.info(f"User with ID REF {user_data.user_id_ref} is OK!")
        #         else:
        #             logger.info(
        #                 f"User with ID REF {user_data.user_id_ref} is buggy in our system. Updating it to {user_in_evox.id_ref}"
        #             )
        #             user_data.user_id_ref = user_in_evox.id_ref
        #             user_data.save()
        #     else:
        #         logger.info(f"User not found with ID ref from EVOX: {user_in_evox.id_ref}")

    #
    #
    # def _prepare_database_from_evox():
    #


#
#     if created_entities_in_evox == UserJsmInEvoxTemp.objects.count():
#         logger.info(f"No need to fill table from CSV")
#     else:
#         batch_size = int(os.getenv("TMP_DJ_BATCH_SIZE", 1000))
#         logger.info(f"Creating users from EVOX...")
#         dto_generator = _translation_to_dtos(file_users_jsm_in_evox)
#         for dtos in chunker(dto_generator, 1000):
#             with transaction.atomic():
#                 UserJsmInEvoxTemp.objects.bulk_create(dtos, batch_size)
#         logger.info(f"Total entries created: {UserJsmInEvoxTemp.objects.count()}")
#
#
def _translation_to_dtos(absolute_file_name):
    regex_for_variant = r"(\([0-9]\))"
    for line in each_line_from_file(absolute_file_name):
        cleaned_line = strip_left_and_right_sides(line.lower())
        word, phoneme = cleaned_line.split("  ")
        matches = list(re.finditer(regex_for_variant, word))

        if not matches:
            yield Dictionary(
                word_or_symbol=word, phoneme=phoneme, classification=Dictionary.WordClassification.UNDEFINED_1
            )
        else:
            match = matches[0]
            mark_that_was_matched = match.group()

            if "1" in mark_that_was_matched:
                classification = Dictionary.WordClassification.UNDEFINED_2
            elif "2" in mark_that_was_matched:
                classification = Dictionary.WordClassification.UNDEFINED_3
            elif "3" in mark_that_was_matched:
                classification = Dictionary.WordClassification.UNDEFINED_4
            else:
                raise MoreVariantsThanWhatIsSupportedException

            word_without_variant_number = word[0 : match.start()]

            yield Dictionary(word_or_symbol=word_without_variant_number, phoneme=phoneme, classification=classification)
