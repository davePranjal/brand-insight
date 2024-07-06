from src.filters.filter import Filter
from src.openai_client.client import OpenAIClient


class PGFilter(Filter):
    def __init__(self, openai_api_client: OpenAIClient):
        self.prohibited_categories = ["profanity", "vulgarity", "racist", "hateful"]
        self.openai_api_client = openai_api_client

    def apply(self, text, **kwargs):
        """
        Applies the PG filter to the input text.

        Args:
            text: The text to be filtered.

        Returns:
            bool: True if the text passes the filter, False otherwise.
        """
        message = f"""Given the following text:
                '{text}'

               Identify any mentions of the following prohibited categories {self.prohibited_categories} in the text. 
               If you are unsure whether a mentioned category is a present, err on the side of including it.
               Return yes if the text contains words from of the prohibited categories and no otherwise."""
        prompt = "You are an expert in identifying intent and words in a text."
        response = self.openai_api_client.query_openai(prompt, message)

        contains_profanity = response.strip()
        if contains_profanity.lower().__contains__("no"):
            return True
        else:
            return False
