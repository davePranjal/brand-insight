from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from typing import List


class Image(BaseModel):
    url: HttpUrl  # Ensures the URL is valid
    description: str


class Campaign(BaseModel):
    campaign_id: str
    campaign_text: str
    images: List[dict]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
