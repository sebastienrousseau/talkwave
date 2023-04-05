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
#
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from flask import Flask
from openai_api_call import openai_api_call

app = Flask(__name__)
app.config["DEBUG"] = True

data_dir_name = "../data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)


@app.route('/resume/<filename>', methods=['GET'])
def resume(filename):
    # get the path of the specified file
    file_path = os.path.join(data_dir, filename)

    # check if the file exists
    if not os.path.isfile(file_path):
        return "File does not exist."

    # read the file contents
    with open(file_path, 'r') as f:
        data = json.load(f)

        # extract the relevant data from the file
        prompt = data.get('prompt')
        model = data.get('model')
        response = data['choices'][0]['text']
        max_tokens = data.get('max_tokens')
        temperature = data.get('temperature')

        # call the TalkWave API to get a new response based on the existing data
        new_response = openai_api_call(model, prompt, max_tokens, temperature)

        # update the file with the new response
        data['choices'][0]['text'] = new_response
        with open(file_path, 'w') as f:
            json.dump(data, f)

        # create a response to return to the user
        response_html = "<h1>Resuming query:</h1>"
        response_html += "<p><strong>Prompt:</strong> {}</p>".format(prompt)
        response_html += "<p><strong>Model:</strong> {}</p>".format(model)
        response_html += "<p><strong>Previous response:</strong> {}</p>".format(
            response)
        response_html += "<hr>"
        response_html += "<h1>New response:</h1>"
        response_html += "<p>{}</p>".format(new_response)
        return response_html
