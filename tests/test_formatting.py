import unittest

from ledgerlite.formatting import counts


class CountsTest(unittest.TestCase):
    def test_single_row_matches_issue_example(self) -> None:
        self.assertEqual(counts({"food": 3}), "food  3")

    def test_names_and_counts_are_aligned(self) -> None:
        self.assertEqual(
            counts({"food": 2, "transport": 1}), "food       2\ntransport  1"
        )

    def test_multi_digit_counts_are_right_aligned(self) -> None:
        self.assertEqual(counts({"a": 5, "bb": 10}), "a    5\nbb  10")

    def test_empty_rows_render_nothing(self) -> None:
        self.assertEqual(counts({}), "")


if __name__ == "__main__":
    unittest.main()
