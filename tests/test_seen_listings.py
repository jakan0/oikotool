# SPDX-License-Identifier: MIT

from oikotool.core import Oikotool


class TestSeenListings:
    def test_filter_unseen_listings(self) -> None:
        oikotool = Oikotool()
        mock = [
            {"cardId": "3"},
            {"cardId": "2"},
            {"cardId": "1"},
        ]
        seen: list[str] = []

        # Test case 1: All listings are new
        new_ids, _ = oikotool._filter_unseen_listings(mock, seen)
        assert new_ids == [
            "1",
            "2",
            "3",
        ], "Expected all listings to be identified as new"

        # Test case 2: Handle object without proper identifier
        mock.insert(0, {"pid": "4"})
        new_ids, _ = oikotool._filter_unseen_listings(mock, seen)
        assert new_ids == ["1", "2", "3"], "Expected to ignore object without 'cardId'"
        mock.pop(0)

        # Test case 3: One new listing added
        mock.insert(0, {"cardId": "4"})
        new_ids, _ = oikotool._filter_unseen_listings(mock, seen)
        assert new_ids == [
            "1",
            "2",
            "3",
            "4",
        ], "Expected to identify all listings including the new one"

    def test_refresh_recent_listings(self) -> None:
        oikotool = Oikotool()
        mock = ["1", "2"]
        limit = 3
        seen: list[str] = []

        # Test case 1: Incomplete list (fewer items than the limit)
        seen = oikotool._refresh_recent_listings(seen, mock, limit)
        assert seen == ["1", "2"], "Expected to add all items when count is below limit"

        # Test case 2: Complete list (number of items equals the limit)
        mock.append("3")
        seen = oikotool._refresh_recent_listings(seen, mock, limit)
        assert seen == [
            "1",
            "2",
            "3",
        ], "Expected to have exactly 'limit' number of items"

        # Test case 3: Rolling window (more items than the limit)
        mock.append("4")
        seen = oikotool._refresh_recent_listings(seen, mock, limit)
        assert seen == [
            "2",
            "3",
            "4",
        ], "Expected to keep only the most recent 'limit' items"
