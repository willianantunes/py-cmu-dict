import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Dictionary(StandardModelMixin):
    # https://en.wikipedia.org/wiki/Longest_word_in_English
    # Sample word: Pneumonoultramicroscopicsilicovolcanoconiosis
    word_or_symbol = models.CharField(max_length=45, unique=True)


class Phoneset(StandardModelMixin):
    words_or_symbols = models.ManyToManyField(Dictionary, related_name="transcription")
    # See more in docs/NLPA-Phon1.pdf
    phoneme = models.CharField(max_length=100, null=True, blank=True)
    # Phonemic is the hypothetical sounds and phonetics is the actual production of them
    phonemic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Phonemic transcription")
    phonetic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Phonetic transcription")
