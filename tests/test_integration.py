import os
import tempfile
import unittest

import reports
from results import SUBJECTS, calculate_average, get_grade
from storage import Storage
from student import Student, StudentManager


def scores_for(value):
    return {subject: value for subject in SUBJECTS}


class PersistenceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_file = os.path.join(
            self.temp_dir.name, "data", "students.json"
        )
        self.manager = StudentManager(Storage(self.data_file))

    def make_student(self, student_id, full_name):
        return Student(
            student_id,
            full_name,
            "Form 1",
            "Female",
            "2010-01-01",
        )

    def test_records_survive_reloading_from_json(self):
        self.manager.add_student(self.make_student("S001", "Alice Banda"))
        self.manager.add_student(self.make_student("S002", "Bob Phiri"))
        self.manager.update_scores(
            "S001",
            scores_for(80),
            "2026-11-12 10:00:00",
        )

        reloaded_manager = StudentManager(Storage(self.data_file))

        self.assertEqual(len(reloaded_manager.students), 2)
        alice = reloaded_manager.get_student("S001")
        self.assertIsNotNone(alice)
        self.assertEqual(alice.full_name, "Alice Banda")
        self.assertEqual(alice.scores, scores_for(80))
        self.assertEqual(alice.result_date, "2026-11-12 10:00:00")

    def test_updates_and_deletions_persist(self):
        self.manager.add_student(self.make_student("S001", "Alice Banda"))
        self.manager.add_student(self.make_student("S002", "Bob Phiri"))
        self.manager.update_student_info(
            "S001",
            "Alice Updated",
            "Form 2",
            "Female",
            "2010-02-01",
        )
        self.manager.delete_student("S002")

        reloaded_manager = StudentManager(Storage(self.data_file))

        self.assertIsNone(reloaded_manager.get_student("S002"))
        alice = reloaded_manager.get_student("S001")
        self.assertIsNotNone(alice)
        self.assertEqual(alice.full_name, "Alice Updated")
        self.assertEqual(alice.class_form, "Form 2")

    def test_reports_use_persisted_results(self):
        self.manager.add_student(self.make_student("S001", "Alice Banda"))
        self.manager.add_student(self.make_student("S002", "Bob Phiri"))
        self.manager.update_scores(
            "S001",
            scores_for(80),
            "2026-11-12 10:00:00",
        )
        self.manager.update_scores(
            "S002",
            scores_for(60),
            "2026-11-12 10:05:00",
        )

        reloaded_manager = StudentManager(Storage(self.data_file))
        stats = reports.class_statistics(reloaded_manager.students)
        report = reports.format_individual_report(
            reloaded_manager.get_student("S001")
        )

        self.assertEqual(stats["highest_average"], 80.0)
        self.assertEqual(stats["highest_student"], "Alice Banda")
        self.assertEqual(stats["class_average"], 70.0)
        self.assertIn("Alice Banda", report)
        self.assertEqual(
            get_grade(calculate_average(
                reloaded_manager.get_student("S001").scores
            )),
            "A",
        )


if __name__ == "__main__":
    unittest.main()
