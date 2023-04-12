import os
import unittest
from unittest import TestCase
from talkwave.dir import set_data_directory


class TestDataDirectory(TestCase):

    # test case for setting the data directory
    def test_set_data_directory(self):
        path = "/data"
        expected_location = os.path.join(os.path.dirname(__file__), path)
        actual_location = set_data_directory(path)
        self.assertEqual(actual_location, expected_location)

    # test case for setting the data directory to a non-existent directory
    def test_set_data_directory_non_existent(self):
        path = "/tests/non_existent"
        expected_location = os.path.join(os.path.dirname(__file__), path)
        actual_location = set_data_directory(path)
        self.assertEqual(actual_location, expected_location)

    # test case for setting the data directory to a file
    def test_set_data_directory_file(self):
        path = "/data/test_file.txt"
        expected_location = os.path.join(os.path.dirname(__file__), path)
        actual_location = set_data_directory(path)
        self.assertEqual(actual_location, expected_location)

    # test case for setting the data directory to a directory
    def test_set_data_directory_directory(self):
        path = "/data/test_directory"
        expected_location = os.path.join(os.path.dirname(__file__), path)
        actual_location = set_data_directory(path)
        self.assertEqual(actual_location, expected_location)


if __name__ == '__main__':
    unittest.main()
