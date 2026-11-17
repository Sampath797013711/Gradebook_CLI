"""Gradebook business operations."""

from .models import Student, Course, Enrollment, validate_grade
from .storage import load_data, save_data


def add_student(name: str, path=None) -> int:
    """Add a student and return the newly assigned ID."""
    data = load_data(path) if path else load_data()
    student_id = max((student["id"] for student in data["students"]), default=0) + 1
    student = Student(student_id, name)
    data["students"].append({"id": student.id, "name": student.name})
    save_data(data, path) if path else save_data(data)
    return student_id


def add_course(code: str, title: str, path=None) -> None:
    """Add a course, rejecting duplicate course codes."""
    data = load_data(path) if path else load_data()
    course = Course(code, title)
    if any(item["code"] == course.code for item in data["courses"]):
        raise ValueError(f"Course {course.code} already exists.")
    data["courses"].append({"code": course.code, "title": course.title})
    save_data(data, path) if path else save_data(data)


def enroll(student_id: int, course_code: str, path=None) -> None:
    """Enroll an existing student in an existing course."""
    data = load_data(path) if path else load_data()
    code = course_code.strip().upper()
    if not any(s["id"] == student_id for s in data["students"]):
        raise ValueError(f"Student ID {student_id} does not exist.")
    if not any(c["code"] == code for c in data["courses"]):
        raise ValueError(f"Course {code} does not exist.")
    if any(e["student_id"] == student_id and e["course_code"] == code
           for e in data["enrollments"]):
        raise ValueError("This student is already enrolled in that course.")
    enrollment = Enrollment(student_id, code)
    data["enrollments"].append({
        "student_id": enrollment.student_id,
        "course_code": enrollment.course_code,
        "grades": enrollment.grades,
    })
    save_data(data, path) if path else save_data(data)


def add_grade(student_id: int, course_code: str, grade: int | float, path=None) -> None:
    """Add a validated grade to an existing enrollment."""
    grade_value = validate_grade(grade)
    data = load_data(path) if path else load_data()
    code = course_code.strip().upper()
    enrollment = next((e for e in data["enrollments"]
                       if e["student_id"] == student_id and e["course_code"] == code), None)
    if enrollment is None:
        raise ValueError("Student is not enrolled in that course.")
    enrollment["grades"].append(grade_value)
    save_data(data, path) if path else save_data(data)


def list_students(path=None) -> list[dict]:
    """Return students sorted by name."""
    data = load_data(path) if path else load_data()
    return sorted(data["students"], key=lambda item: item["name"].lower())


def list_courses(path=None) -> list[dict]:
    """Return courses sorted by course code."""
    data = load_data(path) if path else load_data()
    return sorted(data["courses"], key=lambda item: item["code"])


def list_enrollments(path=None) -> list[dict]:
    """Return enrollments sorted by student ID and course code."""
    data = load_data(path) if path else load_data()
    return sorted(data["enrollments"],
                  key=lambda item: (item["student_id"], item["course_code"]))


def compute_average(student_id: int, course_code: str, path=None) -> float:
    """Compute the arithmetic mean for one student's course grades."""
    data = load_data(path) if path else load_data()
    code = course_code.strip().upper()
    enrollment = next((e for e in data["enrollments"]
                       if e["student_id"] == student_id and e["course_code"] == code), None)
    if enrollment is None:
        raise ValueError("Student is not enrolled in that course.")
    if not enrollment["grades"]:
        raise ValueError("No grades have been recorded for this enrollment.")
    return sum(enrollment["grades"]) / len(enrollment["grades"])


def compute_gpa(student_id: int, path=None) -> float:
    """Compute the simple mean of the student's course averages."""
    data = load_data(path) if path else load_data()
    if not any(s["id"] == student_id for s in data["students"]):
        raise ValueError(f"Student ID {student_id} does not exist.")
    enrollments = [e for e in data["enrollments"]
                   if e["student_id"] == student_id and e["grades"]]
    if not enrollments:
        raise ValueError("No graded courses found for this student.")
    averages = [sum(e["grades"]) / len(e["grades"]) for e in enrollments]
    return sum(averages) / len(averages)
