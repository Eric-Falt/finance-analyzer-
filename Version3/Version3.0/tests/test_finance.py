import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import database
import finance


def make_transaction(date_time, description, category, amount, transaction_type):
    """Build a transaction with the datetime object expected by the app."""
    return {
        "DateTime": datetime.strptime(date_time, "%m/%d/%Y %H:%M"),
        "Description": description,
        "Category": category,
        "Amount": amount,
        "Type": transaction_type,
    }


class DatabaseTests(unittest.TestCase):
    """Test SQLite operations using a temporary database instead of user data."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "finance.db"
        self.database_path_patch = patch.object(
            database, "DB_PATH", str(self.database_path)
        )
        self.database_path_patch.start()
        # Each test gets an empty database so it cannot change finance.db.
        database.initialize_database()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temp_directory.cleanup()

    def test_normalize_transaction_parses_and_normalizes_values(self):
        transaction = make_transaction(
            "01/02/2020 12:00", "lunch", "food", 25.50, "expense"
        )

        normalized = database.normalize_transaction(transaction)

        self.assertEqual(normalized["DateTime"], datetime(2020, 1, 2, 12, 0))
        self.assertEqual(normalized["Description"], "Lunch")
        self.assertEqual(normalized["Category"], "Food")
        self.assertAlmostEqual(normalized["Amount"], 25.50)
        self.assertEqual(normalized["Type"], "Expense")

    def test_normalize_transaction_rejects_invalid_values(self):
        invalid_transactions = [
            ("invalid calendar date", {"DateTime": "02/30/2020 12:00"}),
            ("invalid type", {"Type": "Transfer"}),
            ("zero amount", {"Amount": 0}),
            ("non-finite amount", {"Amount": float("inf")}),
            ("missing description", {"Description": " "}),
            ("missing category", {"Category": " "}),
        ]

        for case, changes in invalid_transactions:
            with self.subTest(case=case):
                transaction = make_transaction(
                    "01/02/2020 12:00", "Lunch", "Food", 25.50, "Expense"
                )
                transaction.update(changes)

                with self.assertRaises(ValueError):
                    database.normalize_transaction(transaction)

    def test_database_add_update_delete_round_trip(self):
        transaction = make_transaction(
            "01/02/2020 12:00", "Lunch", "Food", 25.50, "Expense"
        )
        transaction_id = database.add_transaction(transaction)

        saved = database.get_all_transactions()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["id"], transaction_id)
        self.assertEqual(saved[0]["Description"], "Lunch")
        self.assertEqual(saved[0]["DateTime"], datetime(2020, 1, 2, 12, 0))

        updated = make_transaction(
            "01/03/2020 12:00", "Dinner", "Food", 30.00, "Expense"
        )
        self.assertEqual(database.update_transaction(transaction_id, updated), 1)
        saved = database.get_all_transactions()
        self.assertEqual(saved[0]["Description"], "Dinner")
        self.assertAlmostEqual(saved[0]["Amount"], 30.00)

        self.assertEqual(database.delete_transaction(transaction_id), 1)
        self.assertEqual(database.get_all_transactions(), [])
        self.assertEqual(database.delete_transaction(transaction_id), 0)

    def test_save_transactions_replaces_database_contents(self):
        database.add_transaction(
            make_transaction(
                "01/01/2020 12:00", "Old transaction", "Other", 5.0, "Expense"
            )
        )
        transactions = [
            make_transaction(
                "01/02/2020 12:00", "Paycheck", "Income", 1000.0, "Income"
            ),
            make_transaction(
                "01/03/2020 12:00", "Lunch", "Food", 25.50, "Expense"
            ),
        ]

        database.save_transactions(transactions)

        saved = database.get_all_transactions()
        self.assertEqual(
            [transaction["Description"] for transaction in saved],
            ["Paycheck", "Lunch"],
        )


class FinanceTests(unittest.TestCase):
    """Test calculations and CLI actions against isolated persisted transactions."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path_patch = patch.object(
            database,
            "DB_PATH",
            str(Path(self.temp_directory.name) / "finance.db"),
        )
        self.database_path_patch.start()
        database.initialize_database()
        for transaction in (
            make_transaction(
                "01/01/2020 12:00", "Paycheck", "Income", 1000.0, "Income"
            ),
            make_transaction("01/02/2020 12:00", "Lunch", "Food", 25.50, "Expense"),
            make_transaction(
                "02/03/2020 12:00", "Bus", "Transportation", 10.0, "Expense"
            ),
        ):
            database.add_transaction(transaction)
        self.transactions = database.get_all_transactions()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temp_directory.cleanup()

    def test_financial_calculations(self):
        self.assertAlmostEqual(finance.total_income(self.transactions), 1000.0)
        self.assertAlmostEqual(finance.total_expenses(self.transactions), 35.50)
        self.assertAlmostEqual(finance.net_cash_flow(self.transactions), 964.50)
        self.assertAlmostEqual(finance.largest_expense(self.transactions), 25.50)
        self.assertAlmostEqual(finance.average_expense(self.transactions), 17.75)
        self.assertEqual(finance.average_expense([self.transactions[0]]), 0)

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

                with patch(
                    "builtins.input",
                    side_effect=lambda _prompt="": next(user_inputs),
                ), redirect_stdout(output):
                    finance.filter_transactions(self.transactions)

                rendered_output = output.getvalue()
                for description in expected_descriptions:
                    self.assertIn(description, rendered_output)

                unexpected = {
                    transaction["Description"] for transaction in self.transactions
                } - set(expected_descriptions)
                for description in unexpected:
                    self.assertNotIn(description, rendered_output)

    def test_delete_retries_after_non_numeric_input(self):
        user_inputs = iter(["not a number", "0"])

        with patch(
            "builtins.input", side_effect=lambda _prompt="": next(user_inputs)
        ):
            finance.delete_entry(self.transactions)

        self.assertEqual(len(self.transactions), 3)
        self.assertEqual(len(database.get_all_transactions()), 3)

    def test_delete_removes_confirmed_transaction_from_database(self):
        user_inputs = iter(["2", "1", "0"])

        with patch(
            "builtins.input", side_effect=lambda _prompt="": next(user_inputs)
        ):
            finance.delete_entry(self.transactions)

        descriptions = [transaction["Description"] for transaction in self.transactions]
        self.assertEqual(descriptions, ["Paycheck", "Bus"])
        self.assertEqual(
            [transaction["Description"] for transaction in database.get_all_transactions()],
            ["Paycheck", "Bus"],
        )

    def test_update_persists_validated_changes(self):
        user_inputs = iter(["2", "2", "updated lunch", "0", "0"])

        with patch(
            "builtins.input", side_effect=lambda _prompt="": next(user_inputs)
        ):
            finance.update_entry(self.transactions)

        self.assertEqual(self.transactions[1]["Description"], "Updated Lunch")
        self.assertIsInstance(self.transactions[1]["DateTime"], datetime)
        self.assertEqual(
            database.get_all_transactions()[1]["Description"], "Updated Lunch"
        )

    def test_cancel_update_discards_changes(self):
        original_description = self.transactions[1]["Description"]
        user_inputs = iter(["2", "2", "changed lunch", "-1", "0"])

        with patch(
            "builtins.input", side_effect=lambda _prompt="": next(user_inputs)
        ):
            finance.update_entry(self.transactions)

        self.assertEqual(self.transactions[1]["Description"], original_description)
        self.assertEqual(
            database.get_all_transactions()[1]["Description"], original_description
        )


if __name__ == "__main__":
    unittest.main()
