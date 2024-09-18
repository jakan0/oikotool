# SPDX-License-Identifier: MIT

import pytest
from mocks import MockHtmlProvider

from oikotool.core import Oikotool
from oikotool.exceptions import OikotieSessionError


class TestSessionHeaders:
    def test_extract_session_headers_success(self) -> None:
        oikotool = Oikotool()
        html = MockHtmlProvider()
        result = oikotool._extract_session_headers(html.website_with_session_headers)
        expected = {
            "OTA-cuid": "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
            "OTA-loaded": "1719792000",
            "OTA-token": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
        }
        assert result == expected

    def test_extract_session_headers_failure(self) -> None:
        oikotool = Oikotool()
        html = MockHtmlProvider()
        with pytest.raises(OikotieSessionError):
            oikotool._extract_session_headers(html.website_without_session_headers)
