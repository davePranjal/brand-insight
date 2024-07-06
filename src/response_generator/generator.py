import re
from collections import defaultdict

from src.database.db import CampaignDB


class ResponseGenerator:

    def __init__(self):
        self.db = CampaignDB()

    def build_response(self, openai_response, image_processor_response):
        """
        Builds the final response using OpenAI and image processor data.

        Returns:
            A dictionary with the following structure:
            {
                "campaign": campaign_id,
                "body": (filtered text from OpenAI response),
                "images": [
                    {
                        "url": (image URL),
                        "description": (keywords associated with the image)
                    }
                    # ... more images
                ]
            }
        """
        filtered_text = openai_response

        keyword_to_images = defaultdict(list)
        for item in image_processor_response:
            for keyword in item["tags"]:
                keyword_to_images[keyword].append({"image_url": item["image_url"], "description": keyword})

        response = {"campaign_id": "", "body": filtered_text, "images": []}

        for keyword, images in keyword_to_images.items():
            if re.search(r"\b" + re.escape(keyword) + r"\b", filtered_text, re.IGNORECASE):
                response["images"].extend(images)

        campaign_id = self.db.insert_campaign(response.get("body"), response.get("images"))
        response["campaign_id"] = campaign_id
        return response

    def build_response(self, answer: str):
        """
       Builds the final response for the brand questions.

       Returns:
           The text generated via OpenAI API containing the answers
        """
        return answer
