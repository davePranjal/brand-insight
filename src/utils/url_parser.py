import logging

import requests
from bs4 import BeautifulSoup

from src.utils import utils


def parse_webpage(url):
    """
    Fetches text and image URLs from a webpage and returns them in JSON format.

    Args:
        url: The URL of the webpage to parse.

    Returns:
        A dictionary containing:
            - "url": The given url.
            - "text": A list of extracted text content from the webpage.
            - "images": A list of URLs to images found on the webpage.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the webpage: {e}")
        return {"text": [], "images": []}

    soup = BeautifulSoup(response.text, 'html.parser')

    text_content = [p.text for p in soup.find_all('p')]

    img_tags = soup.find_all('img')
    image_urls = list(filter(utils.is_image_url, [img.get('src')
                                                  for img in img_tags if img.get('src')]))
    return {"url": url, "text": text_content, "images": image_urls}
