import os
from pathlib import Path

from slugify import slugify

from utils import dialogue, response_handler, content_parser
from dotenv import load_dotenv

from utils.dialogue import Prompt, PostTitleQuestion

load_dotenv()


def get_api_key():
    """
    Read Open AI API token from environment variable.
    Returns None if there is no key.
    """

    return os.environ.get('API_SECRET', None)


def create_api_key(api_key: str):
    """ Create a .env file and create API_SECRET variable """

    with open('.env', 'w') as file:
        file.write(f'API_SECRET={api_key}')  # Key value pair


def ask_user_apikey():
    """
    Take input from user
    """

    message = "Visit https://platform.openai.com/account/api-keys to get your free Open AI API key\n"
    print(message)

    api_key = input('Your API KEY: ')
    create_api_key(api_key=api_key.strip())
    print('API key saved successfully. Please run again to continue.')

    # Exit current session and reload variables
    exit(0)


def generate_prompt() -> Prompt:
    """
    Ask necessary questions to generate a prompt.
    Edit > utils > dialogue.py for custom prompts.
    """
    prompt = dialogue.generate_prompt()
    return prompt


def ask_max_tokens() -> int:
    print('\nNote: 1,000 tokens is about 750 words.\n')
    max_tokens = input('Max Token: ')

    if not max_tokens.isnumeric():
        print('Enter a number')
        ask_max_tokens()  # Invalid input

    return int(max_tokens)


def get_title(prompt: Prompt) -> str:
    """
    Finds title from available prompts
    """

    for question in prompt.questions:

        if type(question) == PostTitleQuestion:
            return question.get_answer()


def seo_mixin(prompt: Prompt):
    prompt.text += "It should support html and don't forget to use necessary html tags." \
                   "Use line break when necessary. Each " \
                   "paragraph should be 200 approx. " \
                   "Always follow seo rules while writing content." \
                   "Always use <p> tag for paragraph. It should be a structured content." \
                   "Tell like you are confident experienced person. Try to use more active voice." \
                   "Try to include word 'you' in the sentence like this article is saying to the reader. " \
                   "Article should be high quality and plagiarism free. " \
                   "Use a tone with a shorter sentence that high school kid can understand "


def init():
    """
    Initialize by getting api key and generating prompt
    """

    api_key = get_api_key()

    if not api_key:
        ask_user_apikey()
        return

    prompt = generate_prompt()
    seo_mixin(prompt)

    max_tokens = ask_max_tokens()

    # Waiting message
    print('Please wait...')

    response = response_handler.fetch_response(
        api_key=api_key,
        prompt=prompt.text,
        max_tokens=max_tokens
    )

    title = get_title(prompt=prompt)

    out_dir = Path('generated')

    if not out_dir.exists():
        out_dir.mkdir()

    save_to = Path(f'generated/{title}.html')
    content_parser.save_from_response(response=response, file_path=str(save_to))

    print(f'Generated content saved to: {save_to.absolute()}')
    slug_url = slugify(text=title)
    print('Slug:', slug_url)


init()
