# SPDX-License-Identifier: MIT

from typing import Any


class MockHtmlProvider:
    @property
    def website_with_session_headers(self) -> str:
        return (
            "<!DOCTYPE html>"
            '<html xmlns="http://www.w3.org/1999/html">'
            "<head>"
            '  <meta charset="utf-8" />'
            '  <meta name="api-token" content="01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b" />'
            '  <meta name="loaded" content="1719792000" />'
            '  <meta name="cuid" content="adc83b19e793491b1c6ea0fd8b46cd9f32e592fc" />'
            "</head>"
            "<body>"
            "</body>"
            "</html>"
        )

    @property
    def website_without_session_headers(self) -> str:
        return (
            "<!DOCTYPE html>"
            '<html xmlns="http://www.w3.org/1999/html">'
            "<head>"
            '  <meta charset="utf-8" />'
            "</head>"
            "<body>"
            "</body>"
            "</html>"
        )


class MockListingProvider:
    @property
    def complete_listing(self) -> dict[str, Any]:
        return {
            "cardId": 12345678,
            "url": "https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678",
            "data": {
                "price": "650\u00a0000\u00a0\u20ac",
                "size": "75 m\u00b2",
            },
            "location": {
                "address": "Oikotie 1",
                "district": "Kaivopuisto",
                "city": "Helsinki",
            },
            "medias": [
                {
                    "imageLargeJPEG": "https://cdn.asunnot.oikotie.fi/b2lrb3RpZS5maQo=/12345678",
                }
            ],
        }

    @property
    def float_size(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["data"]["size"] = "74,5 m\u00b2"
        return listing

    @property
    def lowercase_address(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["location"]["address"] = "oikotie 1 a"
        listing["location"]["district"] = "kaivopuisto"
        listing["location"]["city"] = "helsinki"
        return listing

    @property
    def undefined_district(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["location"]["district"] = None
        return listing

    @property
    def undefined_image(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["medias"][0]["imageLargeJPEG"] = None
        return listing

    @property
    def undefined_price(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["data"]["price"] = None
        return listing

    @property
    def undefined_size(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["data"]["size"] = None
        return listing

    @property
    def uppercase_address(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["location"]["address"] = "OIKOTIE 1 A"
        listing["location"]["district"] = "KAIVOPUISTO"
        listing["location"]["city"] = "HELSINKI"
        return listing

    @property
    def zero_price(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["data"]["price"] = 0
        return listing

    @property
    def zero_size(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["data"]["size"] = 0
        return listing


class MockSlackMessageProvider:
    @property
    def complete_listing(self) -> dict[str, Any]:
        return {
            "text": "Oikotie 1, Kaivopuisto, Helsinki",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Oikotie 1, Kaivopuisto, Helsinki",
                    },
                },
                {
                    "type": "image",
                    "image_url": "https://cdn.asunnot.oikotie.fi/b2lrb3RpZS5maQo=/12345678",
                    "alt_text": "Oikotie 1, Kaivopuisto, Helsinki",
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Hinta:*\n650 000 \u20ac"},
                        {"type": "mrkdwn", "text": "*Pinta-ala:*\n75 m\u00b2"},
                    ],
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {
                                    "type": "text",
                                    "text": "Ilmoitus:\n",
                                    "style": {"bold": True},
                                },
                                {
                                    "type": "link",
                                    "url": "https://asunnot.oikotie.fi/myytavat-asunnot/helsinki/12345678",
                                },
                            ],
                        }
                    ],
                },
            ],
        }

    @property
    def float_size(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["blocks"][2]["fields"][1]["text"] = "*Pinta-ala:*\n74.5 m\u00b2"
        return listing

    @property
    def undefined_district(self) -> dict[str, Any]:
        address = "Oikotie 1, Helsinki"
        listing = self.complete_listing
        listing["text"] = address
        listing["blocks"][0]["text"]["text"] = address
        listing["blocks"][1]["alt_text"] = address
        return listing

    @property
    def undefined_image(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["blocks"][1]["image_url"] = (
            "https://asunnot.oikotie.fi/lib/images/placeholder/building/large.jpg"
        )
        return listing

    @property
    def undefined_price(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["blocks"][2]["fields"][0]["text"] = "*Hinta:*\nEi ilmoitettu"
        return listing

    @property
    def undefined_size(self) -> dict[str, Any]:
        listing = self.complete_listing
        listing["blocks"][2]["fields"][1]["text"] = "*Pinta-ala:*\nEi ilmoitettu"
        return listing

    @property
    def zero_price(self) -> dict[str, Any]:
        return self.undefined_price

    @property
    def zero_size(self) -> dict[str, Any]:
        return self.undefined_size
