import os
import unittest
from dir import set_data_directory


class TestDataDirectory(unittest.TestCase):

    def test_set_data_directory(self):
        path = "/tests/test_data"
        expected_location = os.path.join(os.path.dirname(__file__), path)
        actual_location = set_data_directory(path)
        self.assertEqual(actual_location, expected_location)


if __name__ == '__main__':
    unittest.main()
