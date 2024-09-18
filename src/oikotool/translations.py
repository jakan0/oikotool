# SPDX-License-Identifier: MIT

from enum import Enum


class Language(Enum):
    ENGLISH = 1
    FINNISH = 2


class Translations:
    def __init__(self, language: Language):
        self._language = language
        self._translations = {
            Language.ENGLISH: {
                "empty_field": "Not specified",
                "label_price": "Price",
                "label_size": "Size",
                "label_listing": "Listing",
            },
            Language.FINNISH: {
                "empty_field": "Ei ilmoitettu",
                "label_price": "Hinta",
                "label_size": "Pinta-ala",
                "label_listing": "Ilmoitus",
            },
        }

    def __getattr__(self, key: str) -> str:
        try:
            return self._translations[self._language][key]
        except KeyError:
            return key
