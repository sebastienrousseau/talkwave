from flask import Flask, request, redirect, url_for
from handler import write_response_to_log_file, write_to_json_file
from utils import curl_request
import os

app = Flask(__name__)
app.config["DEBUG"] = True

data_dir_name = "/data"
data_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), data_dir_name)


@app.route('/api', methods=['POST'])
def api():
    # get the form data
    # call the openai api
    # write the response to a log file
    # write the response to a json file
    # return the response to the frontend
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key is None:
        return "OPENAI_API_KEY environment variable is not set"
    model = str(request.form.get('model')).strip()
    prompt = str(request.form.get('prompt')).strip()
    max_tokens = int(str(request.form.get('max_tokens')))
    temperature = float(str(request.form.get('temperature')))
    model = model.lower()
    if model == "davinci":
        model = "text-davinci-002"
    elif model == "curie":
        model = "text-curie-001"
    elif model == "babbage":
        model = "text-babbage-001"
    elif model == "ada":
        model = "text-ada-001"
    else:
        return "Invalid model[{}]".format(model)
    response = curl_request(api_key, model, prompt, max_tokens, temperature)
    write_response_to_log_file(response, prompt)
    write_to_json_file(response)
    return redirect(url_for('log'))
