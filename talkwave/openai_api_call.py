import os
import json
import requests

# set the timeout for the API call to 10 seconds
timeout = 60


def openai_api_call(model, prompt, max_tokens, temperature):
    # create the request body
    request_body = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": []
    }
    # check if the API key is set
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    # call the openai api
    try:
        response = requests.post(
            "https://api.openai.com/v1/engines/" + model + "/completions",
            headers={"Authorization": "Bearer " + api_key},
            data=json.dumps(request_body),
            timeout=timeout
        )
        # raise an exception if the response code indicates an error
        response.raise_for_status()
        choices = response.json().get('choices', [])
        if not choices:
            return 'Error: Empty response from OpenAI API'
        return choices[0]['text']
    except requests.exceptions.Timeout:
        return 'Error: API call to OpenAI timed out'
    except Exception as e:
        return f'Error: {e}'
