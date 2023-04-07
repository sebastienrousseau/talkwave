# Copyright (C) 2023 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Enables use of Python TalkWave as a "main" function (i.e.
"python3 -m talkwave").

This allows using TalkWave with third-party libraries without modifying
their code.
"""
# '
from datetime import datetime
import os
from tabulate import tabulate
from utils.curl import request
from utils.dir import set_data_directory
import argparse
import dotenv
import json
import sys

# set the timeout for the API call to a string value from an environment
# variable "TIMEOUT" (required).
timeout = os.environ.get('TIMEOUT')


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

    with open(set_data_directory(dir_path)+'/{}_log.json'.format(timestamp), 'a') as f:
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

    with open(set_data_directory(dir_path)+'/{}_log.md'.format(timestamp), 'a') as f:
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
        stop: bool
):
    """
    Main function to interact with the OpenAI API using the given parameters.
    """
    dotenv.load_dotenv()
    key = dotenv.get_key('openai-key.env', 'OPENAI_API_KEY')

    model_dict = {
        0: "gpt-3.5-turbo",
        1: "text-davinci-002",
        2: "text-curie-001",
        3: "text-babbage-001",
        4: "text-ada-001"
    }

    model_str = model_dict.get(model)
    if model_str is None:
        print("Invalid model")
        sys.exit()

    json_resp = request(key, model_str, prompt, max_tokens,
                        temperature, user_id, rate_limit_seconds, stop)

    if 'choices' in json_resp:
        assistant_reply = json_resp['choices'][0]['message']['content'].strip()
        print(assistant_reply)
        write_response_to_log_file(json_resp, prompt, dir_path)
        write_to_json_file(json_resp)
        write_to_markdown_file(assistant_reply, prompt)
    else:
        print("Error: Unable to get a response from the API.")
        print(json_resp)
        sys.exit()

    sys.exit()


if __name__ == "__main__":
    title = "TalkWave 🐍 (v0.0.1)"
    description = "An AI chatbot for developers"

    title_table = tabulate([[title], [description]], tablefmt="rounded_grid")
    print()
    print(title_table)
    print()

    parser = argparse.ArgumentParser(
        description="When invoked without the -p/--prompt argument, talkwave displays an error message indicating that this argument is required. Otherwise, depending on the options specified, talkwave will return a response or print it in a user-defined way.")
    parser.add_argument("-m", "--model", type=int, default=1,
                        help="""
                            The AI model to use:
                                0: gpt-3.5-turbo,
                                1: text-davinci-002,
                                2: text-curie-001,
                                3: text-babbage-001,
                                4: text-ada-001

                            (Default: 1: text-davinci-002)
                        """)
    parser.add_argument("-p", "--prompt", required=True,
                        help="""
                                The prompt to send to the AI. (Required)
                            """)
    parser.add_argument("-t", "--tokens", type=int, default=50,
                        help="""
                                The maximum number of tokens in the
                                response. (Default: 50)
                            """)
    parser.add_argument("-T", "--temperature", type=float, default=0.5,
                        help="""
                                The sampling temperature for the AI
                                response. (Default: 0.5)
                            """)
    parser.add_argument("-u", "--user_id", type=str, default="example_user",
                        help="The user ID to bind with the request. (Default: example_user)")
    parser.add_argument("-r", "--rate_limit_seconds", type=int, default=5,
                        help="The rate limit in seconds for API requests. (Default: 5)")
    parser.add_argument("-s", "--stop", action='store_true',
                        help="If set, a stop sequence will be added to the request. (Default: False)")

    args = parser.parse_args()

    main(args.model, args.prompt, args.tokens, args.temperature,
         args.user_id, args.rate_limit_seconds, args.stop)
