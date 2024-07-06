import random
import string


def generate_alphanumeric_id(length=6):
    """
    Generates a random human-readable alphanumeric ID of the specified length.

    Args:
        length: The desired length of the ID (default: 6).

    Returns:
        A string representing the generated ID.
    """
    characters = string.ascii_uppercase + string.digits  # Uppercase letters and digits
    return ''.join(random.choices(characters, k=length))
