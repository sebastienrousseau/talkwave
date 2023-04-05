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

data_dir_name = "../data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)


@app.route('/details/<filename>', methods=['GET'])
def details(filename):
    # load the json data from file
    with open(data_dir+'/'+filename, 'r') as f:
        data = json.load(f)
        model = data['model']
        response = data['choices'][0]['text']
        created = data['created']
        prompt = find_prompt_from_created(created)
        # format the response
        response_formatted = response.replace("\n", "<br>")
        # create the details page
        details = "<h2>Details for {}</h2>".format(filename)
        details += "<table><tr><td><b>Created:</b></td><td>{}</td></tr>".format(
            created)
        details += "<tr><td><b>Model:</b></td><td>{}</td></tr>".format(model)
        details += "<tr><td><b>Prompt:</b></td><td>{}</td></tr>".format(prompt)
        details += "<tr><td><b>Response:</b></td><td>{}</td></tr></table>".format(
            response_formatted)
        return details
