from src.filters.pg_filter import PGFilter
from src.filters.relevance_filter import RelevanceFilter
from src.openai_client.client import OpenAIClient


class OpenAIDataFetcher:

    def __init__(self):
        self.openai_client = OpenAIClient()
        self.pg_filter = PGFilter(self.openai_client)
        self.relevance_filter = RelevanceFilter(self.openai_client)

    def generate_campaign(self, prompt: str, brand_info: list):
        campaign_text = self.openai_client.generate_text(prompt, brand_info)
        if not self.pg_filter.apply(campaign_text):
            raise Exception("Inappropriate Content")
        if not self.relevance_filter.apply(campaign_text):
            raise Exception("Irrelevant Content")
        return campaign_text

    def get_brand_answers(self, brand_info: list, questions: list):
        prompt = "Answer these questions using the brand context provided through the brand urls"
        answers = self.openai_client.generate_text(prompt=prompt, brand_info=brand_info, questions=questions)
        if not self.pg_filter.apply(answers):
            raise Exception("Inappropriate Content")
        if not self.relevance_filter.apply(answers):
            raise Exception("Irrelevant Content")
        return answers
