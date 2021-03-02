import uuid

from django.db import models


class StandardModelMixin(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Language(StandardModelMixin):
    # https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md
    # One example that might be applicable: en-gb-scotland
    name = models.CharField(max_length=20, null=True, blank=True)


class Dictionary(StandardModelMixin):
    class WordClassification(models.TextChoices):
        NOUN = "NOUN", "Noun"
        PRONOUN = "PRONOUN", "Pronoun"
        ADJECTIVE = "ADJECTIVE", "Adjectives"
        VERB = "VERB", "Verb"
        ADVERB = "ADVERB", "Adverbs"
        PREPOSITION = "PREPOSITION", "Preposition"
        CONJUNCTION = "CONJUNCTION", "Conjunction"
        INTERJECTION = "INTERJECTION", "Interjection"
        SYMBOL = "SYMBOL", "Symbol"
        UNDEFINED = "UNDEFINED", "Undefined"

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="dictionary_entries")
    classification = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        choices=WordClassification.choices,
        default=WordClassification.UNDEFINED,
    )
    # https://en.wikipedia.org/wiki/Longest_word_in_English
    # Sample word: Pneumonoultramicroscopicsilicovolcanoconiosis
    word_or_symbol = models.CharField(max_length=45, unique=True, null=False, blank=False)
    # See more in docs/NLPA-Phon1.pdf
    phoneme = models.CharField(max_length=100, null=True, blank=True)
    # Phonemic is the hypothetical sounds and phonetics is the actual production of them
    phonemic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Phonemic transcription")
    phonetic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Phonetic transcription")
