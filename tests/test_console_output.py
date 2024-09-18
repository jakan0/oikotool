# SPDX-License-Identifier: MIT

from mocks import MockListingProvider

from oikotool.core import Oikotool


class TestConsoleOutput:
    def test_complete_listing(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.complete_listing)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 75 m², 650 000 €, https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_float_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.float_size)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 74.5 m², 650 000 €, https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_undefined_district(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.undefined_district)
        expected = "Oikotie 1, Helsinki, 75 m², 650 000 €, https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_undefined_price(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.undefined_price)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 75 m², https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_undefined_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.undefined_size)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 650 000 €, https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_zero_price(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.zero_price)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 75 m², https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected

    def test_zero_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        result = oikotool._create_console_message(listing.zero_size)
        expected = "Oikotie 1, Kaivopuisto, Helsinki, 650 000 €, https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678"
        assert result == expected
