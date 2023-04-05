<!-- markdownlint-disable MD033 MD041 -->

<img src="https://raw.githubusercontent.com/sebastienrousseau/vault/main/assets/talkwave/icon/ico-talkwave.svg" alt="talkwave logo" width="261" align="right" />

<!-- markdownlint-enable MD033 MD041 -->

# Python TalkWave

![talkwave banner](https://raw.githubusercontent.com/sebastienrousseau/vault/main/assets/talkwave/title/title-talkwave.svg)

## Overview 📖

TalkWave is an AI chatbot for developers written in Python. It features a simple HTML frontend and is designed to be accessible across various browsers and devices. TalkWave supports asynchronous operations and can handle multiple requests simultaneously.

## Features ✨

- Implements chat rate limiting to avoid overly frequent requests
- Accurately limits billing with limits and ID binding
- Self-maintaining model framework that supports any LLM model and any external API integration, abstracting and unifying access to GPT-3, GPT-3.5, and GPT-4
- Intuitive design of the chat allows for cross-replying, retracing replies, trigger-based replies, and the use of stickers for added fun
- Allows voice command for user inputs
- Accessible design for cross-browser and device compatibility
- Plain Python implementation with a limited number of dependencies

## File Structure 📁

```bash

```

## Installation 🛠

1. Clone the repository:

```bash
git clone https://github.com/your-username/talkwave.git
```

1. Change into the project directory:

```bash
cd talkwave
```

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

1. Create a `.env` file in the root directory and add the following environment variables:

```bash
echo "API_KEY=your_api_key" > .env
echo "API_URL=your_api_url" >> .env
```

1. Run the application:

```bash
python app/main.py
```

1. Open the application in your browser:

```bash
http://localhost:8000
```

## License

Copyright © 2023 WiserOne. All rights reserved.
SPDX-License-Identifier: Apache-2.0 OR MIT

This README file provides an overview of the TalkWave project, its features, installation instructions, and licensing information. Update the repository URL in the "Installation" section to match your GitHub repository.
