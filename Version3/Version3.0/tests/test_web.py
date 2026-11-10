import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import database
from app import create_app


class WebAppTests(unittest.TestCase):
    """Exercise the web routes with Flask's test client and a temporary database."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path_patch = patch.object(
            database,
            "DB_PATH",
            str(Path(self.temp_directory.name) / "finance.db"),
        )
        self.database_path_patch.start()
        # Prepare an empty test database before any simulated browser request.
        database.initialize_database()
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temp_directory.cleanup()

    def test_dashboard_shows_financial_summary(self):
        database.add_transaction(
            {
                "DateTime": datetime(2026, 1, 2, 12, 0),
                "Description": "Paycheck",
                "Category": "Work",
                "Amount": 1200,
                "Type": "Income",
            }
        )
        database.add_transaction(
            {
                "DateTime": datetime(2026, 1, 3, 12, 0),
                "Description": "Groceries",
                "Category": "Food",
                "Amount": 50,
                "Type": "Expense",
            }
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"$1200.00", response.data)
        self.assertIn(b"$50.00", response.data)
        self.assertIn(b"$1150.00", response.data)
        self.assertIn(b"Groceries", response.data)

    def test_add_transaction_persists_validated_data(self):
        response = self.client.post(
            "/transactions",
            data={
                "date": "2026-01-03T12:30",
                "description": "coffee",
                "category": "food",
                "amount": "5.25",
                "type": "expense",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Transaction added.", response.data)
        saved = database.get_all_transactions()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["Description"], "Coffee")
        self.assertEqual(saved[0]["Type"], "Expense")
        self.assertEqual(saved[0]["DateTime"], datetime(2026, 1, 3, 12, 30))

    def test_invalid_transaction_is_not_saved(self):
        response = self.client.post(
            "/transactions",
            data={
                "date": "not-a-date",
                "description": "coffee",
                "category": "food",
                "amount": "5.25",
                "type": "expense",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter a valid transaction date and time", response.data)
        self.assertEqual(database.get_all_transactions(), [])

    def test_edit_and_delete_transaction(self):
        transaction_id = database.add_transaction(
            {
                "DateTime": datetime(2026, 1, 2, 12, 0),
                "Description": "Lunch",
                "Category": "Food",
                "Amount": 20,
                "Type": "Expense",
            }
        )

        edit_response = self.client.post(
            f"/transactions/{transaction_id}/edit",
            data={
                "date": "2026-01-04T13:00",
                "description": "dinner",
                "category": "food",
                "amount": "30",
                "type": "expense",
            },
            follow_redirects=True,
        )
        self.assertEqual(edit_response.status_code, 200)
        self.assertIn(b"Transaction updated.", edit_response.data)
        self.assertEqual(database.get_all_transactions()[0]["Description"], "Dinner")

        delete_response = self.client.post(
            f"/transactions/{transaction_id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(b"Transaction deleted.", delete_response.data)
        self.assertEqual(database.get_all_transactions(), [])

    def test_missing_transaction_returns_not_found(self):
        self.assertEqual(self.client.get("/transactions/999/edit").status_code, 404)
        self.assertEqual(self.client.post("/transactions/999/delete").status_code, 404)


if __name__ == "__main__":
    unittest.main()
