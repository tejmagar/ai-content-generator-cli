import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass
class Prompt:
    questions = []
    text = ''


class AbstractQuestion(ABC):
    """
    Base class for CLI question
    """

    def __init__(self):
        question_title = self.get_question_title()
        if not question_title:
            raise ValueError('Question title cannot be None')

        self.answer = input(f'{question_title}: ')

    def get_answer(self) -> str:
        """
        Returns answer entered by the user for the current question
        """
        return self.answer

    @abstractmethod
    def get_question_title(self) -> str:
        """
        Returns question title
        """

        pass

    @abstractmethod
    def generate_prompt_text(self) -> str:
        """
        Generate prompt text for the current question and returns it.
        Customize it for better output.
        """

        pass


class PostTitleQuestion(AbstractQuestion):
    """
    Asks post title to the user.
    """

    def get_question_title(self) -> str:
        return 'Post title'

    def generate_prompt_text(self) -> str:
        return f'Write a blog post for: {self.answer}.'


class KeywordQuestion(AbstractQuestion):
    """
    Asks keywords to use to in the post.
    """

    def get_question_title(self) -> str:
        return 'Keywords (Leave blank if none)'

    def generate_prompt_text(self) -> str:
        if len(self.get_answer()) > 0:
            return f'Optimize content by using keywords {self.get_answer()}.'

        return ''


class WordCountQuestion(AbstractQuestion):
    """
    Asks keywords to use to in the post.
    """

    def __init__(self):
        super().__init__()

        # Word count should be  a number
        while not self.get_answer().isnumeric():
            super().__init__()

    def get_question_title(self) -> str:
        return 'Word Count'

    def generate_prompt_text(self) -> str:
        return f'It should be about {self.get_answer()} words.'


class ExtraNoteQuestion(AbstractQuestion):
    """
    Ask if anything extra note to user
    """

    def get_question_title(self) -> str:
        return 'Extra note'

    def generate_prompt_text(self) -> str:
        if len(self.answer) == 0:
            return ''

        return f'{self.answer}.'


"""
 =============================================================================
 Add here custom questions for better output.
 Extend a AbstractQuestion class to add your own custom questions.
 Remove a class from list below to remove unwanted question.
 =============================================================================
"""

questions_classes = [
    PostTitleQuestion,
    KeywordQuestion,
    WordCountQuestion,
    ExtraNoteQuestion
]


def generate_prompt() -> Prompt:
    """
    Generate prompt based on the questions asked.
    """

    prompt = Prompt()

    for question_class in questions_classes:
        question = question_class()
        prompt.questions.append(question)
        prompt.text += f'{question.generate_prompt_text()} '

    return prompt
