from datetime import datetime, timezone
from typing import List, Optional
from models.campaign import Campaign
from bson.objectid import ObjectId
from .db_operations import campaigns_collection, objectid_to_str

def create_campaign(name: str, description: str) -> Campaign:
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
    campaigns_collection.insert_one(campaign)
    
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

def update_campaign(campaign_id: str, name: str, description: str) -> Campaign:
    # Find by string ID
    campaign = campaigns_collection.find_one({"id": campaign_id})
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    updated_fields = {
        "name": name,
        "description": description,
        "updated_at": now.isoformat()
    }
    campaigns_collection.update_one({"id": campaign_id}, {"$set": updated_fields})
    
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

def delete_campaign(campaign_id: str) -> bool:
    result = campaigns_collection.delete_one({"id": campaign_id})
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
            "id": campaign["id"],
            "name": campaign["name"],
            "description": campaign["description"],
            "data": campaign.get("data", {}),
            "created_at": campaign["created_at"],
            "updated_at": campaign["updated_at"]
        }
        campaigns.append(Campaign(**campaign_dict))
    return campaigns

def get_campaign(campaign_id: str) -> Campaign:
    campaign = campaigns_collection.find_one({"id": campaign_id})
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

def get_campaign_by_name(name: str) -> Optional[Campaign]:
    campaign = campaigns_collection.find_one({"name": name})
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

def list_campaigns() -> List[Campaign]:
    campaigns = campaigns_collection.find()
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

def delete_all_campaigns() -> int:
    result = campaigns_collection.delete_many({})
    return result.deleted_count 