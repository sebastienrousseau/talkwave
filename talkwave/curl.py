import os
import time
import requests

# Set the timeout for the API call to a string value from an environment
# Keep the default value as a string
timeout_str = os.environ.get('TIMEOUT', '90')

# Convert the timeout value to an integer or float
timeout = int(timeout_str)

# Function Name: request

# Parameters:

# key: str - API key for OpenAI authentication
# model: str - name of the language model to use for generating text
# prompt: str - text prompt to feed into the language model
# max_tokens: int - maximum number of tokens to generate in the response
# temperature: float - level of "creativity" to use when generating text
# user_id: str - unique identifier for the user
# rate_limit_seconds: int - number of seconds to wait between API calls
# stop: str - string to stop the response at (optional)
#
# Returns:
#
# dict - the JSON response from the OpenAI API, containing the generated text
#
# Description:
#
# This function makes a POST request to the OpenAI API with the
# specified parameters to generate a response to the given prompt using
# the specified language model. The generated text is returned as a
# dictionary in JSON format. The function uses the requests library to
# make the API call and sets a timeout for the request to prevent the
# function from hanging indefinitely in case of an error.


last_request_timestamps = {}


def send_request(
    api_key,
    model,
    prompt,
    max_tokens,
    temperature,
    user_id,
    rate_limit_seconds,
    stop,
):
    if not user_id:
        raise ValueError("User ID must be provided")

    if rate_limit_seconds <= 0:
        raise ValueError("Rate limit period must be greater than 0")

    wait_if_rate_limited(user_id, rate_limit_seconds)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f"{user_id}: {prompt}"}
        ],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=timeout
    )

    last_request_timestamps[user_id] = time.time()

    check_response_for_errors(response)

    if stop:
        response_json = response.json()
        if 'choices' in response_json and response_json['choices']:
            for choice in response_json['choices']:
                if 'text' in choice and stop in choice['text'].lower():
                    raise StopIteration('Received "stop" message from AI')

    return response.json()


def wait_if_rate_limited(user_id, rate_limit_seconds):
    last_timestamp = last_request_timestamps.get(user_id, 0)

    if rate_limit_seconds and time.time(
    ) - last_timestamp < rate_limit_seconds:
        time_to_sleep = rate_limit_seconds - (
            time.time() - last_timestamp)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)


def check_response_for_errors(response):
    if response.status_code != 200:
        raise Exception(
            f'Request to OpenAI API failed with status code '
            f'{response.status_code}.'
        )

    if 'error' in response.json():
        raise Exception(response.json()['error'])
