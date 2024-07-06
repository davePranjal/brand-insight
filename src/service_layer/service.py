from typing import Optional

from src.database.openai_data_fetcher import OpenAIDataFetcher
from src.image_processor.processor import ImageProcessor
from src.openai_client.client import OpenAIClient
from src.response_generator.generator import ResponseGenerator
from src.utils import url_parser, utils


class RequestProcessor:
    def __init__(self):
        self.openai_data_fetcher = OpenAIDataFetcher()
        self.response_generator = ResponseGenerator()
        self.image_processor = ImageProcessor(OpenAIClient())

    def process_request(self, prompt: str, brand_urls: list):
        """
        Processes the ad campaign request, generates a tagline, and associated images.

        Args:
            prompt (str): The prompt describing the ad campaign goal.
            brand_urls (list): List of URLs related to the brand.

        Returns:
            tuple: (tagline, list of image data/URLs)
        """

        # Update OpenAI context
        brand_urls = [url_parser.parse_webpage(url) for url in brand_urls]
        list_of_image_urls = utils.flatten_list([url.get("images") for url in brand_urls])
        images_with_tags = [self.image_processor.get_image_with_tags(url) for url in list_of_image_urls]
        campaign_text = self.openai_data_fetcher.generate_campaign(prompt, brand_urls)

        return self.response_generator.build_response(campaign_text, images_with_tags)

    def answer_brand_question(self, question: str, brand_urls: Optional[list] = None,
                              use_previous_context: bool = False) -> str:
        """
        Answers questions about a brand using context from provided URLs or previous interactions.

        Args:
            question (str): The question to answer.
            brand_urls (list, optional): List of URLs for context.
            use_previous_context (bool, optional): Whether to use previously stored context. Defaults to False.

        Returns:
            str: The answer to the question.
        """

        # If using previous context and it's available, fetch it
        if use_previous_context and self.openai_client.has_context():
            brand_urls = self.openai_client.get_context()["brand-info"]

        # Update or retrieve context
        if brand_urls:
            self.openai_client.update_context(brand_urls)

        # Generate answer from OpenAI
        answer = self.openai_client.generate_text(
            question, brand_urls, questions=[question]
        )["campaign"]["body"]

        return answer
