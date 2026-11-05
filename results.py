SUBJECTS = (
    "Mathematics",
    "English",
    "Science",
    "Social Studies",
    "Computer Science",
)


def parse_score(value):
    try:
        score = float(value)
    except (TypeError, ValueError):
        raise ValueError("The score must be a number.")

    if score < 0 or score > 100:
        raise ValueError("The score must be between 0 and 100.")

    return round(score, 2)


def calculate_total(scores):
    total = 0
    for subject in SUBJECTS:
        total += scores.get(subject, 0)
    return round(total, 2)


def calculate_average(scores):
    recorded_scores = []
    for subject in SUBJECTS:
        if subject in scores:
            recorded_scores.append(scores[subject])

    if not recorded_scores:
        return 0.0

    total = sum(recorded_scores)
    return round(total / len(recorded_scores), 2)


def get_grade(average):
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    else:
        return "F"


def get_grade_remark(grade):
    remarks = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Pass",
        "F": "Fail",
    }
    return remarks.get(grade, "Unknown")
