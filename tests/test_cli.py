import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from ledgerlite.cli import main

LEDGER = (
    "date,amount,category,description\n"
    "2026-01-02,12,food,lunch\n"
    "2026-01-15,30,transport,train\n"
    "2026-02-01,5,food,coffee\n"
)

REFUND_LEDGER = (
    "date,amount,category,description\n"
    "2026-01-02,12.00,food,lunch\n"
    "2026-01-15,30.00,clothing,jacket\n"
    "2026-01-20,-60.00,clothing,jacket refund\n"
    "2026-02-01,5.25,food,coffee\n"
    "2026-03-01,-7.50,clothing,returned boots\n"
)


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.file = self.dir / "ledger.csv"
        self.file.write_text(LEDGER)
        self.empty = self.dir / "empty.csv"
        self.empty.write_text("")

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

    def test_summary_refund_lowers_its_month(self) -> None:
        refund_file = self.dir / "refunds.csv"
        refund_file.write_text(REFUND_LEDGER)
        code, out = self.run_cli("summary", str(refund_file))
        self.assertEqual(code, 0)
        month_table, category_table = out.split("\n\n", 1)
        month_rows = {
            month: Decimal(value)
            for month, value in (line.split() for line in month_table.splitlines()[1:])
        }
        self.assertEqual(
            month_rows,
            {
                "2026-01": Decimal("-18.00"),
                "2026-02": Decimal("5.25"),
                "2026-03": Decimal("-7.50"),
            },
        )
        self.assertIn("clothing", category_table)
        self.assertIn("-37.50", category_table)

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

    def test_summary_of_empty_file(self) -> None:
        code, out = self.run_cli("summary", str(self.empty))
        self.assertEqual(code, 0)
        self.assertIn("Per month\n(no entries)", out)
        self.assertIn("Per category\n(no entries)", out)

    def test_categories_of_empty_file(self) -> None:
        self.assertEqual(self.run_cli("categories", str(self.empty)), (0, "\n"))

    def test_export_of_empty_file(self) -> None:
        out = self.dir / "empty-out.csv"
        code, text = self.run_cli("export", str(self.empty), str(out))
        self.assertEqual(code, 0)
        self.assertIn("wrote 0 entries", text)
        self.assertEqual(
            out.read_text().splitlines(), ["date,amount,category,description"]
        )
        code, text = self.run_cli("summary", str(out))
        self.assertEqual(code, 0)
        self.assertIn("(no entries)", text)

    def test_empty_file_does_not_crash_the_process(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "ledgerlite", "summary", str(self.empty)],
            capture_output=True,
            text=True,
            cwd=repo_root,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("(no entries)", result.stdout)

    def test_missing_file(self) -> None:
        code, out = self.run_cli("summary", str(self.dir / "nope.csv"))
        self.assertEqual(code, 1)
        self.assertIn("error:", out)


if __name__ == "__main__":
    unittest.main()
