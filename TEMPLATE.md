<!-- markdownlint-disable MD033 MD041 -->

<img src="https://raw.githubusercontent.com/sebastienrousseau/vault/main/assets/talkwave/icon/ico-talkwave.svg" alt="talkwave logo" width="261" align="right" />

<!-- markdownlint-enable MD033 MD041 -->

# Python TalkWave

![talkwave banner](https://raw.githubusercontent.com/sebastienrousseau/vault/main/assets/talkwave/title/title-talkwave.svg)

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
