from src.filters.filter import Filter
from src.openai_client.client import OpenAIClient


class RelevanceFilter(Filter):
    def __init__(self, openai_api_client: OpenAIClient):
        self.openai_api_client = openai_api_client

    def apply(self, text, **kwargs):
        """Checks if a text mentions rival brands using OpenAI."""
        brand_name = kwargs.get("brand_name")
        message = f"""Given the following brand: '{brand_name}' and a piece of text:

        '{text}'

        Identify any mentions of rival brands in the text. 
        If you are unsure whether a mentioned brand is a rival, err on the side of including it.
        Return yes if it contains a rival brand and no otherwise"""
        prompt = "You are an expert in identifying brands and their rivals."
        response = self.openai_api_client.query_openai(prompt, message)

        rival_mentions = response.strip()
        if rival_mentions.lower().__contains__("no"):
            return True
        else:
            return False

