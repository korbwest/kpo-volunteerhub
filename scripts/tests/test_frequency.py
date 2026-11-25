import unittest
from datetime import UTC, datetime, timedelta

from scripts.commit_frequency import summarize


class FrequencyTests(unittest.TestCase):
    def test_interval_boundaries_and_future(self):
        end = datetime(2026, 11, 25, tzinfo=UTC)
        entries = [
            ("old", (end - timedelta(days=7)).timestamp()),
            ("inside", (end - timedelta(days=1)).timestamp()),
            ("end", end.timestamp()),
            ("future", (end + timedelta(seconds=1)).timestamp()),
        ]
        result = summarize(entries, end)
        self.assertEqual(result["commits"], ["inside", "end"])
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["commits_per_day"], round(2 / 7, 4))

    def test_empty_history(self):
        result = summarize([], datetime(2026, 11, 25, tzinfo=UTC))
        self.assertEqual(result["count"], 0)
