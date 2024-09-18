# SPDX-License-Identifier: MIT

import json
import re
import shutil
from pathlib import Path
from typing import Any, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from bs4 import BeautifulSoup

from oikotool.exceptions import (
    OikotieAddressException,
    OikotieSessionError,
    OikotieUrlError,
)
from oikotool.formatters import ListingConsoleFormatter, ListingSlackFormatter
from oikotool.translations import Language, Translations
from oikotool.utils import HttpUtils


class Oikotool:
    LISTINGS_FILE: str = "seen.txt"
    OIKOTIE_API_PATH: str = "/api/search"
    OIKOTIE_ASUNNOT_CDN_URL: str = "https://cdn.asunnot.oikotie.fi/"
    OIKOTIE_ASUNNOT_WEB_URL: str = "https://asunnot.oikotie.fi/"
    OIKOTIE_IMAGES_PATH: str = "/kuvat"

    def __init__(
        self, translations: Translations = Translations(Language.FINNISH)
    ) -> None:
        _, netloc, _, _, _ = urlsplit(self.OIKOTIE_ASUNNOT_WEB_URL)
        self.OIKOTIE_ASUNNOT_WEB_HOST = netloc
        self._translations = translations

    def _create_console_message(self, listing: dict[str, Any]) -> str:
        formatter = ListingConsoleFormatter(listing)
        details = [formatter.address, formatter.size, formatter.price, listing["url"]]
        return ", ".join(s for s in details if s)

    def _create_slack_message(self, listing: dict[str, Any]) -> dict[str, Any]:
        formatter = ListingSlackFormatter(listing, self._translations)
        return {
            "text": formatter.address,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": formatter.address,
                    },
                },
                {
                    "type": "image",
                    "image_url": formatter.image,
                    "alt_text": formatter.address,
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*{self._translations.label_price}:*\n{formatter.price}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*{self._translations.label_size}:*\n{formatter.size}",
                        },
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
                                    "text": f"{self._translations.label_listing}:\n",
                                    "style": {"bold": True},
                                },
                                {
                                    "type": "link",
                                    "url": listing["url"],
                                },
                            ],
                        }
                    ],
                },
            ],
        }

    def _extract_session_headers(self, html: str) -> dict[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        mapping = {"cuid": "OTA-cuid", "loaded": "OTA-loaded", "api-token": "OTA-token"}
        headers = {}

        for meta, header in mapping.items():
            tag = soup.select_one(f"meta[name={meta}]")
            if tag and "content" in tag.attrs:
                headers[header] = tag.attrs.get("content", "")
            else:
                raise OikotieSessionError(f"'{meta}' tag is missing from the response.")

        return headers

    def _filter_unseen_listings(
        self, listings: list[dict[str, Any]], seen_ids: list[str]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        new_ids = []
        new_listings = []
        for listing in reversed(listings):
            listing_id = listing.get("cardId")
            if listing_id is not None:
                str_id = str(listing_id)
                if str_id not in seen_ids:
                    new_ids.append(str_id)
                    new_listings.append(listing)
        return new_ids, new_listings

    def _get_listing_details(self, url: str) -> tuple[Optional[str], list[str]]:
        url = self._prepare_listing_images_url(url)
        response = HttpUtils.get_with_retry(url)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = []

        for tag in soup.select(f'a[href^="{self.OIKOTIE_ASUNNOT_CDN_URL}"]'):
            href = tag.attrs.get("href")
            if href is not None:
                urls.append(str(href))

        address = None
        header = soup.select_one(".heading--no-styling .listing-header__text")
        if header and header.text:
            address = header.text

        return (address, urls)

    def _get_unseen_listings(
        self, url: str, listings_file: Optional[Path]
    ) -> tuple[list[str], list[dict[str, Any]]]:
        session = self._initialize_session()
        response = HttpUtils.get_with_retry(url, headers=session)
        listings = response.json()["cards"]
        seen_listings = self._read_listings_file(listings_file)
        return self._filter_unseen_listings(listings, seen_listings)

    def _initialize_session(self) -> dict[str, str]:
        response = HttpUtils.get_with_retry(self.OIKOTIE_ASUNNOT_WEB_URL)
        return self._extract_session_headers(response.text)

    def _output_image_path_to_console(self, path: Path) -> None:
        print(f"Saved file: {path}")

    def _output_listings_to_console(self, listings: list[dict[str, Any]]) -> None:
        for listing in listings:
            message = self._create_console_message(listing)
            print(message)

    def _ping_health_services(
        self,
        healthchecks_url: Optional[str],
        uptime_url: Optional[str],
        failure: bool = False,
    ) -> None:
        if healthchecks_url:
            try:
                self._ping_healthchecks_io(healthchecks_url, failure=failure)
            except Exception:
                pass

        if uptime_url:
            try:
                self._ping_uptime_kuma(uptime_url, failure=failure)
            except Exception:
                pass

    def _ping_healthchecks_io(self, url: str, failure: bool = False) -> None:
        url = f"{url}/fail" if failure else url
        HttpUtils.get_with_retry(url)

    def _ping_uptime_kuma(self, url: str, failure: bool = False) -> None:
        scheme, netloc, path, query, fragment = urlsplit(url)
        query = urlencode([("status", "up" if not failure else "down")])
        url = urlunsplit((scheme, netloc, path, query, None))
        HttpUtils.get_with_retry(url)

    def _post_listings_to_slack(self, listings: list[dict[str, Any]], url: str) -> None:
        headers = {"Content-Type": "application/json"}
        for listing in listings:
            message = self._create_slack_message(listing)
            HttpUtils.post_with_retry(url, data=json.dumps(message), headers=headers)

    def _prepare_api_url(self, url: str, limit: int = 10) -> str:
        scheme, netloc, path, query, fragment = urlsplit(url)

        if netloc != self.OIKOTIE_ASUNNOT_WEB_HOST:
            raise OikotieUrlError(
                f"Invalid domain: {netloc}, expected: {self.OIKOTIE_ASUNNOT_WEB_HOST}."
            )
        elif not query:
            raise OikotieUrlError(
                f"Missing query string: {url}, expected: '...?key1=value1&key2=value2'"
            )

        params = [
            (k, v)
            for k, v in parse_qsl(query)
            if k not in ["sortBy", "limit", "pagination"]
        ]
        viewings = any(t[0] == "nextViewingType[]" for t in params)
        params.append(("sortBy", "viewings" if viewings else "published_sort_desc"))
        params.append(("limit", str(limit)))
        params.append(("pagination", "1"))

        return urlunsplit(
            (scheme, netloc, self.OIKOTIE_API_PATH, urlencode(params), fragment)
        )

    def _prepare_listing_images_url(self, url: str) -> str:
        scheme, netloc, path, query, fragment = urlsplit(url)

        if netloc != self.OIKOTIE_ASUNNOT_WEB_HOST:
            raise OikotieUrlError(
                f"Invalid domain: {netloc}, expected: {self.OIKOTIE_ASUNNOT_WEB_HOST}."
            )
        elif not re.search(r"/\d{8,}$", path):
            raise OikotieUrlError(f"Invalid listing address: {url}")
        elif query:
            raise OikotieUrlError(f"Invalid listing address: {url}")

        path = (
            f"{path}{self.OIKOTIE_IMAGES_PATH}"
            if not path.endswith(self.OIKOTIE_IMAGES_PATH)
            else path
        )

        return urlunsplit((scheme, netloc, path, None, None))

    def _read_listings_file(self, listings_file: Optional[Path]) -> list[str]:
        seen_listings = set()
        if listings_file and listings_file.exists():
            with listings_file.open("r") as f:
                seen_listings = set(f.read().splitlines())
        return list(seen_listings)

    def _refresh_recent_listings(
        self, seen: list[str], new: list[str], limit: int = 10
    ) -> list[str]:
        for item in new:
            if item and item not in seen:
                seen.append(item)
        return seen[-limit:]

    def _update_listings_file(
        self, listings_file: Path, new_ids: list[str], limit: int = 10
    ) -> None:
        seen_listings = []
        if listings_file.exists():
            with listings_file.open("r") as f:
                seen_listings = f.read().splitlines()

        seen_listings = self._refresh_recent_listings(seen_listings, new_ids, limit)

        with listings_file.open("w") as f:
            f.write("\n".join(seen_listings))

    def check(
        self,
        url: str,
        name: str,
        limit: int,
        cache_dir: Path,
        slack_url: Optional[str] = None,
        healthchecks_url: Optional[str] = None,
        uptime_url: Optional[str] = None,
        quiet: bool = False,
    ) -> None:
        try:
            check_dir = cache_dir / name
            check_dir.mkdir(parents=True, exist_ok=True)
            listings_file = check_dir / self.LISTINGS_FILE

            url = self._prepare_api_url(url, limit)
            unseen_ids, unseen_listings = self._get_unseen_listings(url, listings_file)

            if slack_url:
                self._post_listings_to_slack(unseen_listings, slack_url)
            if not quiet:
                self._output_listings_to_console(unseen_listings)

            self._update_listings_file(listings_file, unseen_ids, limit)
            self._ping_health_services(healthchecks_url, uptime_url)

        except Exception:
            self._ping_health_services(healthchecks_url, uptime_url, failure=True)
            raise

    def dump(self, url: str, limit: int) -> None:
        session = self._initialize_session()
        url = self._prepare_api_url(url, limit)
        response = HttpUtils.get_with_retry(url, headers=session)
        print(json.dumps(response.json()))

    def save(
        self,
        url: str,
        base_dir: Path,
        batch: bool = False,
        quiet: bool = False,
    ) -> None:
        address, images = self._get_listing_details(url)

        if batch:
            if not address:
                raise OikotieAddressException("Failed to extract listing address")
            base_dir = base_dir / address / "Kuvat"

        base_dir.mkdir(parents=True, exist_ok=True)

        for url in images:
            with HttpUtils.get_with_retry(url, stream=True) as response:
                ctype = str(response.headers.get("Content-Type"))
                bname = url.split("/")[-1]
                ext = ctype.split("/")[-1]
                output = base_dir / f"{bname}.{ext}"

                with output.open("wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)

                    if not quiet:
                        self._output_image_path_to_console(output)

    def slack(self, url: str, limit: int) -> None:
        url = self._prepare_api_url(url, limit)
        _, listings = self._get_unseen_listings(url, None)
        for listing in listings:
            message = self._create_slack_message(listing)
            print(json.dumps(message))
