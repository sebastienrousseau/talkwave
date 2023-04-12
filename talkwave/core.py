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
from datetime import datetime

try:
    from talkwave.__version__ import (
        __logo__,
        __title__,
        __version__,
    )
except ModuleNotFoundError:
    from __version__ import (
        __logo__,
        __title__,
        __version__,
    )


import dotenv
import json
import os
import sqlite3
import sys

try:
    from talkwave.curl import send_request
except ModuleNotFoundError:
    from curl import send_request

# set the directory where the data is stored, value is a string from an
# environment variable "DATA_DIR" (required).
data_dir = os.path.join(os.path.dirname(os.path.realpath(
    __file__)), os.environ.get('DATA_DIR', 'data'))

# set the timestamp for the API call in ISO
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Function Name: write_response_to_log_file
'''
Write the response to a log file.
'''

data_dir = "data"  # Define the data directory or pass it as an argument


def write_response_to_log_file(response, prompt, timestamp):
    """
    Write the response and prompt to a log file.
    """
    if data_dir is None:
        print("Error: Directory path is not provided.")
        return
    with open(data_dir + '/log.txt', 'a') as f:
        f.write(f"{timestamp}|{prompt}|{response}\n")


# Function Name: write_response_to_file
'''
Write the response to a file.
'''

# List of valid file formats for text files
text = ["csv", "xls", "html", "txt", "text",
        "log", "json", "xml", "yaml", "yml"]
database = ["db", "sqlite", "sqlite3", "db3", "s3db", "sl3"]
markdown = ["md", "markdown"]
html = ["html", "htm"]
# pdf = ["pdf"]
# image = ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif"]


# Function Name: write_response_to_file
'''
Write the response to a file.
'''


def write_response_to_file(
    response,
    prompt,
    file_format,
    timestamp,
    data_dir=data_dir
):
    """
    Write the response to a file of the specified format.
    """
    if data_dir is None:
        print("Error: Directory path is not provided.")
        return

    if file_format == "json":
        with open(
            os.path.join(data_dir, f"{timestamp}_log.json"),
            "a"
        ) as f:
            json.dump(response, f)
    elif file_format == "html":
        with open(os.path.join(data_dir, "log.html"), "a") as f:
            if os.stat(os.path.join(data_dir, "log.html")).st_size == 0:

                f.write("<!DOCTYPE html>\n")
                f.write("""
<html lang=\"en\" itemscope itemtype=\"http://schema.org/WebPage\">\n
""")
                f.write("<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write("""
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n
""")
                f.write("""
<meta name=\"theme-color\" content=\"#e82440\"/>\n
""")
                f.write("""
<link rel=\"stylesheet\"
href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css\"
integrity=\"sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65\"
crossorigin=\"anonymous\" />\n""")
                f.write(
                    """
                        <style>
                            .wrap-code {
                                white-space: pre-wrap;
                                word-wrap: break-word;
                            }
                        </style>\n
                    """)
                f.write("<title>"+__title__+"</title>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                f.write(
                    """
<header class=\"bd-header bg-dark py-3 d-flex align-items-stretch
border-bottom border-dark\">""")
                f.write("""
<div class=\"container-fluid d-flex align-items-center\">
""")
                f.write(
                    """
<h1 class=\"d-flex align-items-center fs-4 text-white mb-0\">
""")
                f.write(f"""
<img src="{__logo__}"
width="33"
height="33"
class="me-3" alt="{__title__}" />{__title__}</h1>""")
                f.write("</div>")
                f.write("""
<div class=\"container d-flex flex-wrap justify-content-end\">
""")
                f.write("</div>")
                f.write("</header>")
                f.write("  <main>\n")
                f.write("    <div class=\"container-fluid py-3\">\n")

            # Loop over each response and write the prompt and response
            # to the HTML file
            for i in range(len(response["choices"])):
                # Parse the timestamp string into a datetime object
                dt = datetime.fromisoformat(
                    timestamp.replace("Z", "+00:00")
                )

                # Format the datetime object into a more readable string
                formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

                f.write(
                    f"<p><strong><time>"
                    f"{formatted_timestamp}</time></strong></p>\n"
                )
                f.write("<ul>\n")
                f.write(
                    f"""
<li>
    <strong>Prompt:</strong>
    <pre class=\"wrap-code\"><code>{prompt}</code></pre></li>\n""")
                f.write(
                    f"""
<li><strong>Response:</strong>
<pre class=\"wrap-code\">
<code>{response['choices'][i]['message']['content']}</code>
</pre></li>\n""")
                f.write("</ul>\n")
                f.write("    <hr />\n")

            if os.stat(os.path.join(data_dir, "log.html")).st_size >= 1:
                f.write("    </div>\n")
                f.write("  </main>\n")
                f.write("</body>\n")
                f.write("</html>\n")
    elif file_format in markdown:
        with open(
            os.path.join(data_dir, f"{timestamp}_log.md"),
            "a"
        ) as f:
            f.write(f"# {__title__} (v{__version__})\n\n")
            f.write(f"## {timestamp}\n\n")
            f.write(f"```bash\n{prompt}\n```\n\n")
            f.write(f"```bash\n{response}\n```\n")
    elif file_format in text:
        # elif file_format in ["csv", "xls", "html", "txt", "text"]:
        with open(
            os.path.join(data_dir, f"{timestamp}_log.{file_format}"),
            "a"
        ) as f:
            f.write(f"{timestamp}|{prompt}|{response}\n")
    elif file_format in database:
        # set the path to the database file
        db_path = os.path.join(data_dir, f"log.{file_format}")
        # create a new database file if it doesn't exist
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "CREATE TABLE responses (timestamp TEXT, prompt TEXT, "
                "response TEXT)"
            )
            conn.commit()
            conn.close()
        # insert the response into the database
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO responses (timestamp, prompt, response) "
            "VALUES (?, ?, ?)",
            (timestamp, prompt, json.dumps(response))
        )
        conn.commit()
        conn.close()
    else:
        print("Error: Invalid file format.")
        return


# Function Name: main
'''
Main function to interact with the OpenAI API using the given
parameters.
'''


def main(
    model: int,
    prompt: str,
    max_tokens: int,
    temperature: float,
    user_id: str,
    rate_limit_seconds: int,
    stop: str,
    output_format: str
):
    """
    Main function to interact with the OpenAI API using the given
    parameters.
    """
    dotenv.load_dotenv()
    key = dotenv.get_key('.env', 'OPENAI_API_KEY')

    model_dict = {
        1: "gpt-3.5-turbo",
        2: "text-davinci-002",
        3: "text-curie-001",
        4: "text-babbage-001",
        5: "text-ada-001"
    }

    model_str = model_dict.get(model)
    if model_str is None:
        print("Invalid model")
        sys.exit()

    # Create the timestamp
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    json_resp = send_request(
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

        write_response_to_file(json_resp, prompt, output_format, timestamp)
        write_response_to_log_file(json_resp, prompt, timestamp)

        return assistant_reply

    else:
        print("Error: Unable to get a response from the API.")
        print(json_resp)
        return None
