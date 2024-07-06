import os

from pymongo import MongoClient, ASCENDING
from datetime import datetime

from src.database.models import Campaign
from src.utils.id_utils import generate_alphanumeric_id


class CampaignDB:
    def __init__(self, db_name="ad_campaigns", collection_name="campaigns"):
        db_url = os.environ.get("MONGO_DB_URL")
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        self.collection.create_index([("campaign_id", ASCENDING)], unique=True)

    def insert_campaign(self, campaign_text, images):
        """Inserts a new ad campaign document into the database."""
        campaign_id = generate_alphanumeric_id()
        data = Campaign(
            campaign_id=campaign_id,
            campaign_text=campaign_text,
            images=images,
            timestamp=datetime.utcnow())
        self.collection.insert_one(data.model_dump())
        return campaign_id

    def get_campaign_by_id(self, campaign_id):
        """Retrieves a campaign document by its ID."""
        campaign_data = self.collection.find_one({"campaign_id": campaign_id})
        if campaign_data:
            return Campaign(**campaign_data)
        return None

    def update_campaign(self, campaign_id, updated_data):
        """Updates an existing campaign document."""
        result = self.collection.update_one(
            {"campaign_id": campaign_id},
            {"$set": updated_data}
        )
        return result.modified_count

    def delete_campaign(self, campaign_id):
        """Deletes a campaign document by its ID."""
        result = self.collection.delete_one({"campaign_id": campaign_id})
        return result.deleted_count
