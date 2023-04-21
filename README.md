<!-- markdownlint-disable MD033 MD041 -->

<img src="https://kura.pro/talkwave/images/logos/talkwave.svg" alt="talkwave logo" width="261" align="right" />

<!-- markdownlint-enable MD033 MD041 -->

# Python TalkWave

![talkwave banner](https://kura.pro/talkwave/images/titles/title-talkwave.svg)

## Overview 📖

TalkWave is an AI chatbot for developers written in Python. It features
a simple HTML frontend and is designed to be accessible across various
browsers and devices. TalkWave supports asynchronous operations and can
handle multiple requests simultaneously.

## Features ✨

- [x] Accepts a range of parameters to customize the response, such as max tokens, temperature, and stopping conditions.
- [x] Accessible design for cross-browser and device compatibility (Chrome, Firefox, Safari, Edge, and mobile).
- [x] Accurately limits billing with limits and ID binding to prevent exceeding API limits and incurring charges.
- [x] Implements rate limiting functionality to prevent exceeding API limits and incurring charges.
- [x] Plain Python implementation with a limited number of dependencies for easy installation and use.
- [x] Stores responses in log files, JSON, and Markdown formats for easy analysis and sharing.
- [x] Supports multiple GPT models for generating responses, including `gpt-3.5-turbo`,`text-davinci-002`,`text-curie-001`,`text-babbage-001`,`text-ada-001`.

## Requirements 📋

- Python 3.6 or higher
- The `openai`, `tabulate`, and `python-dotenv` packages
- An OpenAI API key (get one [here](https://openai.com/))

## Installation 🛠

1. Install the required packages:

```bash
pip install openai tabulate python-dotenv
```

1. Clone the TalkWave repository:

```bash
git clone https://github.com/sebastienrousseau/talkwave.git
```

1. Add your OpenAI API key to a `.env` file in the project directory:

```bash
OPENAI_API_KEY="your_api_key_here"
```

## Usage 🚀

### Command Line Interface

To use TalkWave, navigate to the project directory in your terminal and
run the following command:

```bash
python talkwave -p "Your prompt here"
```

You can also specify additional options, such as the GPT model, maximum
tokens, temperature, and user ID:

```bash
python talkwave -m 1 -p "Tell me a joke" -t 50 -T 0.5 -u "test@test.com" -r 5 -s -o "json"

```

For more information on the available options, run:

```bash
python talkwave --help
```

### Web Frontend

To use the web frontend, navigate to the project directory in your
terminal and run the following command:

```bash
python talkwave/frontend.py
```

Then, open your browser and navigate to `http://127.0.0.1:5000`. This
will open the TalkWave web frontend, which you can use to generate
responses.

## File Structure 📁

```bash
.
├── talkwave
│   ├── data
│   ├── templates
│   │   ├── 404.html
│   │   └── index.html
│   ├── utils
│   │   ├── curl.py
│   │   └── dir.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py
│   └── frontend.py
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE-APACHE
├── LICENSE-MIT
├── MANIFEST.in
├── README.md
├── README_fr.md
├── TEMPLATE.md
├── pylintrc
├── pyproject.toml
├── requirements.txt
├── setup.cfg
└── setup.py
```

## License 📜

The project is licensed under the terms of both the MIT license and the
Apache License (Version 2.0).

- [Apache License, Version 2.0](https://opensource.org/license/apache-2-0/)
- [MIT license](https://opensource.org/licenses/MIT)
