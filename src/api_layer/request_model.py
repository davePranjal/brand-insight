from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class CampaignRequest(BaseModel):
    prompt: str = Field(..., description="Description of the desired ad campaign.")
    brand_urls: List[str] = Field(..., description="List of URLs related to the brand.")


class BrandQuestionRequest(BaseModel):
    question: str = Field(..., description="The question to be answered about the brand.")
    brand_urls: Optional[List[HttpUrl]] = Field(
        None, description="Optional list of URLs for context."
    )
    use_previous_context: bool = Field(
        False, description="Use previously stored context if available."
    )
