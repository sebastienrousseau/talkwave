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
from utils.curl import request
from utils.dir import set_data_directory
import dotenv
import json
import os
import sys

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


def write_response_to_log_file(response, prompt, dir_path: str):
    """
    Write the response and prompt to a log file.
    """
    try:
        directory = set_data_directory(dir_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/log.txt', 'a') as f:
            f.write(f"{timestamp}|{prompt}|{response}\n")
    except ValueError as e:
        print(e)


# Function Name: write_to_json_file
'''
Write the response to a JSON file.
'''


def write_to_json_file(response):
    """
    Write the response to a JSON file.
    """
    if dir_path is None:
        print("Error: Directory path is not provided.")
        return

    with open(
        set_data_directory(dir_path)+'/{}_log.json'.format(timestamp),
        'a'
    ) as f:
        json.dump(response, f)


# Function Name: write_to_markdown_file
'''
Write the response to a Markdown file
'''


def write_to_markdown_file(response, prompt):
    """
    Write the response to a Markdown file
    """
    if dir_path is None:
        print("Error: Directory path is not provided.")
        return

    with open(
        set_data_directory(dir_path)+'/{}_log.md'.format(timestamp),
        'a'
    ) as f:
        f.write(f"# TalkWave 🐍 (v0.0.1)\n\n")
        f.write(f"## {timestamp}\n\n")
        f.write(f"```bash\n{prompt}\n```\n\n")
        f.write(f"```bash\n{response}\n```\n")


# Function Name: main
'''
Main function to interact with the OpenAI API using the given parameters.
'''


def main(
    model: int,
    prompt: str,
    max_tokens: int,
    temperature: float,
    user_id: int,
    rate_limit_seconds: int,
    stop: str,
):
    """
    Main function to interact with the OpenAI API using the given parameters.
    """
    dotenv.load_dotenv()
    key = dotenv.get_key('.env', 'OPENAI_API_KEY')

    model_dict = {
        # GPT-4 - Most capable GPT-4 model and optimized for chat at 1/10th the cost of text-davinci-003.
        # 0: "gpt-4",
        # GPT-3.5 Turbo - Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003.
        1: "gpt-3.5-turbo",
        # Davinci - Most capable GPT-3 model. Can do any task the other models can do, often with higher quality.
        2: "text-davinci-002",
        # Curie - Very capable, faster and lower cost than Davinci.
        3: "text-curie-001",
        # Babbage - Capable of straightforward tasks, very fast, and lower cost.
        4: "text-babbage-001",
        # Ada - Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.
        5: "text-ada-001"
    }

    model_str = model_dict.get(model)
    if model_str is None:
        print("Invalid model")
        sys.exit()

    json_resp = request(
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
        write_response_to_log_file(json_resp, prompt, dir_path)
        write_to_json_file(json_resp)
        write_to_markdown_file(assistant_reply, prompt)

        return assistant_reply

    else:
        print("Error: Unable to get a response from the API.")
        print(json_resp)
        return None
