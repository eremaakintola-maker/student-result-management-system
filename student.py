from results import calculate_average


class Student:
    def __init__(self, student_id, full_name, class_form, gender, date_of_birth,
                 scores=None, result_date=""):
        self.student_id = student_id
        self.full_name = full_name
        self.class_form = class_form
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.scores = scores if scores is not None else {}
        self.result_date = result_date

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_form": self.class_form,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": dict(self.scores),
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        scores = data.get("scores") or {}
        if not isinstance(scores, dict):
            scores = {}
        return cls(
            data.get("student_id", ""),
            data.get("full_name", ""),
            data.get("class_form", ""),
            data.get("gender", ""),
            data.get("date_of_birth", ""),
            scores,
            data.get("result_date", ""),
        )


class StudentManager:
    def __init__(self, storage):
        self.storage = storage
        self.students = []
        for record in storage.load_students():
            self.students.append(Student.from_dict(record))

    def save(self):
        records = []
        for student in self.students:
            records.append(student.to_dict())
        return self.storage.save_students(records)

    def get_student(self, student_id):
        for student in self.students:
            if student.student_id.casefold() == student_id.casefold():
                return student
        return None

    def add_student(self, student):
        if self.get_student(student.student_id) is not None:
            raise ValueError(
                "A student with ID '" + student.student_id + "' already exists."
            )
        self.students.append(student)
        self.save()

    def search_students(self, search_term):
        term = search_term.casefold()
        matches = []
        for student in self.students:
            if (term in student.student_id.casefold()
                    or term in student.full_name.casefold()):
                matches.append(student)
        return matches

    def update_student_info(self, student_id, full_name, class_form, gender,
                            date_of_birth):
        student = self.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")

        student.full_name = full_name
        student.class_form = class_form
        student.gender = gender
        student.date_of_birth = date_of_birth
        self.save()
        return student

    def delete_student(self, student_id):
        student = self.get_student(student_id)
        if student is None:
            return False
        self.students.remove(student)
        self.save()
        return True

    def update_scores(self, student_id, scores, result_date):
        student = self.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")
        student.scores = dict(scores)
        student.result_date = result_date
        self.save()
        return student

    def sorted_by_average(self):
        by_name = sorted(self.students, key=lambda student: student.full_name.casefold())
        return sorted(
            by_name,
            key=lambda student: calculate_average(student.scores),
            reverse=True,
        )

    def sorted_by_name(self):
        return sorted(self.students, key=lambda student: student.full_name.casefold())
