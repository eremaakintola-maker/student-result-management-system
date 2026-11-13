import os
import tempfile
import unittest

from results import SUBJECTS
from storage import Storage
from student import Student, StudentManager


def scores_for(value):
    return {subject: value for subject in SUBJECTS}


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_file = os.path.join(
            self.temp_dir.name, "data", "students.json"
        )
        self.storage = Storage(self.data_file)
        self.manager = StudentManager(self.storage)

    def make_student(self, student_id="S001", full_name="Alice Banda",
                     class_form="Form 1", gender="Female",
                     date_of_birth="2010-01-15"):
        return Student(
            student_id,
            full_name,
            class_form,
            gender,
            date_of_birth,
        )

    def test_add_student_and_get_student(self):
        student = self.make_student()
        self.manager.add_student(student)

        self.assertEqual(len(self.manager.students), 1)
        self.assertIs(self.manager.get_student("S001"), student)

    def test_duplicate_student_id_is_rejected_case_insensitively(self):
        self.manager.add_student(self.make_student())
        duplicate = self.make_student(
            student_id="s001",
            full_name="Different Student",
        )

        with self.assertRaisesRegex(ValueError, "already exists"):
            self.manager.add_student(duplicate)

        self.assertEqual(len(self.manager.students), 1)

    def test_get_student_is_case_insensitive(self):
        student = self.make_student()
        self.manager.add_student(student)

        self.assertIs(self.manager.get_student("s001"), student)
        self.assertIsNone(self.manager.get_student("S999"))

    def test_search_by_partial_id_and_name(self):
        alice = self.make_student("S001", "Alice Banda")
        bob = self.make_student("S002", "Bob Phiri")
        self.manager.add_student(alice)
        self.manager.add_student(bob)

        self.assertEqual(
            {student.student_id for student in self.manager.search_students("S00")},
            {"S001", "S002"},
        )
        self.assertEqual(self.manager.search_students("alice"), [alice])
        self.assertEqual(self.manager.search_students("phiri"), [bob])
        self.assertEqual(self.manager.search_students("nobody"), [])

    def test_update_student_information(self):
        self.manager.add_student(self.make_student())

        updated = self.manager.update_student_info(
            "s001",
            "Alice Updated",
            "Form 2",
            "Female",
            "2010-02-20",
        )

        self.assertEqual(updated.full_name, "Alice Updated")
        self.assertEqual(updated.class_form, "Form 2")
        self.assertEqual(updated.gender, "Female")
        self.assertEqual(updated.date_of_birth, "2010-02-20")
        self.assertEqual(self.manager.get_student("S001").full_name, "Alice Updated")

    def test_update_missing_student_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Student not found"):
            self.manager.update_student_info(
                "S999",
                "Missing Student",
                "Form 1",
                "Male",
                "2010-01-01",
            )

    def test_delete_student(self):
        self.manager.add_student(self.make_student("S001", "Alice Banda"))
        self.manager.add_student(self.make_student("S002", "Bob Phiri"))

        self.assertTrue(self.manager.delete_student("s001"))
        self.assertIsNone(self.manager.get_student("S001"))
        self.assertEqual(len(self.manager.students), 1)
        self.assertFalse(self.manager.delete_student("S999"))

    def test_record_and_update_scores(self):
        self.manager.add_student(self.make_student())
        scores = scores_for(75)
        result_date = "2026-11-12 10:00:00"

        updated = self.manager.update_scores("S001", scores, result_date)

        self.assertEqual(updated.scores, scores)
        self.assertEqual(updated.result_date, result_date)

        new_scores = scores_for(90)
        new_date = "2026-11-12 11:00:00"
        self.manager.update_scores("S001", new_scores, new_date)

        self.assertEqual(self.manager.get_student("S001").scores, new_scores)
        self.assertEqual(self.manager.get_student("S001").result_date, new_date)

    def test_update_scores_for_missing_student_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Student not found"):
            self.manager.update_scores("S999", scores_for(70), "2026-11-12")

    def test_sorted_by_average_highest_first(self):
        self.manager.add_student(self.make_student("S001", "Alice Banda"))
        self.manager.add_student(self.make_student("S002", "Bob Phiri"))
        self.manager.add_student(self.make_student("S003", "Carol Mwale"))
        self.manager.update_scores("S001", scores_for(80), "2026-11-12")
        self.manager.update_scores("S002", scores_for(60), "2026-11-12")
        self.manager.update_scores("S003", scores_for(70), "2026-11-12")

        ordered = self.manager.sorted_by_average()

        self.assertEqual(
            [student.student_id for student in ordered],
            ["S001", "S003", "S002"],
        )

    def test_sorted_by_name_is_case_insensitive(self):
        self.manager.add_student(self.make_student("S001", "bob Phiri"))
        self.manager.add_student(self.make_student("S002", "Alice Banda"))
        self.manager.add_student(self.make_student("S003", "Carol Mwale"))

        ordered = self.manager.sorted_by_name()

        self.assertEqual(
            [student.full_name for student in ordered],
            ["Alice Banda", "bob Phiri", "Carol Mwale"],
        )

    def test_student_dictionary_round_trip(self):
        student = self.make_student()
        student.scores = scores_for(88)
        student.result_date = "2026-11-12 12:00:00"

        restored = Student.from_dict(student.to_dict())

        self.assertEqual(restored.student_id, student.student_id)
        self.assertEqual(restored.full_name, student.full_name)
        self.assertEqual(restored.class_form, student.class_form)
        self.assertEqual(restored.gender, student.gender)
        self.assertEqual(restored.date_of_birth, student.date_of_birth)
        self.assertEqual(restored.scores, student.scores)
        self.assertEqual(restored.result_date, student.result_date)

    def test_from_dict_handles_invalid_scores_shape(self):
        restored = Student.from_dict({
            "student_id": "S001",
            "full_name": "Alice Banda",
            "scores": "not a dictionary",
        })

        self.assertEqual(restored.scores, {})


if __name__ == "__main__":
    unittest.main()
