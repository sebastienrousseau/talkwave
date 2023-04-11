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

from flask import render_template, request
import flask
from core import main

# Initialize a Flask app instance
app = flask.Flask(__name__)

# Set the data directory
app.config["DEBUG"] = True
# app.config["PROPAGATE_EXCEPTIONS"] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    This function defines the behavior of the root URL '/'.

    When a GET request is received, it renders the 'index.html'
    template.

    When a POST request is received, it reads the parameters from the
    request form and passes them to the 'main' function in the 'core'
    module. It then renders the 'index.html' template with the response
    returned from 'main'.

    Returns:
        A rendered HTML template.
    """
    if request.method == 'POST':
        model = int(
            request.form.get('model', 1)
        )
        prompt = request.form['prompt']
        max_tokens = int(
            request.form.get('max_tokens', 50)
        )
        temperature = float(
            request.form.get('temperature', 0.5)
        )
        user_id = str(
            request.form.get('user_id', 'example_user')
        )
        rate_limit_seconds = int(
            request.form.get('rate_limit_seconds', 5)
        )
        stop = str(
            request.form.get('stop', None)
        )
        output_format = str(
            request.form.get('output_format', 'json')
        )

        response = main(
            model,
            prompt,
            max_tokens,
            temperature,
            user_id,
            rate_limit_seconds,
            stop,
            output_format
        )
        return render_template(
            'index.html',
            response=response,
            prompt=request.form['prompt']
        )
    else:
        return render_template('index.html')


if __name__ == '__main__':
    """
    This block of code starts the Flask app if the script is run as the
    main module.

    Returns:
        None.
    """
    app.run()
