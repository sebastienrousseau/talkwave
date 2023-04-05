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

from handler import find_prompt_from_created

app = Flask(__name__)
app.config["DEBUG"] = True

data_dir_name = "/data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)


@app.route('/log')
def log():
    # create a flask table with all json files
    table = ""
    with open('templates/head.txt', 'r') as f:
        for line in f:
            table += line
    with open('templates/menu.txt', 'r') as f:
        for line in f:
            table += line
    table += "<style>table, th, td {border: 1px solid black;}</style>"
    table += "<table><tr><th>File</th><th>Created</th><th>Model</th><th>Prompt</th><th>Response</th><th>Options</th></tr><tbody>"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        return table + "</tbody></table>"
    # get a list of files in the data directory
    files = os.listdir(data_dir)
    # sort the files in descending order
    files.sort(reverse=True)
    # loop through the files
    data = ""
    for file in files:
        try:
            if file.endswith(".json"):
                # get data from file
                with open(data_dir+'/'+file, 'r') as f:
                    data = json.load(f)
                    model = data['model']
                    print("model:", model)
                    response = data['choices'][0]['text']
                    created = data['created']
                    prompt = find_prompt_from_created(created)
                    # create a table row
                    table += "<tr>"
                    table += "<td>{}</td>".format(file)
                    table += "<td>{}</td>".format(created)
                    table += "<td>{}</td>".format(model)
                    table += "<td>{}</td>".format(prompt)
                    table += "<td>{}</td>".format(response)
                    # add options
                    table += "<td>"
                    table += "<a href='/details/{}'>Details</a>&nbsp;&nbsp;".format(
                        file)
                    table += "<a href='/resume/{}'>Resume</a>&nbsp;&nbsp;".format(
                        file)
                    table += "</td>"
                    table += "</tr>"
        except:
            table += "<td>{}</td><td></td><td></td><td></td><td>{}</td><td></td></tr>".format(
                file, data)

    table += "</tbody></table>"  # <-- Add this line to close the tbody tag

    with open('templates/footer.txt', 'r') as f:
        for line in f:
            table += line

    return table
