import os
import unittest
from unittest.mock import patch, MagicMock
from talkwave.core import main


class TestTalkWave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary log file for testing
        cls.log_file = 'test_log.md'
        with open(cls.log_file, 'w') as f:
            f.write('# Test Log\n')

    @classmethod
    def tearDownClass(cls):
        # Delete the temporary log file
        os.remove(cls.log_file)

    def test_main(self):
        # Mock the user input
        with patch('builtins.input', side_effect=['test prompt', 'exit']):
            # Mock the API response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [
                    {
                        'index': 0,
                        'logprobs': None,
                        'text': 'test response',
                        'finish_reason': 'stop',
                        'message': {
                            'content': 'test response message'
                        }
                    }
                ]
            }
            with patch('requests.post', return_value=mock_response):
                # Run the main function
                main(
                    model=1,
                    prompt='test prompt',
                    max_tokens=10,
                    temperature=0.5,
                    user_id='test_user',
                    rate_limit_seconds=5,
                    stop='',
                    output_format='md',
                )


if __name__ == '__main__':
    unittest.main()
