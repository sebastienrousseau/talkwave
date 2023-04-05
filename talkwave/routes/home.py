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

import os
from flask import Flask, render_template

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    if not os.path.exists("openai-key.env"):
        # create a file
        with open("openai-key.env", "w") as f:
            f.write("OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>")
            return "Please add your TalkWave API key to the openai-key.env file"
    return render_template('index.html')
