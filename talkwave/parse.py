import argparse
import sys


def parse_args():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="""
When invoked without arguments, talkwave displays the help menu.
Otherwise, depending on the options specified, talkwave will return a
response or print it in a user-defined way.
"""
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
        help="""
            If set, a stop sequence will be added to the request.
            (Default: False)
        """
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=[
            'csv',
            'db',
            'db3',
            'html',
            'json',
            'markdown',
            'md',
            's3db',
            'sl3',
            'sqlite',
            'sqlite3',
            'text',
            'txt'
        ],
        default='json',
        help="The output format for the response. (Default: json)"
    )

    # Parse the command-line arguments
    return parser.parse_args()
