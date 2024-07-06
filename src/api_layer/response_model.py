from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class CampaignResponse(BaseModel):
    campaign_id: str
    campaign_text: str
    images: List[dict] = Field(
        ...,
        description="List of relevant images with URLs and descriptions."
    )


class BrandQuestionResponse(BaseModel):
    answer: str
