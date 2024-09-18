# SPDX-License-Identifier: MIT

from mocks import MockListingProvider

from oikotool.formatters import ListingBaseFormatter


class TestListingBaseFormatter:
    def test_address(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.complete_listing)
        result = formatter.address
        expected = "Oikotie 1, Kaivopuisto, Helsinki"
        assert result == expected

    def test_lowercase_address(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.lowercase_address)
        result = formatter.address
        expected = "Oikotie 1 A, Kaivopuisto, Helsinki"
        assert result == expected

    def test_price(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.complete_listing)
        result = formatter.price
        expected = "650 000 €"
        assert result == expected

    def test_size(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.complete_listing)
        result = formatter.size
        expected = "75 m²"
        assert result == expected

    def test_undefined_district(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.undefined_district)
        result = formatter.address
        expected = "Oikotie 1, Helsinki"
        assert result == expected

    def test_undefined_price(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.undefined_price)
        result = formatter.price
        expected = ""
        assert result == expected

    def test_undefined_size(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.undefined_size)
        result = formatter.size
        expected = ""
        assert result == expected

    def test_uppercase_address(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.uppercase_address)
        result = formatter.address
        expected = "Oikotie 1 A, Kaivopuisto, Helsinki"
        assert result == expected

    def test_zero_price(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.zero_price)
        result = formatter.price
        expected = ""
        assert result == expected

    def test_zero_size(self) -> None:
        mock = MockListingProvider()
        formatter = ListingBaseFormatter(mock.zero_size)
        result = formatter.size
        expected = ""
        assert result == expected
