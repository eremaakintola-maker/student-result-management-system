import json
import os


class Storage:
    def __init__(self, data_file):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        directory = os.path.dirname(self.data_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.data_file):
            self.save_students([])

    def load_students(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: The data file is not valid JSON. Starting with no records.")
            return []
        else:
            if isinstance(data, dict):
                students = data.get("students", [])
            elif isinstance(data, list):
                students = data
            else:
                students = []
            if not isinstance(students, list):
                return []
            return students

    def save_students(self, student_records):
        try:
            directory = os.path.dirname(self.data_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            temp_file = self.data_file + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump({"students": student_records}, file, indent=2, ensure_ascii=False)
            os.replace(temp_file, self.data_file)
        except (OSError, TypeError) as error:
            print("Error: Could not save student data. " + str(error))
            return False
        else:
            return True
