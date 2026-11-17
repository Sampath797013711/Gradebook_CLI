"""Unit tests for gradebook service operations."""

import tempfile
import unittest
from pathlib import Path

from gradebook import service


class GradebookServiceTests(unittest.TestCase):
    """Test core gradebook operations using an isolated JSON file."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "gradebook.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_student_returns_id(self):
        student_id = service.add_student("Test Student", self.data_path)
        self.assertEqual(student_id, 1)
        self.assertEqual(service.list_students(self.data_path)[0]["name"], "Test Student")

    def test_add_grade_and_compute_average(self):
        student_id = service.add_student("Test Student", self.data_path)
        service.add_course("CS101", "Intro to CS", self.data_path)
        service.enroll(student_id, "CS101", self.data_path)
        service.add_grade(student_id, "CS101", 80, self.data_path)
        service.add_grade(student_id, "CS101", 100, self.data_path)
        self.assertEqual(service.compute_average(student_id, "CS101", self.data_path), 90)

    def test_add_grade_rejects_unenrolled_student(self):
        service.add_student("Test Student", self.data_path)
        service.add_course("CS101", "Intro to CS", self.data_path)
        with self.assertRaises(ValueError):
            service.add_grade(1, "CS101", 75, self.data_path)

    def test_invalid_grade_is_rejected(self):
        with self.assertRaises(ValueError):
            service.add_grade(1, "CS101", 105, self.data_path)


if __name__ == "__main__":
    unittest.main()
