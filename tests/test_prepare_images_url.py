# SPDX-License-Identifier: MIT

import pytest

from oikotool.core import Oikotool
from oikotool.exceptions import OikotieUrlError


class TestPrepareListingImagesUrl:
    def test_raises_error_for_incorrect_domain(self) -> None:
        oikotool = Oikotool()
        url = "https://toimitilat.oikotie.fi/vuokrattavat-toimitilat"
        with pytest.raises(OikotieUrlError):
            oikotool._prepare_listing_images_url(url)

    def test_raises_error_for_query_string(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100"
        with pytest.raises(OikotieUrlError):
            oikotool._prepare_listing_images_url(url)

    def test_raises_error_for_invalid_listing_url(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot/helsinki"
        with pytest.raises(OikotieUrlError):
            oikotool._prepare_listing_images_url(url)

    def test_images_url(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        result = oikotool._prepare_listing_images_url(url)
        expected = "https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678/kuvat"
        assert result == expected
