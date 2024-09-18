# SPDX-License-Identifier: MIT

import pytest

from oikotool.core import Oikotool
from oikotool.exceptions import OikotieUrlError


class TestPrepareApiUrl:
    def test_raises_error_for_incorrect_domain(self) -> None:
        oikotool = Oikotool()
        url = "https://toimitilat.oikotie.fi/vuokrattavat-toimitilat"
        with pytest.raises(OikotieUrlError):
            oikotool._prepare_api_url(url)

    def test_raises_error_for_missing_query_string(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot"
        with pytest.raises(OikotieUrlError):
            oikotool._prepare_api_url(url)

    def test_custom_limit(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100"
        result = oikotool._prepare_api_url(url, limit=1)
        expected = "https://asunnot.oikotie.fi/api/search?cardType=100&sortBy=published_sort_desc&limit=1&pagination=1"
        assert result == expected

    def test_sort_viewings(self) -> None:
        oikotool = Oikotool()
        url = "https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100&nextViewingType%5B%5D=3"
        result = oikotool._prepare_api_url(url)
        expected = "https://asunnot.oikotie.fi/api/search?cardType=100&nextViewingType%5B%5D=3&sortBy=viewings&limit=10&pagination=1"
        assert result == expected
