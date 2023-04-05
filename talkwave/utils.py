import json
import requests

# set the timeout for the API call to 10 seconds
timeout = 10

# Function Name: curl_request

# Parameters:

# key: str - API key for OpenAI authentication
# model: str - name of the language model to use for generating text
# prompt: str - text prompt to feed into the language model
# max_tokens: int - maximum number of tokens to generate in the response
# temperature: float - level of "creativity" to use when generating text
# Returns:

# dict - the JSON response from the OpenAI API, containing the generated text
# Description:
# This function makes a POST request to the OpenAI API with the specified parameters to generate a response to the given prompt using the specified language model. The generated text is returned as a dictionary in JSON format. The function uses the requests library to make the API call and sets a timeout for the request to prevent the function from hanging indefinitely in case of an error.


def curl_request(api_key, model, prompt, max_tokens, temperature):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions', headers=headers, json=data, timeout=timeout)
    return response.json()
