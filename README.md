# Gradebook CLI

A small command-line gradebook built with Python's standard library. It stores students, courses, enrollments, and grades in JSON.

## Project structure

```text
gradebook/
├── gradebook/
│   ├── __init__.py
│   ├── models.py
│   ├── service.py
│   └── storage.py
├── scripts/
│   └── seed.py
├── tests/
│   └── test_service.py
├── data/
│   └── gradebook.json
├── logs/
├── main.py
└── README.md
```

## Setup

Python 3.10 or newer is recommended. From the project root:

```bash
python -m venv .venv
```

Activate it:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

There are no third-party dependencies.

## Seed sample data

Run from the project root:

```bash
python -m scripts.seed
```

This creates three students, two courses, six enrollments, and sample grades in `data/gradebook.json`. Run it only against a fresh data file; it appends records.

## CLI usage

```bash
python main.py add-student --name "Alex Morgan"
# Added student with ID: 4

python main.py add-course --code CS101 --title "Intro to CS"
# Added course CS101.

python main.py enroll --student-id 4 --course CS101
# Student 4 enrolled in CS101.

python main.py add-grade --student-id 4 --course CS101 --grade 95
# Recorded grade 95 for student 4.

python main.py list students --sort name
# {'id': 1, 'name': 'Aarav Sharma'}
# ...

python main.py list courses --sort code
python main.py list enrollments
python main.py avg --student-id 1 --course CS101
# Average: 90.00

python main.py gpa --student-id 1
# GPA (simple course-average mean): 88.75
```

The sample IDs above assume a fresh seed file. `avg` and `gpa` print numeric means on a 0–100 scale.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Design decisions & limitations

- JSON is used for simple local persistence; it is not designed for concurrent writers or large datasets.
- Student IDs are sequential integers generated from the current data.
- Course codes are normalized to uppercase; names and titles are trimmed.
- GPA is the unweighted arithmetic mean of the student's available course averages, not a credit-weighted or 4.0-scale GPA.
- A course average requires at least one recorded grade. GPA ignores enrollments with no grades.
- Service functions accept an optional file path to make tests independent and repeatable.
- The CLI is intended to be run from the project root so the default `data/` and `logs/` paths resolve consistently.
