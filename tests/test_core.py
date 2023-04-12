import os
import json

from datetime import datetime
from unittest import TestCase, main as unittest_main

from talkwave.core import write_response_to_file


class TestCore(TestCase):
    # test case for writing response to a file
    def test_write_response_to_file(self):
        response = {'choices': [
            {'text': 'I am fine.'}
        ]}
        prompt = 'How are you?'
        file_format = 'json'
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # get the absolute path to the root of the project
        root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))

        # specify the name of the test data directory
        test_data_dir = 'data'

        # create the test data directory if it doesn't exist
        test_data_path = os.path.join(root_dir, test_data_dir)
        os.makedirs(test_data_path, exist_ok=True)

        # test writing response to a JSON file
        expected_output = json.dumps(response)
        write_response_to_file(
            response, prompt, file_format, timestamp)
        with open(
            f'{root_dir}/{test_data_dir}/{timestamp}_log.json', 'r'
        ) as f:
            self.assertEqual(f.read().strip(), expected_output)

        # test writing response to a CSV file
        expected_output = (
            f"{timestamp}|"
            f"{prompt}|"
            f"{response['choices'][0]['text']}"
        )

        file_format = 'csv'
        write_response_to_file(
            response['choices'][0]['text'], prompt, file_format, timestamp)
        with open(f'{root_dir}/{test_data_dir}/{timestamp}_log.csv', 'r') as f:
            actual_output = f.read().strip()
        self.assertEqual(expected_output, actual_output)

        # test writing response to a TXT file
        expected_output = (
            f"{timestamp}|"
            f"{prompt}|"
            f"{response['choices'][0]['text']}"
        )
        file_format = 'txt'
        write_response_to_file(
            response['choices'][0]['text'], prompt, file_format, timestamp)
        with open(f'{root_dir}/{test_data_dir}/{timestamp}_log.txt', 'r') as f:
            actual_output = f.read().strip()
        self.assertEqual(expected_output, actual_output)

    # test case for writing response to a file with an invalid file
    # format

    def test_write_response_to_file_invalid_file_format(self):
        response = {'choices': [
            {'text': 'I am fine.'}
        ]}
        prompt = 'How are you?'
        file_format = 'txt'
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # get the absolute path to the root of the project
        root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))

        # specify the name of the test data directory
        test_data_dir = 'data'

        # create the test data directory if it doesn't exist
        test_data_path = os.path.join(root_dir, test_data_dir)
        os.makedirs(test_data_path, exist_ok=True)

        # test writing response to a JSON file
        expected_output = json.dumps(response)
        write_response_to_file(
            response, prompt, file_format, timestamp)
        with open(
            f'{root_dir}/{test_data_dir}/{timestamp}_log.json', 'r'
        ) as f:
            self.assertEqual(f.read().strip(), expected_output)


if __name__ == "__main__":
    unittest_main()
