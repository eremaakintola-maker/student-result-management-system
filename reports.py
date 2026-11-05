import os
from datetime import datetime

from results import (
    SUBJECTS,
    calculate_average,
    calculate_total,
    get_grade,
    get_grade_remark,
)


def _fit(value, width):
    text = str(value)
    if len(text) > width:
        text = text[:width]
    return text.ljust(width)


def _number(value):
    return "{:.2f}".format(value)


def format_student_table(students, title):
    if not students:
        return title + "\nNo student records found."

    header = (
        _fit("ID", 10)
        + _fit("Name", 22)
        + _fit("Class", 14)
        + _fit("Gender", 9)
        + "Total".rjust(9)
        + "Average".rjust(9)
        + "Grade".rjust(7)
    )
    lines = [title, "=" * len(header), header, "-" * len(header)]

    for student in students:
        if student.scores:
            total = _number(calculate_total(student.scores))
            average = calculate_average(student.scores)
            average_text = _number(average)
            grade = get_grade(average)
        else:
            total = "-"
            average_text = "-"
            grade = "-"

        lines.append(
            _fit(student.student_id, 10)
            + _fit(student.full_name, 22)
            + _fit(student.class_form, 14)
            + _fit(student.gender, 9)
            + total.rjust(9)
            + average_text.rjust(9)
            + grade.rjust(7)
        )

    return "\n".join(lines)


def format_individual_report(student):
    lines = [
        "=" * 62,
        "STUDENT REPORT CARD".center(62),
        "=" * 62,
        "Student ID   : " + student.student_id,
        "Full Name    : " + student.full_name,
        "Class/Form   : " + student.class_form,
        "Gender       : " + student.gender,
        "Date of Birth: " + student.date_of_birth,
        "-" * 62,
    ]

    if student.scores:
        lines.append(_fit("Subject", 30) + "Score".rjust(12))
        lines.append("-" * 62)
        for subject in SUBJECTS:
            if subject in student.scores:
                score = _number(student.scores[subject])
            else:
                score = "Not recorded"
            lines.append(_fit(subject, 30) + score.rjust(12))

        average = calculate_average(student.scores)
        grade = get_grade(average)
        lines.extend([
            "-" * 62,
            "Total Score  : " + _number(calculate_total(student.scores)),
            "Average Score: " + _number(average),
            "Grade        : " + grade + " (" + get_grade_remark(grade) + ")",
            "Result Date  : " + (student.result_date or "Not recorded"),
        ])
    else:
        lines.append("No results have been recorded for this student.")

    lines.append("=" * 62)
    return "\n".join(lines)


def class_statistics(students):
    students_with_results = []
    for student in students:
        if student.scores:
            students_with_results.append(student)

    if not students_with_results:
        return {
            "student_count": len(students),
            "with_results": 0,
            "highest_average": 0.0,
            "highest_student": "N/A",
            "lowest_average": 0.0,
            "lowest_student": "N/A",
            "class_average": 0.0,
            "grade_counts": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0},
        }

    highest_student = students_with_results[0]
    lowest_student = students_with_results[0]
    total_average = 0.0
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for student in students_with_results:
        average = calculate_average(student.scores)
        total_average += average
        grade = get_grade(average)
        grade_counts[grade] += 1

        if average > calculate_average(highest_student.scores):
            highest_student = student
        if average < calculate_average(lowest_student.scores):
            lowest_student = student

    return {
        "student_count": len(students),
        "with_results": len(students_with_results),
        "highest_average": calculate_average(highest_student.scores),
        "highest_student": highest_student.full_name,
        "lowest_average": calculate_average(lowest_student.scores),
        "lowest_student": lowest_student.full_name,
        "class_average": round(total_average / len(students_with_results), 2),
        "grade_counts": grade_counts,
    }


def format_class_report(students):
    stats = class_statistics(students)
    lines = [
        "=" * 62,
        "CLASS RESULTS REPORT".center(62),
        "=" * 62,
        "Generated on    : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Total students  : " + str(stats["student_count"]),
        "With results    : " + str(stats["with_results"]),
        "Highest average : " + _number(stats["highest_average"])
        + " (" + stats["highest_student"] + ")",
        "Lowest average  : " + _number(stats["lowest_average"])
        + " (" + stats["lowest_student"] + ")",
        "Class average   : " + _number(stats["class_average"]),
        "-" * 62,
        "Grade distribution:",
    ]

    for grade in ("A", "B", "C", "D", "F"):
        lines.append(
            "  " + grade + " (" + get_grade_remark(grade) + "): "
            + str(stats["grade_counts"][grade])
        )

    lines.append("")
    lines.append(
        format_student_table(
            sorted(
                students,
                key=lambda student: calculate_average(student.scores),
                reverse=True,
            ),
            "ALL STUDENTS (SORTED BY AVERAGE, HIGHEST FIRST)",
        )
    )
    return "\n".join(lines)


def save_report(report_text, reports_directory, prefix):
    os.makedirs(reports_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = prefix + "_" + timestamp + ".txt"
    file_path = os.path.join(reports_directory, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report_text)
    return file_path
