from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from models.setting import Setting
from bson.objectid import ObjectId
from .db_operations import objectid_to_str, Database

def create_setting(db: Database, **setting_data: Dict[str, Any]) -> Setting:
    # Check if a setting with this name already exists
    existing_setting = db.settings_collection.find_one({"name": setting_data["name"]})
    if existing_setting:
        raise ValueError(f"A setting with the name '{setting_data['name']}' already exists")
    
    now = datetime.now(timezone.utc)
    # Create a new ObjectId first
    oid = ObjectId()
    str_id = objectid_to_str(oid)
    
    # Prepare the document for MongoDB
    setting_doc = {
        "_id": oid,
        "id": str_id,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    
    # Add all fields from setting_data
    for key, value in setting_data.items():
        setting_doc[key] = value
    
    db.settings_collection.insert_one(setting_doc)
    
    # For the Pydantic model
    setting_dict = {
        "id": str_id,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        **setting_data  # Include all provided setting data
    }
    return Setting(**setting_dict)

def update_setting(db: Database, setting_id: str, **update_data: Dict[str, Any]) -> Setting:
    # Find by string ID
    setting = db.settings_collection.find_one({"id": setting_id})
    if not setting:
        raise ValueError(f"Setting with ID {setting_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    update_data["updated_at"] = now.isoformat()
    
    db.settings_collection.update_one(
        {"id": setting_id},
        {"$set": update_data}
    )
    
    # Get the updated document
    updated_setting = db.settings_collection.find_one({"id": setting_id})
    if not updated_setting:
        raise ValueError(f"Failed to retrieve updated setting with ID {setting_id}")
    
    # Convert to Pydantic model
    setting_dict = {
        "id": setting_id,
        "created_at": updated_setting["created_at"],
        "updated_at": now.isoformat(),
        **{k: v for k, v in updated_setting.items() if k not in ["_id", "id", "created_at", "updated_at"]}
    }
    return Setting(**setting_dict)

def delete_setting(db: Database, setting_id: str) -> bool:
    result = db.settings_collection.delete_one({"id": setting_id})
    return result.deleted_count > 0

def search_settings(db: Database, query: str) -> List[Setting]:
    results = db.settings_collection.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"region": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    })
    return [_convert_to_setting(setting) for setting in results]

def filter_settings_by_type(db: Database, setting_type: str) -> List[Setting]:
    results = db.settings_collection.find({"setting_type": setting_type})
    return [_convert_to_setting(setting) for setting in results]

def get_setting(db: Database, setting_id: str) -> Setting:
    setting = db.settings_collection.find_one({"id": setting_id})
    if not setting:
        raise ValueError(f"Setting with ID {setting_id} does not exist.")
    return _convert_to_setting(setting)

def get_setting_by_name(db: Database, name: str) -> Optional[Setting]:
    setting = db.settings_collection.find_one({"name": name})
    if not setting:
        return None
    return _convert_to_setting(setting)

def list_settings(db: Database) -> List[Setting]:
    settings = db.settings_collection.find()
    return [_convert_to_setting(setting) for setting in settings]

def delete_all_settings(db: Database) -> int:
    result = db.settings_collection.delete_many({})
    return result.deleted_count

def _convert_to_setting(setting_doc: Dict) -> Setting:
    """Helper function to convert a MongoDB document to a Setting model."""
    # Convert datetime objects to ISO strings if needed
    created_at = setting_doc["created_at"]
    updated_at = setting_doc["updated_at"]
    
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()
    if isinstance(updated_at, datetime):
        updated_at = updated_at.isoformat()
    
    # Create the dictionary for the Pydantic model
    setting_dict = {
        "id": setting_doc["id"],
        "created_at": created_at,
        "updated_at": updated_at,
        **{k: v for k, v in setting_doc.items() if k not in ["_id", "id", "created_at", "updated_at"]}
    }
    return Setting(**setting_dict)

def filter_settings_by_parent(db: Database, parent_id: str) -> List[Setting]:
    """
    Filter settings to get all children of a specific parent setting.
    
    Args:
        db: Database instance
        parent_id: ID of the parent setting
        
    Returns:
        List of Setting objects that are children of the specified parent
    """
    results = db.settings_collection.find({"parent_id": parent_id})
    return [_convert_to_setting(setting) for setting in results]

def get_setting_children(db: Database, parent_id: str) -> List[Setting]:
    """
    Get all child settings of a specific parent setting.
    
    Args:
        db: Database instance
        parent_id: ID of the parent setting
        
    Returns:
        List of Setting objects that are children of the specified parent
    """
    # This is essentially the same as filter_settings_by_parent,
    # created as a separate function for semantic clarity
    return filter_settings_by_parent(db, parent_id) 