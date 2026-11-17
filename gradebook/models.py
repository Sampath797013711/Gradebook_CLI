"""Gradebook data models."""


class Student:
    def __init__(self, student_id: int, name: str):
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("Student ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")
        self.id = student_id
        self.name = name.strip()

    def __str__(self) -> str:
        return f"Student(id={self.id}, name={self.name})"


class Course:
    def __init__(self, code: str, title: str):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title cannot be empty.")
        self.code = code.strip().upper()
        self.title = title.strip()

    def __str__(self) -> str:
        return f"Course(code={self.code}, title={self.title})"


class Enrollment:
    def __init__(self, student_id: int, course_code: str, grades: list | None = None):
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("Student ID must be a positive integer.")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code cannot be empty.")
        self.student_id = student_id
        self.course_code = course_code.strip().upper()
        self.grades = []
        for grade in grades or []:
            self.grades.append(validate_grade(grade))

    def __str__(self) -> str:
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code={self.course_code}, grades={self.grades})"
        )


def validate_grade(grade: int | float) -> float:
    if isinstance(grade, bool) or not isinstance(grade, (int, float)):
        raise ValueError("Grade must be a number between 0 and 100.")
    if not 0 <= grade <= 100:
        raise ValueError("Grade must be between 0 and 100.")
    return float(grade)
