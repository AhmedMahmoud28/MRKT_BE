from modeltranslation.translator import TranslationOptions, translator

from .models import Store, StoreCategory


class StoreTranslationOptions(TranslationOptions):
    fields = ("name",)
    # required_languages = ('en', 'ar')


class StoreCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
    # required_languages = ('en', 'ar')


translator.register(Store, StoreTranslationOptions)
translator.register(StoreCategory, StoreCategoryTranslationOptions)
