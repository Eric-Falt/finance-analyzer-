import csv
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import csv_handler
import finance


def make_transaction(
    date_time,
    description,
    category,
    amount,
    transaction_type,
):
    return {
        "DateTime": datetime.strptime(date_time, "%m/%d/%Y %H:%M"),
        "Description": description,
        "Category": category,
        "Amount": amount,
        "Type": transaction_type,
    }


class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            make_transaction("01/01/2020 12:00", "Paycheck", "Income", 1000.0, "Income"),
            make_transaction("01/02/2020 12:00", "Lunch", "Food", 25.50, "Expense"),
            make_transaction(
                "02/03/2020 12:00",
                "Bus",
                "Transportation",
                10.0,
                "Expense",
            ),
        ]

    def test_total_income(self):
        self.assertAlmostEqual(finance.total_income(self.transactions), 1000.0)

    def test_total_expenses(self):
        self.assertAlmostEqual(finance.total_expenses(self.transactions), 35.50)

    def test_net_cash_flow(self):
        self.assertAlmostEqual(finance.net_cash_flow(self.transactions), 964.50)

    def test_largest_expense(self):
        self.assertAlmostEqual(finance.largest_expense(self.transactions), 25.50)

    def test_average_expense(self):
        self.assertAlmostEqual(finance.average_expense(self.transactions), 17.75)

    def test_average_expense_is_zero_when_no_expenses_exist(self):
        income_only = [self.transactions[0]]

        self.assertEqual(finance.average_expense(income_only), 0)

    def test_normalize_row_parses_and_normalizes_values(self):
        row = {
            "DateTime": "01/02/2020 12:00",
            "Description": "lunch",
            "Category": "food",
            "Amount": "25.50",
            "Type": "expense",
        }

        result = csv_handler.normalize_row(row)

        self.assertEqual(result["DateTime"], datetime(2020, 1, 2, 12, 0))
        self.assertEqual(result["Description"], "Lunch")
        self.assertEqual(result["Category"], "Food")
        self.assertAlmostEqual(result["Amount"], 25.50)
        self.assertEqual(result["Type"], "Expense")

    def test_normalize_row_rejects_invalid_calendar_date(self):
        row = {
            "DateTime": "02/30/2020 12:00",
            "Description": "lunch",
            "Category": "food",
            "Amount": "25.50",
            "Type": "expense",
        }

        with self.assertRaises(ValueError):
            csv_handler.normalize_row(row)

    def test_normalize_row_rejects_invalid_type(self):
        row = {
            "DateTime": "01/02/2020 12:00",
            "Description": "lunch",
            "Category": "food",
            "Amount": "25.50",
            "Type": "transfer",
        }

        with self.assertRaises(ValueError):
            csv_handler.normalize_row(row)

    def test_normalize_row_rejects_zero_and_non_finite_amounts(self):
        for amount in ("0", "nan", "inf", "-inf"):
            with self.subTest(amount=amount):
                row = {
                    "DateTime": "01/02/2020 12:00",
                    "Description": "lunch",
                    "Category": "food",
                    "Amount": amount,
                    "Type": "expense",
                }

                with self.assertRaises(ValueError):
                    csv_handler.normalize_row(row)

    def test_date_filter_matches_year_month_and_day(self):
        filter_cases = [
            ("0", "2020", ["Paycheck", "Lunch", "Bus"]),
            ("1", "01/2020", ["Paycheck", "Lunch"]),
            ("2", "01/02/2020", ["Lunch"]),
        ]

        for date_precision, date_text, expected_descriptions in filter_cases:
            with self.subTest(date_text=date_text):
                user_inputs = iter(["1", date_precision, date_text, "0"])
                output = StringIO()

                with patch("builtins.input", side_effect=lambda _prompt="": next(user_inputs)):
                    with redirect_stdout(output):
                        finance.filter_transactions(self.transactions)

                rendered_output = output.getvalue()
                for description in expected_descriptions:
                    self.assertIn(description, rendered_output)

                unexpected = set(
                    transaction["Description"]
                    for transaction in self.transactions
                ) - set(expected_descriptions)
                for description in unexpected:
                    self.assertNotIn(description, rendered_output)

    def test_delete_retries_after_non_numeric_input(self):
        user_inputs = iter(["not a number", "0"])

        with patch("builtins.input", side_effect=lambda _prompt="": next(user_inputs)):
            finance.delete_entry(self.transactions)

        self.assertEqual(len(self.transactions), 3)

    def test_delete_removes_confirmed_transaction(self):
        user_inputs = iter(["2", "1", "0"])

        with patch("builtins.input", side_effect=lambda _prompt="": next(user_inputs)):
            finance.delete_entry(self.transactions)

        self.assertEqual(
            [transaction["Description"] for transaction in self.transactions],
            ["Paycheck", "Bus"],
        )

    def test_update_saves_validated_changes(self):
        user_inputs = iter(["2", "2", "updated lunch", "0", "0"])

        with patch("builtins.input", side_effect=lambda _prompt="": next(user_inputs)):
            finance.update_entry(self.transactions)

        self.assertEqual(self.transactions[1]["Description"], "Updated Lunch")
        self.assertIsInstance(self.transactions[1]["DateTime"], datetime)

    def test_cancel_update_discards_changes(self):
        original_description = self.transactions[1]["Description"]
        user_inputs = iter(["2", "2", "changed lunch", "-1", "0"])

        with patch("builtins.input", side_effect=lambda _prompt="": next(user_inputs)):
            finance.update_entry(self.transactions)

        self.assertEqual(self.transactions[1]["Description"], original_description)


class CsvHandlerTests(unittest.TestCase):
    def test_rewrite_and_load_csv_round_trip(self):
        transaction = make_transaction(
            "01/02/2020 12:00",
            "Lunch",
            "Food",
            25.50,
            "Expense",
        )

        with tempfile.TemporaryDirectory() as temp_directory:
            csv_path = Path(temp_directory) / "transactions.csv"
            with patch.object(csv_handler, "CSV_PATH", csv_path):
                csv_handler.rewrite_csv([transaction.copy()])
                loaded_transactions = csv_handler.load_csv()

            self.assertEqual(len(loaded_transactions), 1)
            self.assertEqual(
                loaded_transactions[0]["DateTime"],
                datetime(2020, 1, 2, 12, 0),
            )
            self.assertEqual(loaded_transactions[0]["Description"], "Lunch")
            self.assertEqual(loaded_transactions[0]["Category"], "Food")
            self.assertAlmostEqual(loaded_transactions[0]["Amount"], 25.50)
            self.assertEqual(loaded_transactions[0]["Type"], "Expense")

    def test_rewrite_csv_writes_expected_columns(self):
        transaction = make_transaction(
            "01/02/2020 12:00",
            "Lunch",
            "Food",
            25.50,
            "Expense",
        )

        with tempfile.TemporaryDirectory() as temp_directory:
            csv_path = Path(temp_directory) / "transactions.csv"
            with patch.object(csv_handler, "CSV_PATH", csv_path):
                csv_handler.rewrite_csv([transaction.copy()])

            with csv_path.open(newline="") as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)

        self.assertEqual(
            header,
            ["DateTime", "Description", "Category", "Amount", "Type"],
        )


if __name__ == "__main__":
    unittest.main()
