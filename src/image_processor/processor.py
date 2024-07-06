from src.openai_client.client import OpenAIClient


class ImageProcessor:
    def __init__(self, openai_api_client: OpenAIClient):
        self.openai_api_client = openai_api_client

    def get_image_with_tags(self, image_url, max_tags=10):
        """Fetches an image from a URL and returns the top relevant tags."""
        tags = self.openai_api_client.generate_image_tags(image_url, max_tags)
        return {"image_url": image_url, "tags": tags}
