import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from ledgerlite.cli import main

LEDGER = (
    "date,amount,category,description\n"
    "2026-01-02,12,food,lunch\n"
    "2026-01-15,30,transport,train\n"
    "2026-02-01,5,food,coffee\n"
)


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.file = self.dir / "ledger.csv"
        self.file.write_text(LEDGER)

    def run_cli(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = main(list(args))
        return code, out.getvalue()

    def test_summary(self) -> None:
        code, out = self.run_cli("summary", str(self.file))
        self.assertEqual(code, 0)
        self.assertIn("2026-01", out)
        self.assertIn("42.00", out)
        self.assertIn("transport", out)

    def test_categories(self) -> None:
        self.assertEqual(self.run_cli("categories", str(self.file)), (0, "food\ntransport\n"))

    def test_export(self) -> None:
        out = self.dir / "out.csv"
        code, text = self.run_cli("export", str(self.file), str(out))
        self.assertEqual(code, 0)
        self.assertIn("wrote 3 entries", text)

    def test_export_output_can_be_read_back(self) -> None:
        out = self.dir / "out.csv"
        code, _ = self.run_cli("export", str(self.file), str(out))
        self.assertEqual(code, 0)
        self.assertEqual(
            out.read_text().splitlines()[0], "date,amount,category,description"
        )
        code, text = self.run_cli("summary", str(out))
        self.assertEqual(code, 0)
        self.assertIn("2026-01", text)
        self.assertIn("42.00", text)

    def test_missing_file(self) -> None:
        code, out = self.run_cli("summary", str(self.dir / "nope.csv"))
        self.assertEqual(code, 1)
        self.assertIn("error:", out)


if __name__ == "__main__":
    unittest.main()
