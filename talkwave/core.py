# Copyright (C) 2023 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#

# '
# set the timeout for the API call to a string value from an environment
# variable "TIMEOUT" (required).
from datetime import datetime
from utils.curl import send_request
from utils.dir import set_data_directory
import dotenv
import json
import os
import sys

VERSION = '0.0.2'

# set the timeout for the API call to a string value from an environment
timeout = os.environ.get('TIMEOUT', '90')

# set the directory where the data is stored, value is a string from an
# environment variable "DIR_PATH" (required).
dir_path = os.path.join(os.path.dirname(os.path.realpath(
    __file__)), os.environ.get('DIR_PATH', 'data'))

# set the timestamp for the API call in ISO
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Function Name: write_response_to_log_file
'''
Write the response to a log file.
'''


def write_response_to_log_file(response, prompt, timestamp):
    """
    Write the response and prompt to a log file.
    """
    if dir_path is None:
        print("Error: Directory path is not provided.")
        return
    with open(dir_path + '/log.txt', 'a') as f:
        f.write(f"{timestamp}|{prompt}|{response}\n")


# Function Name: write_response_to_file
'''
Write the response to a file.
'''


def write_response_to_file(response, prompt, file_format, timestamp):
    """
    Write the response to a file of the specified format.
    """
    if dir_path is None:
        print("Error: Directory path is not provided.")
        return

    if file_format == "json":
        with open(
            set_data_directory(dir_path)+'/{}_log.json'.format(timestamp),
            'a'
        ) as f:
            json.dump(response, f)
    elif file_format == "markdown" or file_format == "md":
        with open(
            set_data_directory(dir_path)+'/{}_log.md'.format(timestamp),
            'a'
        ) as f:
            f.write(f"# TalkWave 🐍 (v{VERSION})\n\n")
            f.write(f"## {timestamp}\n\n")
            f.write(f"```bash\n{prompt}\n```\n\n")
            f.write(f"```bash\n{response}\n```\n")
    elif file_format == "csv" or file_format == "xls":
        with open(
            set_data_directory(dir_path)+'/{}_log.csv'.format(timestamp),
            'a'
        ) as f:
            f.write(f"{timestamp}|{prompt}|{response}\n")
            f.close()
    elif file_format == "html":
        with open(
            set_data_directory(dir_path)+'/{}_log.html'.format(timestamp),
            'a'
        ) as f:
            f.write(f"{timestamp}|{prompt}|{response}\n")
            f.close()
    elif file_format == "txt" or file_format == "text":
        with open(
            set_data_directory(dir_path)+'/{}_log.txt'.format(timestamp),
            'a'
        ) as f:
            f.write(f"{timestamp}|{prompt}|{response}\n")
            f.close()
    else:
        print("Error: Invalid file format.")


# Function Name: main
'''
Main function to interact with the OpenAI API using the given parameters.
'''


def main(
    model: int,
    prompt: str,
    max_tokens: int,
    temperature: float,
    user_id: str,
    rate_limit_seconds: int,
    stop: str,
    output_format: str
):
    """
    Main function to interact with the OpenAI API using the given parameters.
    """
    dotenv.load_dotenv()
    key = dotenv.get_key('.env', 'OPENAI_API_KEY')

    model_dict = {
        1: "gpt-3.5-turbo",
        2: "text-davinci-002",
        3: "text-curie-001",
        4: "text-babbage-001",
        5: "text-ada-001"
    }

    model_str = model_dict.get(model)
    if model_str is None:
        print("Invalid model")
        sys.exit()

    json_resp = send_request(
        key,
        model_str,
        prompt,
        max_tokens,
        temperature,
        user_id,
        rate_limit_seconds,
        stop
    )

    if 'choices' in json_resp:
        assistant_reply = json_resp['choices'][0]['message']['content'].strip()
        print(assistant_reply)

        write_response_to_file(json_resp, prompt, output_format, timestamp)
        write_response_to_log_file(json_resp, prompt, timestamp)

        return assistant_reply

    else:
        print("Error: Unable to get a response from the API.")
        print(json_resp)
        return None
