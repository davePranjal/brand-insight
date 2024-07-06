from typing import List, Optional
from pydantic import BaseModel, Field


class CampaignRequest(BaseModel):
    prompt: str = Field(..., description="Description of the desired ad campaign.")
    brand_urls: List[str] = Field(..., description="List of URLs related to the brand.")


class BrandQuestionRequest(BaseModel):
    questions: list = Field(..., description="The questions to be answered about the brand.")
    brand_urls: Optional[List[str]] = Field(
        None, description="Optional list of URLs for context."
    )
    use_previous_context: bool = Field(
        False, description="Use previously stored context if available."
    )
