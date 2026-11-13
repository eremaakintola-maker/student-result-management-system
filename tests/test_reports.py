import os
import tempfile
import unittest

import reports
from results import SUBJECTS
from student import Student


def scores_for(value):
    return {subject: value for subject in SUBJECTS}


def make_student(student_id, full_name, scores=None, result_date=""):
    return Student(
        student_id,
        full_name,
        "Form 1",
        "Female",
        "2010-01-01",
        scores if scores is not None else {},
        result_date,
    )


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.alice = make_student(
            "S001",
            "Alice Banda",
            scores_for(80),
            "2026-11-12 10:00:00",
        )
        self.bob = make_student(
            "S002",
            "Bob Phiri",
            scores_for(60),
            "2026-11-12 10:05:00",
        )
        self.carol = make_student("S003", "Carol Mwale")

    def test_individual_report_with_scores(self):
        report = reports.format_individual_report(self.alice)

        self.assertIn("STUDENT REPORT CARD", report)
        self.assertIn("S001", report)
        self.assertIn("Alice Banda", report)
        self.assertIn("Form 1", report)

        for subject in SUBJECTS:
            self.assertIn(subject, report)

        self.assertIn("Total Score  : 400.00", report)
        self.assertIn("Average Score: 80.00", report)
        self.assertIn("Grade        : A (Excellent)", report)
        self.assertIn("Result Date  : 2026-11-12 10:00:00", report)

    def test_individual_report_without_scores(self):
        report = reports.format_individual_report(self.carol)

        self.assertIn("No results have been recorded for this student.", report)

    def test_student_table_contains_results_and_missing_state(self):
        table = reports.format_student_table(
            [self.alice, self.carol],
            "TEST RESULTS",
        )

        self.assertIn("TEST RESULTS", table)
        self.assertIn("S001", table)
        self.assertIn("400.00", table)
        self.assertIn("80.00", table)
        self.assertIn("A", table)
        self.assertIn("S003", table)
        self.assertIn("-", table)

    def test_student_table_with_no_students(self):
        table = reports.format_student_table([], "EMPTY TABLE")

        self.assertIn("No student records found.", table)

    def test_class_statistics(self):
        stats = reports.class_statistics([self.alice, self.bob, self.carol])

        self.assertEqual(stats["student_count"], 3)
        self.assertEqual(stats["with_results"], 2)
        self.assertEqual(stats["highest_average"], 80.0)
        self.assertEqual(stats["highest_student"], "Alice Banda")
        self.assertEqual(stats["lowest_average"], 60.0)
        self.assertEqual(stats["lowest_student"], "Bob Phiri")
        self.assertEqual(stats["class_average"], 70.0)
        self.assertEqual(
            stats["grade_counts"],
            {"A": 1, "B": 1, "C": 0, "D": 0, "F": 0},
        )

    def test_class_statistics_without_results(self):
        stats = reports.class_statistics([self.carol])

        self.assertEqual(stats["student_count"], 1)
        self.assertEqual(stats["with_results"], 0)
        self.assertEqual(stats["highest_average"], 0.0)
        self.assertEqual(stats["highest_student"], "N/A")
        self.assertEqual(stats["lowest_average"], 0.0)
        self.assertEqual(stats["lowest_student"], "N/A")
        self.assertEqual(stats["class_average"], 0.0)
        self.assertEqual(
            stats["grade_counts"],
            {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0},
        )

    def test_class_report_is_sorted_by_average(self):
        report = reports.format_class_report([self.bob, self.alice])

        self.assertIn("CLASS RESULTS REPORT", report)
        self.assertIn("Highest average : 80.00 (Alice Banda)", report)
        self.assertIn("Lowest average  : 60.00 (Bob Phiri)", report)
        self.assertIn("Class average   : 70.00", report)
        self.assertLess(report.index("Alice Banda"), report.index("Bob Phiri"))

    def test_save_report_writes_text_file(self):
        with tempfile.TemporaryDirectory() as reports_dir:
            file_path = reports.save_report(
                "REPORT CONTENT",
                reports_dir,
                "test_report",
            )

            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.basename(file_path).startswith("test_report_"))
            self.assertTrue(file_path.endswith(".txt"))

            with open(file_path, "r", encoding="utf-8") as file:
                self.assertEqual(file.read(), "REPORT CONTENT")


if __name__ == "__main__":
    unittest.main()
