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
"python3 talkwave").

This allows using TalkWave with third-party libraries without modifying
their code.
"""

from core import main
from parse import parse_args
from tabulate import tabulate
import os
import sys
from __version__ import (
    __description__,
    __title__,
    __version__,
)

# set the directory where the data is stored, value is a string from an
# environment variable "DIR_PATH" (required).
dir_path = os.path.join(os.path.dirname(os.path.realpath(
    __file__)), os.environ.get('DIR_PATH', 'data'))

if __name__ == "__main__":
    # Set the title and description of the program
    title = __title__ + " (v" + __version__ + ")"
    description = __description__

    # Print the title and description of the program
    title_table = tabulate([[title], [description]],
                           tablefmt="rounded_grid")
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
