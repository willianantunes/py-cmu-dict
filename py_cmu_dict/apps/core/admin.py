from django.contrib import admin

from py_cmu_dict.apps.core.models import Dictionary
from py_cmu_dict.apps.core.models import Language
from py_cmu_dict.support.django_helpers import CustomModelAdminMixin


@admin.register(Language)
class LanguageAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Dictionary)
class DictionaryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["word_or_symbol"]
    list_filter = [
        "version",
        "classification",
        "language__language_tag",
    ]
