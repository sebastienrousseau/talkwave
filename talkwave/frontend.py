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

import flask
import os

from routes.api import api
from routes.details import details
from routes.home import home
from routes.log import log
from routes.errors import page_not_found
from routes.resume import resume
from routes.test import test

# Flask app should start in global layout
app = flask.Flask(__name__)

# Se
app.config["DEBUG"] = True

data_dir_name = "data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)

# Register the home route
app.route('/')(home)

# Register the api route
app.route('/api')(api)

# Register the log route
app.route('/log')(log)

# Register the details route
app.route('/details/<filename>')(details)

# Register the 404 route
app.errorhandler(404)(page_not_found)

# Register the 500 route
app.errorhandler(500)(page_not_found)

# Register the resume route
app.route('/resume/<filename>')(resume)

# Register the test route
app.route('/test')(test)

# Run the application
app.run()
