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

from datetime import datetime
import json
import os

data_dir_name = "data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)


def write_response_to_log_file(response, prompt):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(data_dir+'/log.txt'):
        with open(data_dir+'/log.txt', 'w') as f:
            f.write("timestamp|prompt|response")
    with open(data_dir+'/log.txt', 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        f.write(timestamp+"|{}|".format(str(prompt))+str(response)+"\n")


def write_to_json_file(response):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    timestamp = timestamp.replace(" ", "_").replace(":", "-").replace("-", "_")
    with open(data_dir+'/{}_log.json'.format(timestamp), 'a') as f:
        json.dump(response, f)


def find_prompt_from_created(created):
    created = str(created)
    with open(data_dir+'/log.txt', 'r') as f:
        for line in f:
            if created in line:
                return line.split("|")[1]
    return "Prompt not found"
