from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field
from src.service_layer.service import RequestProcessor
import uuid
import os
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

from src.api_layer.request_model import CampaignRequest, BrandQuestionRequest
from src.api_layer.response_model import CampaignResponse, BrandQuestionResponse

app = FastAPI(title="Ad Campaign and Brand Q&A API")
request_processor = RequestProcessor()


# API Endpoints
@app.post("/campaigns", response_model=CampaignResponse)
async def create_ad_campaign(request: CampaignRequest):
    try:
        # Process the request and generate the campaign
        campaign = dict(request_processor.process_request(request.prompt, request.brand_urls))
        return CampaignResponse(campaign_id=campaign.get("campaign_id"), campaign_text=campaign.get("body"),
                                images=campaign.get("images"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/brands/answer", response_model=BrandQuestionResponse)
async def answer_brand_question(request: BrandQuestionRequest):
    try:
        # Process the question and generate the answer
        response = request_processor.answer_brand_question(
            request.questions, request.brand_urls, request.use_previous_context
        )
        return BrandQuestionResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
