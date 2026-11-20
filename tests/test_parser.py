import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from ledgerlite.parser import ParseError, read_entries


class ReadEntriesTest(unittest.TestCase):
    def write(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        tmp.write(text)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        return Path(tmp.name)

    def test_reads_entries(self) -> None:
        path = self.write(
            "date,amount,category,description\n"
            "2026-01-03,12.50,Food,lunch\n"
            "2026-01-04,40,transport,\n"
        )
        entries = read_entries(path)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].amount, Decimal("12.50"))
        self.assertEqual(entries[0].category, "food")
        self.assertEqual(entries[1].description, "")

    def test_skips_blank_lines(self) -> None:
        path = self.write("date,amount,category,description\n\n2026-01-03,1,food,\n")
        self.assertEqual(len(read_entries(path)), 1)

    def test_empty_file_has_no_entries(self) -> None:
        path = self.write("")
        self.assertEqual(read_entries(path), [])

    def test_rejects_file_with_only_a_blank_line(self) -> None:
        path = self.write("\n")
        with self.assertRaises(ParseError):
            read_entries(path)

    def test_rejects_wrong_header(self) -> None:
        path = self.write("when,how much\n2026-01-03,1\n")
        with self.assertRaises(ParseError):
            read_entries(path)

    def test_rejects_bad_amount(self) -> None:
        path = self.write("date,amount,category,description\n2026-01-03,abc,food,\n")
        with self.assertRaisesRegex(ParseError, "line 2"):
            read_entries(path)

    def test_rejects_bad_date(self) -> None:
        path = self.write("date,amount,category,description\n03/01/2026,1,food,\n")
        with self.assertRaisesRegex(ParseError, "bad date"):
            read_entries(path)


if __name__ == "__main__":
    unittest.main()
