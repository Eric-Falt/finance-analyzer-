import os
import secrets
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import database
import finance


def create_app():
    """Build the Flask app and connect its pages to the existing finance logic."""
    app = Flask(__name__)
    # Flask uses this key to sign session data, including one-time flash messages.
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

    @app.before_request
    def initialize_database():
        # Create the SQLite table on first use; this is safe to call on later requests.
        database.initialize_database()

    @app.get("/")
    def index():
        """Show saved transactions and calculate summary totals for the dashboard."""
        transactions = database.get_all_transactions()
        return render_template(
            "index.html",
            transactions=transactions,
            total_income=finance.total_income(transactions),
            total_expenses=finance.total_expenses(transactions),
            net_cash_flow=finance.net_cash_flow(transactions),
        )

    @app.post("/transactions")
    def add_transaction():
        """Validate and save the add form, then return to the dashboard."""
        try:
            # The database module performs the shared field validation and normalization.
            database.add_transaction(_transaction_from_form())
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash("Transaction added.", "success")
        return redirect(url_for("index"))

    @app.route("/transactions/<int:transaction_id>/edit", methods=["GET", "POST"])
    def edit_transaction(transaction_id):
        """Display an edit form, or validate and save its submitted changes."""
        transaction = _find_transaction(transaction_id)
        if transaction is None:
            abort(404)

        if request.method == "POST":
            try:
                updated_rows = database.update_transaction(
                    transaction_id, _transaction_from_form()
                )
            except ValueError as error:
                flash(str(error), "error")
            else:
                if updated_rows == 0:
                    abort(404)
                flash("Transaction updated.", "success")
                return redirect(url_for("index"))

        return render_template("edit.html", transaction=transaction)

    @app.post("/transactions/<int:transaction_id>/delete")
    def delete_transaction(transaction_id):
        """Delete one saved transaction; unknown IDs return a not-found page."""
        if database.delete_transaction(transaction_id) == 0:
            abort(404)
        flash("Transaction deleted.", "success")
        return redirect(url_for("index"))

    return app


def _transaction_from_form():
    """Convert browser form fields into the transaction shape used by database.py."""
    date_text = request.form.get("date", "").strip()
    try:
        # datetime-local submits this ISO-style value; the database accepts a datetime.
        transaction_date = datetime.strptime(date_text, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValueError("Enter a valid transaction date and time") from None

    return {
        "DateTime": transaction_date,
        "Description": request.form.get("description", ""),
        "Category": request.form.get("category", ""),
        "Amount": request.form.get("amount", ""),
        "Type": request.form.get("type", ""),
    }


def _find_transaction(transaction_id):
    """Return a transaction by its database ID, or None if it no longer exists."""
    return next(
        (
            transaction
            for transaction in database.get_all_transactions()
            if transaction["id"] == transaction_id
        ),
        None,
    )


app = create_app()


if __name__ == "__main__":
    # Bind to this computer only; run with `python app.py` from this folder.
    app.run(host="127.0.0.1", port=5000, debug=False)
