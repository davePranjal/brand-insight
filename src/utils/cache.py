import json
import redis

class CampaignCache:
    def __init__(self, host="localhost", port=6379, db=0, ttl=3600):  # Default TTL of 1 hour
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.ttl = ttl

    def set_campaign_context(self, campaign_id, brand_info, prompt=None):
        """Stores the brand context data for a campaign in the Redis cache."""
        key = f"campaign_context:{campaign_id}"
        value = {
            "brand-info": brand_info,
            "prompt": prompt
        }
        self.redis.setex(key, self.ttl, json.dumps(value))  # Set with expiration

    def get_campaign_context(self, campaign_id):
        """Retrieves the brand context data for a campaign from the cache."""
        key = f"campaign_context:{campaign_id}"
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def delete_campaign_context(self, campaign_id):
        """Deletes the cached data for a specific campaign."""
        key = f"campaign_context:{campaign_id}"
        self.redis.delete(key)
