import base64
import logging
from io import BytesIO

import openai
import os
import json
from functools import lru_cache

import requests
from PIL import Image


class OpenAIClient:
    def __init__(self, api_key: str = os.environ.get("OPENAI_API_KEY"), initial_context: dict = {}):
        openai.api_key = api_key
        self.model = os.environ.get("OPENAI_MODEL")
        self.context = initial_context
        self.cache = {}  # Simple cache for demonstration; consider LRU cache for production

    def update_context(self, brand_info: list):
        """Updates the context with the provided brand information."""
        for brand in brand_info:
            self.context.setdefault("brand-info", []).append(brand)

    def has_context(self):
        return "brand-info" in self.context and self.context["brand-info"]

    def get_context(self):
        return self.context

    # @lru_cache(maxsize=128)  # Optional LRU cache for efficiency
    def generate_text(self, prompt: str, brand_info: list, questions: list = None):
        """Generates a campaign using the OpenAI API, potentially using cached results."""

        # Construct request data
        request_data = self._build_openai_request(prompt, brand_info, questions)

        # Hash the request data to use as a cache key
        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response  # Store in cache

        return response.choices[0].message.content

    # @lru_cache(maxsize=128)  # Optional LRU cache for efficiency
    def generate_image_tags(self, image_url, max_tags=10):
        """Fetches an image from a URL and returns the top relevant tags."""
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception if the request fails
        try:
            image = Image.open(BytesIO(response.content)).convert("RGB")
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()  # Remove .encode()
            image_b64 = f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            logging.warning(f"Not able to parse image url {image_url} due to {e}")
            return []

        request_data = self._build_openai_image_request(image_b64)

        # Hash the request data to use as a cache key
        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response  # Store in cache

        tags_string = response.choices[0].message.content.strip()
        tags = [tag.strip() for tag in tags_string.split(",")]
        return tags[:max_tags]  # Return top max_tags

    def generate_image(self, campaign: dict, brand_images: list, num_images: int = 2):
        """Generates images using DALL-E based on campaign and brand image URLs."""
        images = []
        for _ in range(num_images):
            # Combine campaign details and brand image for prompt
            prompt = f"Create an image for the following campaign: {campaign}. Use elements from these brand images: {brand_images}."
            image_response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
            images.append(image_response["data"][0]["url"])
        return images

    def query_openai(self, prompt: str, message: str):
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,  # Adjust temperature for creativity
            "max_tokens": 1000,  # Adjust as needed
        }

        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response  # Store in cache

        return response.choices[0].message.content.strip()

    def _build_openai_request(self, prompt: str, brand_info: list, questions: list = None) -> dict:
        """Constructs the request payload for the OpenAI API call."""

        messages = [
            {"role": "system", "content": "You are an AI marketing assistant."},
            {"role": "user", "content": self._create_context_string(brand_info, prompt, questions)}
        ]
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,  # Adjust temperature for creativity
            "max_tokens": 1000,  # Adjust as needed
        }
        return request_data

    def _build_openai_image_request(self, image_url: str) -> dict:
        """Constructs the request payload for the OpenAI API call."""

        content = [
            {"type": "text",
             "text": "What are the top 10 most relevant tags for this image? Return only the tags as a comma-separated list"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]

        messages = [
            {"role": "system", "content": "You are an AI marketing assistant."},
            {"role": "user", "content": content}
        ]

        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,  # Adjust temperature for creativity
            "max_tokens": 1000,  # Adjust as needed
        }
        return request_data

    def _parse_openai_response(self, response) -> dict:
        """Parses the raw response from the OpenAI API into the desired format."""
        response_text = response.choices[0].message.content
        try:
            # Try to parse the response as JSON
            parsed_response = json.loads(response_text)

            # If the response doesn't match the expected format, try to extract the content as the body
            if "campaign" not in parsed_response:
                parsed_response = {"campaign": {"body": response_text}}

        except json.JSONDecodeError:
            # If the response is not JSON, return it as the body
            parsed_response = {"campaign": {"body": response_text}}

        return parsed_response

    def _create_context_string(self, brand_info: list, prompt: str, questions: list = None) -> str:
        """Creates a context string by combining brand info, prompt, and optional questions."""
        context_string = ""
        for brand in brand_info:
            context_string += f"Brand URL: {brand['url']}\n"
            context_string += f"URL Text: {brand['text']}\n"
            context_string += f"URL Images: {', '.join(brand['images'])}\n\n"

        context_string += f"Prompt: {prompt}\n"

        if questions:
            context_string += "Questions:\n"
            for question in questions:
                context_string += f"- {question}\n"

        return context_string
