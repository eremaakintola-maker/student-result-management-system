import os
from datetime import date, datetime

import reports
from results import (
    SUBJECTS,
    calculate_average,
    calculate_total,
    get_grade,
    parse_score,
)
from storage import Storage
from student import Student, StudentManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def input_text(prompt, default=None):
    while True:
        if default is None:
            label = prompt + ": "
        else:
            label = prompt + " [" + default + "]: "

        value = input(label).strip()
        if value:
            return value
        if default is not None:
            return default
        print("This field cannot be empty.")


def input_gender(default=None):
    while True:
        if default is None:
            label = "Gender (Male/Female/Other): "
        else:
            label = "Gender (Male/Female/Other) [" + default + "]: "

        value = input(label).strip()
        if not value and default is not None:
            return default

        value = value.capitalize()
        if value in ("Male", "Female", "Other"):
            return value
        print("Please enter Male, Female or Other.")


def input_date_of_birth(default=None):
    while True:
        if default is None:
            label = "Date of birth (YYYY-MM-DD): "
        else:
            label = "Date of birth (YYYY-MM-DD) [" + default + "]: "

        value = input(label).strip()
        if not value and default is not None:
            return default

        try:
            birth_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD, for example 2010-05-23.")
        else:
            if birth_date > date.today():
                print("Date of birth cannot be in the future.")
            else:
                return birth_date.isoformat()


def input_score(subject, current=None):
    while True:
        if current is None:
            label = subject + ": "
        else:
            label = subject + " [" + str(current) + "] (Enter to keep): "

        value = input(label).strip()
        if value == "" and current is not None:
            return current

        try:
            return parse_score(value)
        except ValueError as error:
            print("Invalid score. " + str(error))


def show_menu():
    print()
    print("=" * 50)
    print("      STUDENT RESULT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1.  Add a new student")
    print("2.  View all registered students")
    print("3.  Search students by ID or name")
    print("4.  Update student information")
    print("5.  Delete a student record")
    print("6.  Record or update student results")
    print("7.  View an individual report card")
    print("8.  View all results (sorted by average)")
    print("9.  View students (sorted by name)")
    print("10. View class statistics and report")
    print("11. Save a report as a text file")
    print("0.  Exit")
    print("=" * 50)


def add_student(manager):
    print("\n--- Add New Student ---")
    student_id = input_text("Student ID")

    if manager.get_student(student_id) is not None:
        print("Error: A student with ID '" + student_id + "' already exists.")
        return

    full_name = input_text("Full name")
    class_form = input_text("Class/Form")
    gender = input_gender()
    date_of_birth = input_date_of_birth()

    student = Student(student_id, full_name, class_form, gender, date_of_birth)
    try:
        manager.add_student(student)
    except ValueError as error:
        print("Error: " + str(error))
    else:
        print("Success: Student '" + full_name + "' was added and saved.")


def view_students(manager):
    print()
    print(reports.format_student_table(manager.students, "ALL REGISTERED STUDENTS"))


def search_students(manager):
    print("\n--- Search Students ---")
    search_term = input_text("Enter a student ID or name")
    matches = manager.search_students(search_term)

    if not matches:
        print("No students matched '" + search_term + "'.")
    else:
        print()
        print(reports.format_student_table(matches, "SEARCH RESULTS"))


def update_student(manager):
    print("\n--- Update Student Information ---")
    student_id = input_text("Student ID")
    student = manager.get_student(student_id)

    if student is None:
        print("Error: Student with ID '" + student_id + "' was not found.")
        return

    print("Press Enter to keep the current value.")
    full_name = input_text("Full name", student.full_name)
    class_form = input_text("Class/Form", student.class_form)
    gender = input_gender(student.gender)
    date_of_birth = input_date_of_birth(student.date_of_birth)

    try:
        manager.update_student_info(
            student.student_id,
            full_name,
            class_form,
            gender,
            date_of_birth,
        )
    except ValueError as error:
        print("Error: " + str(error))
    else:
        print("Success: Student information was updated and saved.")


