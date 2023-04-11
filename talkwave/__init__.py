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

# TalkWave


TalkWave is a Python package that provides an easy-to-use command-line
interface for interacting with OpenAI's GPT-powered language models.

## Features

- Supports multiple GPT models for generating responses.
- Accepts a range of parameters to customize the response, such as max
tokens, temperature, and stopping conditions.
- Stores responses in log files, JSON, and Markdown formats for easy
analysis and sharing.
- Provides rate limiting functionality to prevent exceeding API limits
and incurring charges.

## Requirements

- Python 3.6 or higher
- The `openai`, `tabulate`, and `python-dotenv` packages
- An OpenAI API key (get one [here](https://openai.com/))

## Installation

1. Install the required packages:

```bash
pip install openai tabulate python-dotenv
```

1. Clone the TalkWave repository:

```bash
git clone https://github.com/yourusername/talkwave.git
```

3. Add your OpenAI API key to a `.env` file in the project directory:

```bash
OPENAI_API_KEY="your_api_key_here"
```

## Usage

To use TalkWave, navigate to the project directory in your terminal and
run the following command:

```bash
python talkwave -p "Your prompt here"
```

You can also specify additional options, such as the GPT model, maximum
tokens, temperature, and user ID:

```bash
python talkwave\n
    -m 1\n
    -p "Tell me a joke"\n
    -t 50\n
    -T 0.5\n
    -u "test@test.com"\n
    -r 5\n
    -s "."
```

For more information on the available options, run:

```bash
python talkwave --help
```


## License

The project is licensed under the terms of both the MIT license and the
Apache License (Version 2.0).

- [Apache License, Version 2.0](https://opensource.org/license/apache-2-0/)
- [MIT license](https://opensource.org/licenses/MIT)

"""

"""The Python talkwave module."""
__all__ = ["__version__"]

__version__ = "0.0.2"
