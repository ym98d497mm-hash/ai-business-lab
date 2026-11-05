import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

APP_PATH = (
    Path(__file__).resolve().parents[1]
    / "projects"
    / "customer-tracker"
    / "app.py"
)

spec = importlib.util.spec_from_file_location("customer_tracker", APP_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class CustomerTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)

        self.data_file = (
            Path(self.temp_directory.name) / "customers.json"
        )
        data_patch = patch.object(app, "DATA_FILE", self.data_file)
        data_patch.start()
        self.addCleanup(data_patch.stop)

        self.customers = [
            {
                "name": "Alex Smith",
                "phone": "785-555-0101",
                "notes": "Photo inquiry",
            },
            {
                "name": "Jordan Lee",
                "phone": "785-555-0102",
                "notes": "",
            },
        ]

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(app.load_customers(), [])

    def test_save_and_reload_customers(self):
        app.save_customers(self.customers)
        self.assertEqual(app.load_customers(), self.customers)

    def test_invalid_json_is_rejected(self):
        self.data_file.write_text("broken JSON", encoding="utf-8")
        with self.assertRaises(ValueError):
            app.load_customers()

    def test_invalid_record_is_rejected(self):
        self.data_file.write_text(
            '[{"name": "Alex"}]', encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            app.load_customers()

    def test_blank_input_is_retried_and_spaces_removed(self):
        with patch("builtins.input", side_effect=["", "  ", " Alex "]):
            with redirect_stdout(io.StringIO()):
                result = app.required_input("Name: ")
        self.assertEqual(result, "Alex")

    def test_add_customer_saves_optional_blank_notes(self):
        customers = []
        with patch(
            "builtins.input",
            side_effect=[" Alex Smith ", " 785-555-0101 ", ""],
        ):
            with redirect_stdout(io.StringIO()):
                app.add_customer(customers)

        expected = [{
            "name": "Alex Smith",
            "phone": "785-555-0101",
            "notes": "",
        }]
        self.assertEqual(customers, expected)
        self.assertEqual(app.load_customers(), expected)

    def test_search_matches_partial_name_ignoring_case(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="SMI"):
            with redirect_stdout(output):
                app.search_customers(self.customers)

        self.assertIn("Alex Smith", output.getvalue())
        self.assertNotIn("Jordan Lee", output.getvalue())

    def test_search_reports_no_matches(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="Nobody"):
            with redirect_stdout(output):
                app.search_customers(self.customers)

        self.assertIn("No customers found.", output.getvalue())

    def test_failed_save_does_not_add_customer(self):
        customers = []
        with patch(
            "builtins.input",
            side_effect=["Alex", "785-555-0101", ""],
        ):
            with patch.object(
                app, "save_customers", side_effect=OSError("Test failure")
            ):
                with redirect_stdout(io.StringIO()):
                    app.add_customer(customers)

        self.assertEqual(customers, [])

    def test_damaged_file_is_preserved_when_app_starts(self):
        original = "broken JSON"
        self.data_file.write_text(original, encoding="utf-8")

        with patch("builtins.input") as mock_input:
            with redirect_stdout(io.StringIO()):
                app.main()

        mock_input.assert_not_called()
        self.assertEqual(
            self.data_file.read_text(encoding="utf-8"), original
        )


if __name__ == "__main__":
    unittest.main()