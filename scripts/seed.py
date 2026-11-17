"""Populate the default gradebook with sample records."""

from gradebook import service


def seed() -> None:
    """Create a small sample gradebook."""
    # The script is intended for a fresh data/gradebook.json file.
    students = [
        service.add_student("Aarav Sharma"),
        service.add_student("Maya Iyer"),
        service.add_student("Rohan Das"),
    ]
    service.add_course("CS101", "Introduction to Computer Science")
    service.add_course("EE201", "Circuit Analysis")
    for student_id in students:
        service.enroll(student_id, "CS101")
        service.enroll(student_id, "EE201")
    sample_grades = {
        (students[0], "CS101"): [92, 88],
        (students[0], "EE201"): [85, 90],
        (students[1], "CS101"): [95, 91],
        (students[1], "EE201"): [89, 93],
        (students[2], "CS101"): [78, 82],
        (students[2], "EE201"): [86, 80],
    }
    for (student_id, course), grades in sample_grades.items():
        for grade in grades:
            service.add_grade(student_id, course, grade)
    print("Seed data created in data/gradebook.json.")


if __name__ == "__main__":
    seed()
