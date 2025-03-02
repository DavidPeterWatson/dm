from pymongo import MongoClient
from bson.objectid import ObjectId
from models.campaign import Campaign
from datetime import datetime, timezone
from typing import List, Optional
import os

# Default connection settings
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "dnd_gm")

# Initialize with None, will be set up in init_db
client = None
db = None
campaigns_collection = None

def init_db(db_name: Optional[str] = None):
    """Initialize database connection with optional database name override"""
    global client, db, campaigns_collection
    
    # Use provided db_name or fall back to default
    actual_db_name = db_name or DB_NAME
    
    client = MongoClient(MONGODB_URI)
    db = client[actual_db_name]
    campaigns_collection = db["campaigns"]
    return db

# Initialize with default settings
init_db()

# Helper function to convert between MongoDB ObjectId and integer ID
def objectid_to_int(oid):
    return int(str(oid)[-8:], 16)

def int_to_objectid(int_id):
    # Store a mapping from integer IDs to ObjectIds
    # This is a simplified approach - in a real app, you'd need a more robust solution
    campaign = campaigns_collection.find_one({"int_id": int_id})
    if campaign:
        return campaign["_id"]
    raise ValueError(f"No campaign found with ID {int_id}")

def create_campaign(name: str, description: str) -> Campaign:
    now = datetime.now(timezone.utc)
    # Create a new ObjectId first
    oid = ObjectId()
    int_id = objectid_to_int(oid)
    
    campaign = {
        "_id": oid,
        "int_id": int_id,  # Store the integer ID in the document
        "name": name,
        "description": description,
        "data": {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    campaigns_collection.insert_one(campaign)
    
    # For the Pydantic model
    campaign_dict = {
        "id": int_id,
        "name": name,
        "description": description,
        "data": {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    return Campaign(**campaign_dict)

def update_campaign(campaign_id: int, name: str, description: str) -> Campaign:
    # Find by integer ID
    campaign = campaigns_collection.find_one({"int_id": campaign_id})
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    updated_fields = {
        "name": name,
        "description": description,
        "updated_at": now.isoformat()
    }
    campaigns_collection.update_one({"int_id": campaign_id}, {"$set": updated_fields})
    
    # For the Pydantic model
    campaign_dict = {
        "id": campaign_id,
        "name": name,
        "description": description,
        "data": campaign.get("data", {}),
        "created_at": campaign["created_at"],
        "updated_at": now.isoformat()
    }
    return Campaign(**campaign_dict)

def delete_campaign(campaign_id: int) -> bool:
    result = campaigns_collection.delete_one({"int_id": campaign_id})
    if result.deleted_count > 0:
        return True
    return False

def search_campaigns(query: str) -> List[Campaign]:
    results = campaigns_collection.find({"$or": [
        {"name": {"$regex": query, "$options": "i"}},
        {"description": {"$regex": query, "$options": "i"}}
    ]})
    campaigns = []
    for campaign in results:
        campaign_dict = {
            "id": campaign["int_id"],
            "name": campaign["name"],
            "description": campaign["description"],
            "data": campaign.get("data", {}),
            "created_at": campaign["created_at"],
            "updated_at": campaign["updated_at"]
        }
        campaigns.append(Campaign(**campaign_dict))
    return campaigns

def get_campaign(campaign_id: int) -> Campaign:
    campaign = campaigns_collection.find_one({"int_id": campaign_id})
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    campaign_dict = {
        "id": campaign["int_id"],
        "name": campaign["name"],
        "description": campaign["description"],
        "data": campaign.get("data", {}),
        "created_at": campaign["created_at"],
        "updated_at": campaign["updated_at"]
    }
    return Campaign(**campaign_dict)

def list_campaigns() -> List[Campaign]:
    campaigns = campaigns_collection.find()
    campaign_list = []
    for campaign in campaigns:
        campaign_dict = {
            "id": campaign["int_id"],
            "name": campaign["name"],
            "description": campaign["description"],
            "data": campaign.get("data", {}),
            "created_at": campaign["created_at"],
            "updated_at": campaign["updated_at"]
        }
        campaign_list.append(Campaign(**campaign_dict))
    return campaign_list

def clear_database():
    """Clear all campaigns from the database"""
    campaigns_collection.delete_many({})
    return True 