import sys
from unittest import TestCase, main as unittest_main
from unittest.mock import patch
from talkwave.parse import parse_args

# Add the path to the 'utils' directory to sys.path
# utils_path = os.path.abspath(os.path.join(
#     os.path.dirname(__file__), '..', 'talkwave', 'utils'))
# if not os.path.isdir(utils_path):
#     raise ValueError(f"Cannot find 'utils' directory at {utils_path}")
# sys.path.insert(0, utils_path)

# try:
#     from parse import parse_args
# except ImportError as e:
#     raise ImportError(f"Cannot import 'parse' module: {e}")


class TestMain(TestCase):
    def test_parse_args(self):
        # Test with no arguments
        with patch.object(
            sys, "argv", ["__main__.py"]
        ):
            with self.assertRaises(SystemExit):
                parse_args()

        # Test with required arguments
        with patch.object(
            sys, "argv", ["__main__.py", "-p", "Hello, how are you?"]
        ):
            args = parse_args()
            self.assertEqual(args.prompt, "Hello, how are you?")

        # Test with optional arguments
        with patch.object(
            sys, "argv", ["__main__.py", "-p",
                          "Hello, how are you?", "-m", "3"]
        ):
            args = parse_args()
            self.assertEqual(args.model, 3)


if __name__ == "__main__":
    unittest_main()
