import tempfile
import unittest
from pathlib import Path

from scripts.html_report import render, section


class HtmlReportTests(unittest.TestCase):
    def test_statuses_and_escaped_diagnostics(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "junit.xml"
            path.write_text('''<testsuites><testsuite><testcase name="ok" time="0.12"/>
<testcase name="bad"><failure message="&lt;script&gt;">a &amp; b</failure></testcase>
<testcase name="skip"><skipped message="PostgreSQL required"/></testcase>
<testcase name="broken"><error message="setup failed"/></testcase>
</testsuite></testsuites>''', encoding="utf-8")
            html = section("Backend", path)
            self.assertIn("Всего: 4", html)
            self.assertIn("Пройдено: 1", html)
            self.assertIn("Ошибок: 2", html)
            self.assertIn("Пропущено: 1", html)
            self.assertIn("&lt;script&gt;", html)
            self.assertNotIn("<script>", html)
            self.assertIn("PostgreSQL required", html)
            self.assertIn("0.12", html)

    def test_missing_and_malformed_are_not_success(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "junit.xml"
            self.assertIn("Результаты неизвестны", render(path, path))
            path.write_text("invalid xml", encoding="utf-8")
            self.assertIn("Не удалось прочитать", section("Backend", path))
