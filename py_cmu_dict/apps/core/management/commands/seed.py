import logging
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from py_cmu_dict.apps.core.business.CMUDatabaseHandler import CMUDatabaseHandler
from py_cmu_dict.apps.core.business.CMUDatabaseHandler import Variant
from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.support.file_utils import number_of_lines
from py_cmu_dict.support.iter_utils import chunker

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
            batch_size = int(os.getenv("DJANGO_BULK_BATCH_SIZE", 1000))
            self.stdout.write("Translating to DTOs...")
            carnegie_mellon_university_database = CMUDatabaseHandler(self.cmu_file_location)
            cmu_line_generator = carnegie_mellon_university_database.retrieve_lines()
            dtos_generator = _translation_to_dtos(cmu_line_generator)
            for dtos in chunker(dtos_generator, batch_size):
                with transaction.atomic():
                    Dictionary.objects.bulk_create(dtos, batch_size)
            logger.info(f"Total entries created: {Dictionary.objects.count()}")


def _translation_to_dtos(cmu_line_generator):
    for cmu_line in cmu_line_generator:
        if cmu_line.variant == Variant.V1:
            version = Dictionary.Version.V_1
        elif cmu_line.variant == Variant.V2:
            version = Dictionary.Version.V_2
        elif cmu_line.variant == Variant.V3:
            version = Dictionary.Version.V_3
        else:
            version = Dictionary.Version.V_4
        yield Dictionary(word_or_symbol=cmu_line.word_or_symbol, phoneme=cmu_line.phoneme, version=version)
