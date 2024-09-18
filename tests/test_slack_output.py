# SPDX-License-Identifier: MIT

from mocks import MockListingProvider, MockSlackMessageProvider

from oikotool.core import Oikotool


class TestSlackOutput:
    def test_complete_listing(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.complete_listing)
        assert result == slack.complete_listing

    def test_float_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.float_size)
        assert result == slack.float_size

    def test_undefined_district(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.undefined_district)
        assert result == slack.undefined_district

    def test_undefined_image(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.undefined_image)
        assert result == slack.undefined_image

    def test_undefined_price(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.undefined_price)
        assert result == slack.undefined_price

    def test_undefined_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.undefined_size)
        assert result == slack.undefined_size

    def test_zero_price(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.zero_price)
        assert result == slack.zero_price

    def test_zero_size(self) -> None:
        oikotool = Oikotool()
        listing = MockListingProvider()
        slack = MockSlackMessageProvider()
        result = oikotool._create_slack_message(listing.zero_size)
        assert result == slack.zero_size
