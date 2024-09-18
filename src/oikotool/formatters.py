# SPDX-License-Identifier: MIT

import re
from typing import Any, Optional

from oikotool.translations import Translations


class ListingBaseFormatter:
    """
    A base formatter class for formatting listing data.

    This class provides methods to format various attributes of a listing,
    such as address, price, and size. It uses lazy loading for its properties,
    meaning the formatted values are only calculated when first accessed and
    then cached for subsequent accesses.
    """

    _listing: dict[str, Any]
    _formatted_address: Optional[str]
    _formatted_price: Optional[str]
    _formatted_size: Optional[str]
    _prepared_image_url: Optional[str]

    def __init__(self, listing: dict[str, Any]) -> None:
        self._listing = listing
        self._formatted_address = None
        self._formatted_price = None
        self._formatted_size = None
        self._prepared_image_url = None

    def _format_address(self) -> str:
        location = self._listing["location"]
        return ", ".join(
            [
                value.title()
                for value in [
                    location["address"],
                    location["district"],
                    location["city"],
                ]
                if value
            ]
        )

    def _format_price(self) -> str:
        number = re.sub(r"[^\d,]", "", str(self._listing["data"]["price"]))
        number = number.replace(",", ".")
        price = float(number) if number else None
        if price and price > 0:
            formatted = f"{price:_.0f}".replace("_", " ")
            return f"{formatted} €"
        return ""

    def _format_size(self) -> str:
        number = re.sub(r"[^\d,]", "", str(self._listing["data"]["size"]))
        number = number.replace(",", ".")
        size = float(number) if number else None
        if size and size > 0:
            formatted = f"{size:.1f}" if size % 1 else f"{size:.0f}"
            return f"{formatted} m²"
        return ""

    def _prepare_image_url(self) -> str:
        medias = self._listing["medias"]
        image = medias[0]["imageLargeJPEG"] if len(medias) > 0 else None
        if image and isinstance(image, str):
            return str(image)
        return "https://asunnot.oikotie.fi/lib/images/placeholder/building/large.jpg"

    @property
    def address(self) -> str:
        if self._formatted_address is None:
            self._formatted_address = self._format_address()
        return self._formatted_address

    @property
    def image(self) -> str:
        if self._prepared_image_url is None:
            self._prepared_image_url = self._prepare_image_url()
        return self._prepared_image_url

    @property
    def price(self) -> str:
        if self._formatted_price is None:
            self._formatted_price = self._format_price()
        return self._formatted_price

    @property
    def size(self) -> str:
        if self._formatted_size is None:
            self._formatted_size = self._format_size()
        return self._formatted_size


class ListingConsoleFormatter(ListingBaseFormatter):
    """
    A formatter class for console output of listing data.

    This class inherits from ListingBaseFormatter and is specifically designed
    for formatting listing data for console output. For console-specific
    formatting needs, the necessary methods are overridden in this class.
    """

    pass


class ListingSlackFormatter(ListingBaseFormatter):
    """
    A formatter class for Slack output of listing data.

    This class inherits from ListingBaseFormatter and is specifically designed
    for formatting listing data for Slack output. For Slack-specific formatting
    needs, the necessary methods are overridden in this class.
    """

    def __init__(self, listing: dict[str, Any], translations: Translations) -> None:
        super().__init__(listing)
        self._translations = translations

    @property
    def price(self) -> str:
        return super().price or self._translations.empty_field

    @property
    def size(self) -> str:
        return super().size or self._translations.empty_field
