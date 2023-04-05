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

# The destination is temporarily unavailable.


@app.errorhandler(403)
def service_unavailable(e):
    return render_template('403.html'), 403

# The requested resource cannot be found.


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# The requested resource does not support the HTTP verb that has been used in the request.


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
