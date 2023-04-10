import unittest
from unittest.mock import patch
from flask import render_template, request
import flask
from core import main


# Initialize a Flask app instance
app = flask.Flask(__name__)


class TestCore(unittest.TestCase):

    def test_main(self):
        # Test with valid input
        response = main(1, 'Hello', 50, 0.5, 'example_user', 5, '', 'json')
        self.assertIsInstance(response, str)

        # Test with invalid model
        with self.assertRaises(SystemExit):
            main(10, 'Hello', 50, 0.5, 'example_user', 5, '', 'json')


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True  # type: ignore[attr]

    def test_index_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('core.main')
    def test_index_post_request(self, mock_main):
        mock_main.return_value = 'Hello, world!'
        data = {
            'model': '1',
            'prompt': 'Hello',
            'max_tokens': '50',
            'temperature': '0.5',
            'user_id': 'example_user',
            'rate_limit_seconds': '5',
            'stop': '',
            'output_format': 'json'
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, world!', response.data)
