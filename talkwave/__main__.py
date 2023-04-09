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

from core import main
from tabulate import tabulate
import argparse
import os
import sys

# set the directory where the data is stored, value is a string from an
# environment variable "DIR_PATH" (required).
dir_path = os.path.join(os.path.dirname(os.path.realpath(
    __file__)), os.environ.get('DIR_PATH', 'data'))


def parse_args():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="When invoked without arguments, talkwave displays the help menu. Otherwise, depending on the options specified, talkwave will return a response or print it in a user-defined way."
    )

    parser.add_argument(
        "-m",
        "--model",
        type=int,
        default=1,
        help="""
            The AI model to use:
            0: gpt-3.5-turbo,
            1: text-davinci-002,
            2: text-curie-001,
            3: text-babbage-001,
            4: text-ada-001

            (Default: 1: text-davinci-002)
        """
    )

    parser.add_argument(
        "-p",
        "--prompt",
        required=not sys.stdin.isatty(),
        help="The prompt to send to the AI. (Required)"
    )

    parser.add_argument(
        "-t",
        "--tokens",
        type=int,
        default=50,
        help="The maximum number of tokens in the response. (Default: 50)"
    )

    parser.add_argument(
        "-T",
        "--temperature",
        type=float,
        default=0.5,
        help="The sampling temperature for the AI response. (Default: 0.5)"
    )

    parser.add_argument(
        "-u",
        "--user_id",
        type=str,
        default="example_user",
        help="The user ID to bind with the request. (Default: example_user)"
    )

    parser.add_argument(
        "-r",
        "--rate_limit_seconds",
        type=int,
        default=5,
        help="The rate limit in seconds for API requests. (Default: 5)"
    )

    parser.add_argument(
        "-s",
        "--stop",
        action='store_true',
        help="If set, a stop sequence will be added to the request. (Default: False)"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=['csv', 'html', 'json', 'markdown', 'md', 'text', 'txt'],
        default='json',
        help="The output format for the response. (Default: json)"
    )

    # Parse the command-line arguments
    return parser.parse_args()


if __name__ == "__main__":
    # Set the title and description of the program
    title = "TalkWave 🐍 (v0.0.1)"
    description = "An AI chatbot for developers"

    # Print the title and description of the program
    title_table = tabulate([[title], [description]], tablefmt="rounded_grid")
    print()
    print(title_table)
    print()

    # Parse the command-line arguments
    args = parse_args()

    # Call the main function to interact with the OpenAI API
    main(
        args.model,
        args.prompt,
        args.tokens,
        args.temperature,
        args.user_id,
        args.rate_limit_seconds,
        args.stop,
        args.output
    )
    sys.exit(0)
