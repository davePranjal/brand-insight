from datetime import datetime

from pydantic import BaseModel, Field
from typing import List


class Campaign(BaseModel):
    campaign_id: str
    campaign_text: str
    images: List[dict]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
