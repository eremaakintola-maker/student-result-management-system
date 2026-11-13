# Student Result Management System

## Project Description

The Student Result Management System is a menu-driven command-line application
written in Python. It allows a school to register students, record and update
their subject scores, calculate totals, averages and grades, generate individual
and class reports, and save all records permanently using JSON.

The application is intentionally simple and beginner-friendly. It uses only the
Python standard library and no external packages.

## Main Features

### Student Management

- Add a new student with Student ID, Full Name, Class/Form, Gender and Date of Birth.
- View all registered students.
- Search for students by Student ID or name.
- Update student information.
- Delete student records.
- Prevent duplicate Student IDs (case-insensitive).
- Validate all required student fields.
- Validate dates of birth using the YYYY-MM-DD format and reject future dates.

### Result Management

- Record scores for five subjects:
  - Mathematics
  - English
  - Science
  - Social Studies
  - Computer Science
- Update existing scores while keeping unchanged values.
- Automatically calculate total and average scores.
- Assign grades from the average:
  - A: 70-100
  - B: 60-69
  - C: 50-59
  - D: 45-49
  - F: Below 45
- Display an individual student report card.
- Record the date and time each result is entered.
- Reject scores outside the 0-100 range.

### Reporting and Analysis

- Display all students with total scores, averages and grades.
- Sort students by average score from highest to lowest.
- Sort students by student name.
- Display class statistics:
  - Highest average and the student who achieved it
  - Lowest average and the student who achieved it
  - Class average
  - Grade distribution
- Generate individual and class reports.
- Save reports as text files in the `reports` folder.

### Data Persistence

- Store student information and results in `data/students.json`.
- Automatically save after every change.
- Automatically save again when the application exits.
- Load existing records when the application starts.
- Create the `data` folder and data file automatically when needed, and create the `reports` folder when a report is saved.
- Handle missing or invalid JSON data safely.

### User Experience

- Clear numbered main menu.
- Clear success and error messages.
- Input validation throughout the application.
- Graceful handling of missing students.
- Return to the main menu after each operation.
- Exit option from the main menu.

### Automated Testing

- Includes a test suite built with Python's built-in `unittest` module.
- Contains 42 automated tests.
- Covers student management, results, grading, storage, reports and integration.
- Uses temporary test data and does not rely on the real student records.

## Requirements

- Python 3 (tested with Python 3.14).
- No external libraries or packages are required.
- A terminal or command prompt for running the application and tests.
- Write permission in the project folder so JSON data and text reports can be saved.

## Technologies Used

- Python 3 (tested with Python 3.14)
- Python standard library only:
  - `os`
  - `json`
  - `datetime`
  - `unittest`
  - `tempfile`

No external libraries are required.

## Project Structure

```
student_result_system/
    .gitignore
    main.py
    student.py
    results.py
    storage.py
    reports.py
    data/
        students.json
    reports/
        .gitkeep
    tests/
        __init__.py
        test_results.py
        test_student_manager.py
        test_storage.py
        test_reports.py
        test_integration.py
    README.md
```

### Description of Each File

- `main.py` - Runs the command-line application, displays the menu, handles user
  input and connects all other modules together.
- `student.py` - Contains the `Student` class and the `StudentManager` class.
  It handles adding, searching, updating, deleting and sorting students.
- `results.py` - Contains subject definitions and functions for validating
  scores, calculating totals and averages, and assigning grades.
- `storage.py` - Contains the `Storage` class, which loads and saves all records
  using JSON.
- `reports.py` - Builds student tables, individual report cards, class reports
  and class statistics, and saves reports as text files.
- `tests/__init__.py` - Marks the tests folder as a Python package.
- `tests/test_results.py` - Tests score validation, totals, averages and grades.
- `tests/test_student_manager.py` - Tests student registration, duplicate
  prevention, searching, updating, deleting, score recording and sorting.
- `tests/test_storage.py` - Tests JSON saving and loading, missing files and
  invalid JSON handling.
- `tests/test_reports.py` - Tests report cards, student tables and class
  statistics.
- `tests/test_integration.py` - Tests persistence and report generation across
  multiple application manager instances.
- `data/students.json` - Stores the application's student and result records.
- `reports/` - Stores generated report text files.
- `README.md` - Provides project documentation and usage instructions.

## How to Run the Application

1. Open a terminal or command prompt.
2. Move into the project folder:

   ```
   cd student_result_system
   ```

3. Start the command-line application:

   ```
   python main.py
   ```

4. Choose an option from the numbered menu and follow the prompts.
5. Choose option `0` to exit. All data is saved automatically.

Note: On some systems the command may be `python3 main.py`.

## How to Run the Automated Tests

1. Open a terminal or command prompt.
2. Move into the project folder.
3. Run the full test suite:

   ```
   python -m unittest discover -s tests -v
   ```

The suite currently contains 42 tests. On a successful run, the output includes
`Ran 42 tests in ...` and ends with `OK`.

The tests use temporary files and temporary data folders. They do not modify
`data/students.json` or use real student records.

## Test Suite Coverage

The 42 automated tests cover:

- Student registration and duplicate ID prevention.
- Searching for students by ID, partial ID and name.
- Updating student information.
- Deleting student records.
- Recording and updating examination scores.
- Total and average calculations.
- Grade assignment and grade boundaries.
- Invalid score and out-of-range score handling.
- Individual report card generation.
- Student result tables.
- Class statistics.
- Sorting students by average and name.
- Saving and loading student records with JSON.
- Handling missing and invalid JSON files.
- Persistence across application restarts.
- Report generation using persisted records.

## How Data Is Stored

Student records are stored in `data/students.json` in this format:

```json
{
  "students": [
    {
      "student_id": "S001",
      "full_name": "John Doe",
      "class_form": "Form 1",
      "gender": "Male",
      "date_of_birth": "2010-05-23",
      "scores": {
        "Mathematics": 80,
        "English": 75,
        "Science": 70,
        "Social Studies": 65,
        "Computer Science": 90
      },
      "result_date": "2026-11-04 10:30:00"
    }
  ]
}
```

## Python Concepts Demonstrated

- Variables and data types (strings, integers, floats, lists, dictionaries, booleans)
- Type conversion using `float()` for score parsing and `str()` for display and text output
- Conditional statements (`if`, `elif`, `else`)
- `for` and `while` loops
- Lists, tuples and dictionaries
- Functions with parameters and return values
- Sorting using `sorted()` with `key` functions
- Exception handling using `try`, `except`, `else` and `finally`
- File handling for reading and writing text and JSON files
- JSON serialization and deserialization using the `json` module
- Object-Oriented Programming using the `Student`, `StudentManager` and `Storage` classes
- Date and time handling using the `datetime` module
- Standard library modules: `os`, `json`, `datetime`, `unittest` and `tempfile`
- Automated testing with `unittest`
