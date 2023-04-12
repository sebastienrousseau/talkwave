import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch
from requests.exceptions import Timeout

from talkwave.curl import send_request


class TestSendRequest(TestCase):

    # test case for missing user_id
    def test_missing_user_id(self):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = ''
        rate_limit_seconds = 5
        stop = None

        with self.assertRaises(ValueError):
            send_request(
                api_key,
                model,
                prompt,
                max_tokens,
                temperature,
                user_id,
                rate_limit_seconds,
                stop
            )

    # test case for rate limit period of 0
    def test_rate_limit_period_of_0(self):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = 'test_user'
        rate_limit_seconds = 0
        stop = None

        with self.assertRaises(ValueError):
            send_request(
                api_key,
                model,
                prompt,
                max_tokens,
                temperature,
                user_id,
                rate_limit_seconds,
                stop
            )

    # test case for successful request
    @patch('requests.post')
    def test_successful_request(self, mock_post):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = 'test_user'
        rate_limit_seconds = 5
        stop = None

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }
        mock_post.return_value = mock_response

        response = send_request(
            api_key,
            model,
            prompt,
            max_tokens,
            temperature,
            user_id,
            rate_limit_seconds,
            stop
        )

        expected_response = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }

        self.assertEqual(response, expected_response)

    # test case for timeout
    @patch('requests.post')
    def test_timeout(self, mock_post):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = 'test_user'
        rate_limit_seconds = 5
        stop = None

        mock_post.side_effect = Timeout()

        with self.assertRaises(Exception):
            response = send_request(
                api_key,
                model,
                prompt,
                max_tokens,
                temperature,
                user_id,
                rate_limit_seconds,
                stop
            )
            self.assertEqual(response, None)
            self.assertEqual(mock_post.call_count, 1)

    @patch('requests.post')
    def test_stop_message(self, mock_post):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = 'test_user'
        rate_limit_seconds = 5
        stop = 'stop'

        # Mock response with stop message
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'text': 'This is a stop message.',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'stop'
                }
            ]
        }
        mock_post.return_value = mock_response

        # Test that StopIteration is raised when stop message is received
        with self.assertRaises(StopIteration):
            send_request(api_key, model, prompt, max_tokens,
                         temperature, user_id, rate_limit_seconds, stop)

        # Second call to send_request should return a response without
        # raising an exception

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }
        mock_post.return_value = mock_response
        response = send_request(
            api_key,
            model,
            prompt,
            max_tokens,
            temperature,
            user_id,
            rate_limit_seconds,
            stop
        )
        expected_response = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }
        self.assertEqual(response, expected_response)
        self.assertEqual(mock_post.call_count, 2)

    # test case for rate limit

    @patch('requests.post')
    def test_rate_limit(self, mock_post):
        api_key = 'test_api_key'
        model = 'test_model'
        prompt = 'test_prompt'
        max_tokens = 10
        temperature = 0.5
        user_id = 'test_user'
        rate_limit_seconds = 5
        stop = None

        # First call to send_request should return a response without
        # raising an exception
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }
        mock_post.return_value = mock_response
        response = send_request(
            api_key,
            model,
            prompt,
            max_tokens,
            temperature,
            user_id,
            rate_limit_seconds,
            stop
        )
        expected_response = {
            'choices': [
                {
                    'text': 'test_text',
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': 'test_reason'
                }
            ]
        }
        self.assertEqual(response, expected_response)
        self.assertEqual(mock_post.call_count, 1)


if __name__ == '__main__':
    unittest.main()
