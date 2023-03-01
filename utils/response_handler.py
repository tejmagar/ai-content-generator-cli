import json
import openai


def fetch_response(api_key: str, prompt: str, max_tokens: int, model='text-davinci-003') -> dict:
    """
    Fetch data from api and returns its response in json format
    """

    openai.api_key = api_key

    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    data = json.loads(str(response))

    return data
