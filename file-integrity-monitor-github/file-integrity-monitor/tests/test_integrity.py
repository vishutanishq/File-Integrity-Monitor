import hashlib
import tempfile
import unittest
from pathlib import Path

from main import calculate_sha256, compare_files


class FileIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.file_a = self.root / "a.txt"
        self.file_b = self.root / "b.txt"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sha256_matches_standard_library_result(self):
        content = b"integrity test data"
        self.file_a.write_bytes(content)
        self.assertEqual(calculate_sha256(self.file_a), hashlib.sha256(content).hexdigest())

    def test_identical_files_match(self):
        self.file_a.write_bytes(b"same content")
        self.file_b.write_bytes(b"same content")
        result = compare_files(self.file_a, self.file_b)
        self.assertTrue(result["identical"])
        self.assertEqual(result["first_hash"], result["second_hash"])

    def test_different_files_do_not_match(self):
        self.file_a.write_bytes(b"original")
        self.file_b.write_bytes(b"changed")
        result = compare_files(self.file_a, self.file_b)
        self.assertFalse(result["identical"])
        self.assertNotEqual(result["first_hash"], result["second_hash"])

    def test_empty_files_match(self):
        self.file_a.write_bytes(b"")
        self.file_b.write_bytes(b"")
        self.assertTrue(compare_files(self.file_a, self.file_b)["identical"])


if __name__ == "__main__":
    unittest.main()
