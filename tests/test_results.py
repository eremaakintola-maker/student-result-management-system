import unittest

from results import (
    SUBJECTS,
    calculate_average,
    calculate_total,
    get_grade,
    get_grade_remark,
    parse_score,
)


class ScoreValidationTests(unittest.TestCase):
    def test_valid_score_strings_are_converted_to_floats(self):
        cases = {
            "0": 0.0,
            "45": 45.0,
            "69.5": 69.5,
            "100": 100.0,
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(parse_score(value), expected)

    def test_numeric_score_is_accepted(self):
        self.assertEqual(parse_score(80), 80.0)

    def test_invalid_scores_raise_value_error(self):
        invalid_values = ("abc", "", -1, 101, "100.01", None, [])

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_score(value)

    def test_score_is_rounded_to_two_decimal_places(self):
        self.assertEqual(parse_score("75.556"), 75.56)


class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.full_scores = {
            "Mathematics": 80,
            "English": 80,
            "Science": 80,
            "Social Studies": 80,
            "Computer Science": 80,
        }

    def test_subjects_contains_five_subjects(self):
        self.assertEqual(len(SUBJECTS), 5)

    def test_total_score_for_all_subjects(self):
        self.assertEqual(calculate_total(self.full_scores), 400.0)

    def test_average_score_for_all_subjects(self):
        self.assertEqual(calculate_average(self.full_scores), 80.0)

    def test_total_and_average_for_partial_results(self):
        scores = {
            "Mathematics": 80,
            "English": 90,
        }

        self.assertEqual(calculate_total(scores), 170.0)
        self.assertEqual(calculate_average(scores), 85.0)

    def test_average_of_empty_scores_is_zero(self):
        self.assertEqual(calculate_average({}), 0.0)

    def test_unknown_subjects_are_ignored(self):
        scores = dict(self.full_scores)
        scores["Art"] = 100

        self.assertEqual(calculate_total(scores), 400.0)
        self.assertEqual(calculate_average(scores), 80.0)


class GradeTests(unittest.TestCase):
    def test_grade_boundaries(self):
        cases = {
            100: "A",
            70: "A",
            69.99: "B",
            60: "B",
            59.99: "C",
            50: "C",
            49.99: "D",
            45: "D",
            44.99: "F",
            0: "F",
        }

        for average, expected in cases.items():
            with self.subTest(average=average):
                self.assertEqual(get_grade(average), expected)

    def test_grade_remarks(self):
        self.assertEqual(get_grade_remark("A"), "Excellent")
        self.assertEqual(get_grade_remark("B"), "Very Good")
        self.assertEqual(get_grade_remark("C"), "Good")
        self.assertEqual(get_grade_remark("D"), "Pass")
        self.assertEqual(get_grade_remark("F"), "Fail")
        self.assertEqual(get_grade_remark("X"), "Unknown")


if __name__ == "__main__":
    unittest.main()
