import requests
import filetype
import os


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def is_image_url(url):
    """Checks if a URL points to an image by examining the Content-Type header."""
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get("content-type")
        return content_type and content_type.startswith("image/")
    except requests.exceptions.RequestException:
        return False
