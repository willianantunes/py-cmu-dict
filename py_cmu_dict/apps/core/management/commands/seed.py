import logging

from typing import Generator

from django.core.management.base import BaseCommand
from django.db import transaction

from py_cmu_dict import settings
from py_cmu_dict.apps.core.business.CMUDatabaseHandler import CMUDatabaseHandler
from py_cmu_dict.apps.core.business.CMUDatabaseHandler import CMULine
from py_cmu_dict.apps.core.business.CMUDatabaseHandler import Variant
from py_cmu_dict.apps.core.business.InternationalPhoneticAlphabet import InternationalPhoneticAlphabet
from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.apps.core.models import Language
from py_cmu_dict.support.iter_utils import chunker

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database with CMU pronunciation dictionary"

    def add_arguments(self, parser):
        parser.add_argument("--cmu-file-location", type=str, help="Full path where CMU database file is")

    def handle(self, *args, **options):
        self.cmu_file_location = options["cmu_file_location"]

        carnegie_mellon_university_database = CMUDatabaseHandler(self.cmu_file_location)
        number_of_entries = carnegie_mellon_university_database.number_of_valid_entries
        self.stdout.write(f"Number of entries: {number_of_entries}")

        if number_of_entries <= Dictionary.objects.count():
            self.stdout.write("No need to fill the table!")
        else:
            batch_size = getattr(settings, "DJANGO_BULK_BATCH_SIZE")
            language_model, created = Language.objects.get_or_create(language_tag="en-us")
            self.stdout.write(f"Was {language_model.language_tag} created? {created}")

            self.stdout.write("Initializing database handler and generators...")
            cmu_line_generator = carnegie_mellon_university_database.retrieve_cmu_lines()
            dtos_generator = _translation_to_dtos(cmu_line_generator, language_model)

            self.stdout.write("All done! Let's go...")
            saved_data = 0
            for dtos in chunker(dtos_generator, batch_size):
                with transaction.atomic():
                    Dictionary.objects.bulk_create(dtos, batch_size)
                saved_data += batch_size
                if saved_data % 20_000 == 0:
                    logger.info(f"Entries saved: {Dictionary.objects.count()}")

            logger.info(f"Total entries created: {Dictionary.objects.count()}")


def _translation_to_dtos(cmu_line_generator: Generator[CMULine, None, None], language: Language):
    for cmu_line in cmu_line_generator:
        phonemes_as_ipa_symbols = InternationalPhoneticAlphabet.ipa_format_from_arpanet(cmu_line.phonemes)

        if cmu_line.variant == Variant.V1:
            version = Dictionary.Version.V_1
        elif cmu_line.variant == Variant.V2:
            version = Dictionary.Version.V_2
        elif cmu_line.variant == Variant.V3:
            version = Dictionary.Version.V_3
        else:
            version = Dictionary.Version.V_4

        # Better to join without spaces
        phonemic = "".join(phonemes_as_ipa_symbols)
        # Better to leave with spaces
        phoneme = " ".join(cmu_line.phonemes)

        yield Dictionary(
            word_or_symbol=cmu_line.word_or_symbol,
            phoneme=phoneme,
            phonemic=phonemic,
            version=version,
            language=language,
        )
