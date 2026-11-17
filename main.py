
import argparse

from gradebook import service
from gradebook.models import validate_grade


def parse_grade(value):
    try:
        return validate_grade(float(value))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Enter a valid grade between 0 and 100."
        )


def main():
    parser = argparse.ArgumentParser(description="Student Gradebook")
    commands = parser.add_subparsers(dest="command", required=True)

    student = commands.add_parser("add-student")
    student.add_argument("--name", required=True)

    course = commands.add_parser("add-course")
    course.add_argument("--code", required=True)
    course.add_argument("--title", required=True)

    enroll = commands.add_parser("enroll")
    enroll.add_argument("--student-id", type=int, required=True)
    enroll.add_argument("--course", required=True)

    grade = commands.add_parser("add-grade")
    grade.add_argument("--student-id", type=int, required=True)
    grade.add_argument("--course", required=True)
    grade.add_argument("--grade", type=parse_grade, required=True)

    listing = commands.add_parser("list")
    listing.add_argument(
        "kind",
        choices=["students", "courses", "enrollments"]
    )
    listing.add_argument("--sort", choices=["name", "code"])

    average = commands.add_parser("avg")
    average.add_argument("--student-id", type=int, required=True)
    average.add_argument("--course", required=True)

    gpa = commands.add_parser("gpa")
    gpa.add_argument("--student-id", type=int, required=True)

    args = parser.parse_args()

    try:
        if args.command == "add-student":
            result = service.add_student(args.name)
            print("Student added. ID:", result)

        elif args.command == "add-course":
            service.add_course(args.code, args.title)
            print("Course added successfully.")

        elif args.command == "enroll":
            service.enroll(args.student_id, args.course)
            print("Student enrolled successfully.")

        elif args.command == "add-grade":
            service.add_grade(
                args.student_id, args.course, args.grade
            )
            print("Grade added successfully.")

        elif args.command == "list":
            if args.kind == "students":
                records = service.list_students()
            elif args.kind == "courses":
                records = service.list_courses()
            else:
                records = service.list_enrollments()

            if args.sort == "name" and args.kind == "students":
                records = sorted(records, key=lambda x: x["name"].lower())
            elif args.sort == "code" and args.kind == "courses":
                records = sorted(records, key=lambda x: x["code"])

            if records:
                for item in records:
                    print(item)
            else:
                print("No records found.")

        elif args.command == "avg":
            result = service.compute_average(
                args.student_id, args.course
            )
            print("Average:", round(result, 2))

        elif args.command == "gpa":
            result = service.compute_gpa(args.student_id)
            print("GPA:", round(result, 2))

    except (ValueError, OSError) as error:
        print("Error:", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
