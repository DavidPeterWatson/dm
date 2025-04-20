from datetime import datetime, timezone
from typing import List, Optional
from models.campaign import Campaign
from bson.objectid import ObjectId
from .db_operations import objectid_to_str, Database

def create_campaign(db: Database, name: str, description: str) -> Campaign:
    # Check if a campaign with this name already exists
    existing_campaign = db.campaigns_collection.find_one({"name": name})
    if existing_campaign:
        raise ValueError(f"A campaign with the name '{name}' already exists")
    
    now = datetime.now(timezone.utc)
    # Create a new ObjectId first
    oid = ObjectId()
    str_id = objectid_to_str(oid)
    
    campaign = {
        "_id": oid,
        "id": str_id,  # Store the string ID in the document
        "name": name,
        "description": description,
        "data": {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    db.campaigns_collection.insert_one(campaign)
    
    # For the Pydantic model
    campaign_dict = {
        "id": str_id,
        "name": name,
        "description": description,
        "data": {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    return Campaign(**campaign_dict)

def update_campaign(db: Database, campaign_id: str, name: str, description: str) -> Campaign:
    # Find by string ID
    campaign = db.campaigns_collection.find_one({"id": campaign_id})
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    updated_fields = {
        "name": name,
        "description": description,
        "updated_at": now.isoformat()
    }
    db.campaigns_collection.update_one({"id": campaign_id}, {"$set": updated_fields})
    
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

def delete_campaign(db: Database, campaign_id: str) -> bool:
    result = db.campaigns_collection.delete_one({"id": campaign_id})
    if result.deleted_count > 0:
        return True
    return False

def search_campaigns(db: Database, query: str) -> List[Campaign]:
    results = db.campaigns_collection.find({"$or": [
        {"name": {"$regex": query, "$options": "i"}},
        {"description": {"$regex": query, "$options": "i"}}
    ]})
    campaigns = []
    for campaign in results:
        campaign_dict = {
            "id": campaign["id"],
            "name": campaign["name"],
            "description": campaign["description"],
            "data": campaign.get("data", {}),
            "created_at": campaign["created_at"],
            "updated_at": campaign["updated_at"]
        }
        campaigns.append(Campaign(**campaign_dict))
    return campaigns

def get_campaign(db: Database, campaign_id: str) -> Campaign:
    campaign = db.campaigns_collection.find_one({"id": campaign_id})
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    # Convert datetime objects to ISO strings if needed
    created_at = campaign["created_at"]
    updated_at = campaign["updated_at"]
    
    # If they're datetime objects, convert to ISO strings
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()
    if isinstance(updated_at, datetime):
        updated_at = updated_at.isoformat()
    
    campaign_dict = {
        "id": campaign["id"],
        "name": campaign["name"],
        "description": campaign["description"],
        "data": campaign.get("data", {}),
        "created_at": created_at,
        "updated_at": updated_at
    }
    return Campaign(**campaign_dict)

def get_campaign_by_name(db: Database, name: str) -> Optional[Campaign]:
    campaign = db.campaigns_collection.find_one({"name": name})
    if not campaign:
        return None
    
    # Convert datetime objects to ISO strings if needed
    created_at = campaign["created_at"]
    updated_at = campaign["updated_at"]
    
    # If they're datetime objects, convert to ISO strings
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()
    if isinstance(updated_at, datetime):
        updated_at = updated_at.isoformat()
    
    campaign_dict = {
        "id": campaign["id"],
        "name": campaign["name"],
        "description": campaign["description"],
        "data": campaign.get("data", {}),
        "created_at": created_at,
        "updated_at": updated_at
    }
    return Campaign(**campaign_dict)

def list_campaigns(db: Database) -> List[Campaign]:
    campaigns = db.campaigns_collection.find()
    campaign_list = []
    for campaign in campaigns:
        # Convert datetime objects to ISO strings if needed
        created_at = campaign["created_at"]
        updated_at = campaign["updated_at"]
        
        # If they're datetime objects, convert to ISO strings
        if isinstance(created_at, datetime):
            created_at = created_at.isoformat()
        if isinstance(updated_at, datetime):
            updated_at = updated_at.isoformat()
        
        campaign_dict = {
            "id": campaign["id"],
            "name": campaign["name"],
            "description": campaign["description"],
            "data": campaign.get("data", {}),
            "created_at": created_at,
            "updated_at": updated_at
        }
        campaign_list.append(Campaign(**campaign_dict))
    return campaign_list

def delete_all_campaigns(db: Database) -> int:
    result = db.campaigns_collection.delete_many({})
    return result.deleted_count
