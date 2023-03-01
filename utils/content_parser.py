from typing import List


def parse_content(response: dict) -> List[str]:
    """
    Parse all the contents and return string list
    """

    contents = []
    for choice in response['choices']:
        content = choice['text']
        contents.append(content)

    return contents


def save_from_response(response: dict, file_path: str) -> str:
    """
    Returns the saved file path
    """

    contents = parse_content(response)

    with open(file_path, 'w') as file:
        for content in contents:
            file.write(content)

    return file_path
