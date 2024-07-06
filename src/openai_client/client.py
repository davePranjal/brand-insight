import base64
import logging
from io import BytesIO

import openai
import os
import json

import requests
from PIL import Image


class OpenAIClient:
    def __init__(self, api_key: str = os.environ.get("OPENAI_API_KEY")):
        openai.api_key = api_key
        self.model = os.environ.get("OPENAI_MODEL")
        self.cache = {}

    def generate_text(self, prompt: str, brand_info: list, questions: list = None):
        """Generates text using the prompt and OpenAI API."""

        request_data = self._build_openai_request(prompt, brand_info, questions)

        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response

        return response.choices[0].message.content

    def generate_image_tags(self, image_url, max_tags=10):
        """Fetches an image from a URL and returns the top relevant tags."""
        response = requests.get(image_url)
        response.raise_for_status()
        try:
            image = Image.open(BytesIO(response.content)).convert("RGB")
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_b64 = f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            logging.warning(f"Not able to parse image url {image_url} due to {e}")
            return []

        request_data = self._build_openai_image_request(image_b64, max_tags)

        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response

        tags_string = response.choices[0].message.content.strip()
        tags = [tag.strip() for tag in tags_string.split(",")]
        return tags[:max_tags]

    def query_openai(self, prompt: str, message: str):
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        cache_key = hash(str(json.dumps(request_data, sort_keys=True)))

        if cache_key in self.cache:
            response = self.cache[cache_key]
        else:
            response = openai.chat.completions.create(**request_data)
            self.cache[cache_key] = response

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
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        return request_data

    def _build_openai_image_request(self, image_url: str, max_tags: int) -> dict:
        """Constructs the request payload for the OpenAI API call."""

        content = [
            {"type": "text",
             "text": f"What are the top {max_tags} most relevant tags for this image? Return only the tags as a comma-separated list"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]

        messages = [
            {"role": "system", "content": "You are an AI marketing assistant."},
            {"role": "user", "content": content}
        ]

        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        return request_data

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
