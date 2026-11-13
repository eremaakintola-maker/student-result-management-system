import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from storage import Storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_file = os.path.join(
            self.temp_dir.name, "data", "students.json"
        )
        self.storage = Storage(self.data_file)

    def test_missing_data_file_and_folder_are_created(self):
        self.assertTrue(os.path.exists(self.data_file))
        self.assertEqual(self.storage.load_students(), [])

        with open(self.data_file, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, {"students": []})

    def test_save_and_load_records_round_trip(self):
        records = [
            {
                "student_id": "T001",
                "full_name": "Test Student",
                "class_form": "Form 1",
                "gender": "Female",
                "date_of_birth": "2010-01-01",
                "scores": {"Mathematics": 80},
                "result_date": "2026-11-12 10:00:00",
            }
        ]

        self.assertTrue(self.storage.save_students(records))
        self.assertEqual(self.storage.load_students(), records)

        with open(self.data_file, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data["students"], records)

    def test_load_returns_empty_list_when_file_is_missing(self):
        os.remove(self.data_file)

        self.assertEqual(self.storage.load_students(), [])

    def test_load_invalid_json_returns_empty_list_and_warns(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            file.write("{not valid json")

        output = io.StringIO()
        with redirect_stdout(output):
            records = self.storage.load_students()

        self.assertEqual(records, [])
        self.assertIn("not valid JSON", output.getvalue())

    def test_load_invalid_students_shape_returns_empty_list(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump({"students": "not a list"}, file)

        self.assertEqual(self.storage.load_students(), [])

    def test_load_supports_top_level_list_format(self):
        records = [
            {
                "student_id": "T002",
                "full_name": "List Format Student",
            }
        ]
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(records, file)

        self.assertEqual(self.storage.load_students(), records)


if __name__ == "__main__":
    unittest.main()
