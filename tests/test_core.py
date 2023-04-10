import unittest
from unittest.mock import patch
from core import main


class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.model = 1
        self.prompt = "Hello, how are you?"
        self.max_tokens = 50
        self.temperature = 0.5
        self.user_id = "user123"
        self.rate_limit_seconds = 2
        self.stop = None
        self.output_format = "json"

    @patch("main.send_request")
    def test_main_function_with_valid_parameters(self, mock_send_request):
        mock_send_request.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "I'm doing well, thank you for asking!"
                    }
                }
            ]
        }
        response = main(
            self.model,
            self.prompt,
            self.max_tokens,
            self.temperature,
            self.user_id,
            self.rate_limit_seconds,
            self.stop,
            self.output_format
        )
        self.assertEqual(response, "I'm doing well, thank you for asking!")

    def test_main_function_with_invalid_model(self):
        self.model = 6
        with self.assertRaises(SystemExit):
            main(
                self.model,
                self.prompt,
                self.max_tokens,
                self.temperature,
                self.user_id,
                self.rate_limit_seconds,
                self.stop,
                self.output_format
            )

    def test_main_function_with_invalid_output_format(self):
        self.output_format = "invalid_format"
        with self.assertRaises(Exception):
            main(
                self.model,
                self.prompt,
                self.max_tokens,
                self.temperature,
                self.user_id,
                self.rate_limit_seconds,
                self.stop,
                self.output_format
            )
