import time
import requests

# set the timeout for the API call to 10 seconds
timeout = 10

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


def request(
    api_key,
    model,
    prompt,
    max_tokens,
    temperature,
    user_id,
    rate_limit_seconds,
    stop
):
    global last_request_timestamps

    # Check that the user ID is valid
    if not user_id:
        raise ValueError("User ID must be provided")

    # Check that the rate limit period is greater than 0
    if rate_limit_seconds <= 0:
        raise ValueError("Rate limit period must be greater than 0")

    # Get the last timestamp for this user, or set to 0 if it doesn't exist
    last_timestamp = last_request_timestamps.get(user_id, 0)

    # If rate limiting is enabled and the time since the last request is less
    # than the rate limit, sleep for the remaining time
    if rate_limit_seconds and time.time() - last_timestamp < rate_limit_seconds:
        time_to_sleep = rate_limit_seconds - (time.time() - last_timestamp)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

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
        timeout=timeout,
    )

    # Update the last request timestamp for this user
    last_request_timestamps[user_id] = time.time()

    # Check if the response was successful
    if response.status_code != 200:
        raise Exception(
            f'Request to OpenAI API failed with status code {response.status_code}.'
        )

    # Check if the response contains any errors
    if 'error' in response.json():
        raise Exception(response.json()['error'])

    # If the "stop" parameter is True, raise an exception to stop the program
    if stop:
        response_json = response.json()
        if 'choices' in response_json and response_json['choices']:
            for choice in response_json['choices']:
                if 'text' in choice and stop in choice['text'].lower():
                    raise StopIteration('Received "stop" message from AI')

    # print(response.json())

    return response.json()