def delete_student(manager):
    print("\n--- Delete Student ---")
    student_id = input_text("Student ID")
    student = manager.get_student(student_id)

    if student is None:
        print("Error: Student with ID '" + student_id + "' was not found.")
        return

    confirm = input(
        "Delete " + student.full_name + " (" + student.student_id + ")? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    if manager.delete_student(student.student_id):
        print("Success: Student record was deleted and the data file was updated.")
    else:
        print("Error: The student could not be deleted.")


def record_results(manager):
    print("\n--- Record or Update Results ---")
    student_id = input_text("Student ID")
    student = manager.get_student(student_id)

    if student is None:
        print("Error: Student with ID '" + student_id + "' was not found.")
        return

    if student.scores:
        print("Press Enter to keep an existing score.")

    scores = {}
    for subject in SUBJECTS:
        scores[subject] = input_score(subject, student.scores.get(subject))

    result_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        manager.update_scores(student.student_id, scores, result_date)
    except ValueError as error:
        print("Error: " + str(error))
    else:
        average = calculate_average(scores)
        print("Success: Results were recorded and saved.")
        print("Total   : " + str(calculate_total(scores)))
        print("Average : " + str(average))
        print("Grade   : " + get_grade(average))
        print("Date    : " + result_date)


def view_report_card(manager):
    print("\n--- Individual Report Card ---")
    student_id = input_text("Student ID")
    student = manager.get_student(student_id)

    if student is None:
        print("Error: Student with ID '" + student_id + "' was not found.")
        return

    print()
    print(reports.format_individual_report(student))


def view_results_by_average(manager):
    print()
    if not manager.students:
        print("No student records found.")
        return

    sorted_students = manager.sorted_by_average()
    print(
        reports.format_student_table(
            sorted_students,
            "ALL STUDENTS (SORTED BY AVERAGE, HIGHEST FIRST)",
        )
    )


def view_students_by_name(manager):
    print()
    if not manager.students:
        print("No student records found.")
        return

    print(
        reports.format_student_table(
            manager.sorted_by_name(),
            "ALL STUDENTS (SORTED BY NAME)",
        )
    )


def view_class_report(manager):
    print()
    if not manager.students:
        print("No student records found.")
        return

    print(reports.format_class_report(manager.students))


def safe_filename(text):
    cleaned = ""
    for character in text:
        if character.isalnum() or character in ("-", "_"):
            cleaned += character
        else:
            cleaned += "_"
    if cleaned == "":
        return "report"
    return cleaned


def save_reports(manager):
    print("\n--- Save Report ---")
    if not manager.students:
        print("No student records found.")
        return

    print("1. Save an individual report card")
    print("2. Save the class report")
    choice = input("Choose a report to save: ").strip()

    if choice == "1":
        student_id = input_text("Student ID")
        student = manager.get_student(student_id)

        if student is None:
            print("Error: Student with ID '" + student_id + "' was not found.")
            return

        report_text = reports.format_individual_report(student)
        prefix = "report_card_" + safe_filename(student.student_id)
    elif choice == "2":
        report_text = reports.format_class_report(manager.students)
        prefix = "class_report"
    else:
        print("Invalid choice. No report was saved.")
        return

    try:
        file_path = reports.save_report(report_text, REPORTS_DIR, prefix)
    except OSError as error:
        print("Error: Could not save the report. " + str(error))
    else:
        print("Success: Report saved to:")
        print(file_path)


def main():
    storage = Storage(DATA_FILE)
    manager = StudentManager(storage)

    print("Welcome to the Student Result Management System.")
    print("Loaded " + str(len(manager.students)) + " student record(s).")

    try:
        while True:
            show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Exiting the application...")
                break
            elif choice == "1":
                add_student(manager)
            elif choice == "2":
                view_students(manager)
            elif choice == "3":
                search_students(manager)
            elif choice == "4":
                update_student(manager)
            elif choice == "5":
                delete_student(manager)
            elif choice == "6":
                record_results(manager)
            elif choice == "7":
                view_report_card(manager)
            elif choice == "8":
                view_results_by_average(manager)
            elif choice == "9":
                view_students_by_name(manager)
            elif choice == "10":
                view_class_report(manager)
            elif choice == "11":
                save_reports(manager)
            else:
                print("Invalid option. Please choose a number from the menu.")

            input("\nPress Enter to return to the main menu...")
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user.")
    except Exception as error:
        print("\nAn unexpected error occurred: " + str(error))
    else:
        print("Thank you for using the Student Result Management System.")
    finally:
        if manager.save():
            print("All data has been saved to " + DATA_FILE)
        else:
            print("Warning: Some data may not have been saved.")


if __name__ == "__main__":
    main()
