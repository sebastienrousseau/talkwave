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

from tabulate import tabulate
from utils import curl_request
import argparse
import dotenv
from datetime import datetime
import json
import sys
import os

timeout = 10
data_dir_name = "data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def write_response_to_log_file(response, prompt):
    """
    Write the response and prompt to a log file.
    """
    with open(data_dir+'/log.txt', 'a') as f:
        f.write(f"{timestamp}|{prompt}|{response}\n")


def write_to_json_file(response):
    """
    Write the response to a JSON file.
    """
    with open(data_dir+'/{}_log.json'.format(timestamp), 'a') as f:
        json.dump(response, f)


def main(model: int, prompt: str, max_tokens: int, temperature: float):
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

    json_resp = curl_request(key, model_str, prompt, max_tokens, temperature)

    if 'choices' in json_resp:
        assistant_reply = json_resp['choices'][0]['message']['content'].strip()
        print(assistant_reply)
        write_response_to_log_file(json_resp, prompt)
        write_to_json_file(json_resp)
    else:
        print("Error: Unable to get a response from the API.")
        print(json_resp)
        sys.exit()


if __name__ == "__main__":
    title = "TalkWave 🐍 (version 0.0.1)"
    description = "An AI chatbot for developers written in Python"

    title_table = tabulate([[title], [description]], tablefmt="rounded_grid")
    print(title_table)

    parser = argparse.ArgumentParser(
        description="Talk to an AI language model.")
    parser.add_argument("-m", "--model", type=int, required=True,
                        help="The model to use. (0: gpt-3.5-turbo, 1: text-davinci-002, 2: text-curie-001, 3: text-babbage-001, 4: text-ada-001)")
    parser.add_argument("-p", "--prompt", required=True,
                        help="The prompt to send to the AI.")
    parser.add_argument("-t", "--tokens", type=int, default=50,
                        help="The maximum number of tokens in the response.")
    parser.add_argument("-T", "--temperature", type=float, default=0.5,
                        help="The sampling temperature for the AI response.")

    args = parser.parse_args()

    main(args.model, args.prompt, args.tokens, args.temperature)
