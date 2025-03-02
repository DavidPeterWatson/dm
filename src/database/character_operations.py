from datetime import datetime, timezone
from typing import List, Optional
from models.character import Character
from bson.objectid import ObjectId
from .db_operations import characters_collection, objectid_to_int
from .campaign_operations import get_campaign

def create_character(name: str, campaign_id: int, player_name: Optional[str] = None, 
                    race: Optional[str] = None, character_class: Optional[str] = None,
                    level: int = 1, data: Optional[dict] = None):
    # Verify campaign exists
    try:
        get_campaign(campaign_id)
    except ValueError:
        raise ValueError(f"Campaign with ID {campaign_id} does not exist.")
    
    # Check if a character with this name already exists
    existing_character = characters_collection.find_one({"name": name})
    if existing_character:
        raise ValueError(f"Character with name '{name}' already exists.")
    
    now = datetime.now(timezone.utc)
    # Create a new ObjectId first
    oid = ObjectId()
    int_id = objectid_to_int(oid)
    
    character = {
        "_id": oid,
        "int_id": int_id,
        "campaign_id": campaign_id,
        "name": name,
        "player_name": player_name,
        "race": race,
        "class": character_class,
        "level": level,
        "data": data or {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    characters_collection.insert_one(character)
    
    # For the Pydantic model
    character_dict = {
        "id": int_id,
        "campaign_id": campaign_id,
        "name": name,
        "player_name": player_name,
        "race": race,
        "class": character_class,
        "level": level,
        "data": data or {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    return Character(**character_dict)

def update_character(character_id: int, **kwargs):
    # Find by integer ID
    character = characters_collection.find_one({"int_id": character_id})
    if not character:
        raise ValueError(f"Character with ID {character_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    
    # Prepare update fields
    updated_fields = {"updated_at": now.isoformat()}
    
    # Add any provided fields to the update
    for key, value in kwargs.items():
        if key == "character_class":  # Handle the class field specially
            updated_fields["class"] = value
        elif key == "ability_scores" and isinstance(value, dict):
            # Handle nested updates for ability scores
            for ability, score in value.items():
                updated_fields[f"data.ability_scores.{ability}"] = score
        elif key == "campaign_progress" and isinstance(value, dict):
            # Handle nested updates for campaign progress
            for progress_key, progress_value in value.items():
                updated_fields[f"data.campaign_progress.{progress_key}"] = progress_value
        else:
            updated_fields[key] = value
    
    characters_collection.update_one({"int_id": character_id}, {"$set": updated_fields})
    
    # Get the updated character
    updated_character = characters_collection.find_one({"int_id": character_id})
    
    # For the Pydantic model
    character_dict = {
        "id": updated_character["int_id"],
        "campaign_id": updated_character["campaign_id"],
        "name": updated_character["name"],
        "player_name": updated_character.get("player_name"),
        "race": updated_character.get("race"),
        "class": updated_character.get("class"),
        "level": updated_character.get("level", 1),
        "data": updated_character.get("data", {}),
        "created_at": updated_character["created_at"],
        "updated_at": updated_character["updated_at"]
    }
    return Character(**character_dict)

def delete_character(character_id: int) -> bool:
    result = characters_collection.delete_one({"int_id": character_id})
    if result.deleted_count > 0:
        return True
    return False

def get_character(character_id: int):
    character = characters_collection.find_one({"int_id": character_id})
    if not character:
        raise ValueError(f"Character with ID {character_id} does not exist.")
    
    character_dict = {
        "id": character["int_id"],
        "campaign_id": character["campaign_id"],
        "name": character["name"],
        "player_name": character.get("player_name"),
        "race": character.get("race"),
        "class": character.get("class"),
        "level": character.get("level", 1),
        "data": character.get("data", {}),
        "created_at": character["created_at"],
        "updated_at": character["updated_at"]
    }
    return Character(**character_dict)

def get_character_by_name(name: str):
    query = {"name": name}
    character = characters_collection.find_one(query)
    
    if not character:
        raise ValueError(f"Character with name '{name}' does not exist.")
    
    character_dict = {
        "id": character["int_id"],
        "campaign_id": character["campaign_id"],
        "name": character["name"],
        "player_name": character.get("player_name"),
        "race": character.get("race"),
        "class": character.get("class"),
        "level": character.get("level", 1),
        "data": character.get("data", {}),
        "created_at": character["created_at"],
        "updated_at": character["updated_at"]
    }
    return Character(**character_dict)

def list_characters() -> List[Character]:
    characters = characters_collection.find()
    character_list = []
    for character in characters:
        character_dict = {
            "id": character["int_id"],
            "campaign_id": character["campaign_id"],
            "name": character["name"],
            "player_name": character.get("player_name"),
            "race": character.get("race"),
            "class": character.get("class"),
            "level": character.get("level", 1),
            "data": character.get("data", {}),
            "created_at": character["created_at"],
            "updated_at": character["updated_at"]
        }
        character_list.append(Character(**character_dict))
    return character_list

def list_campaign_characters(campaign_id: int) -> List[Character]:
    characters = characters_collection.find({"campaign_id": campaign_id})
    character_list = []
    for character in characters:
        character_dict = {
            "id": character["int_id"],
            "campaign_id": character["campaign_id"],
            "name": character["name"],
            "player_name": character.get("player_name"),
            "race": character.get("race"),
            "class": character.get("class"),
            "level": character.get("level", 1),
            "data": character.get("data", {}),
            "created_at": character["created_at"],
            "updated_at": character["updated_at"]
        }
        character_list.append(Character(**character_dict))
    return character_list

def search_characters(query: str = None, campaign_id: Optional[int] = None, 
                     character_class: Optional[str] = None, race: Optional[str] = None) -> List[Character]:
    # Build the search query
    search_query = {}
    
    if query:
        search_query["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"player_name": {"$regex": query, "$options": "i"}}
        ]
    
    if campaign_id is not None:
        search_query["campaign_id"] = campaign_id
        
    if character_class:
        search_query["class"] = {"$regex": character_class, "$options": "i"}
        
    if race:
        search_query["race"] = {"$regex": race, "$options": "i"}
    
    characters = characters_collection.find(search_query)
    character_list = []
    for character in characters:
        character_dict = {
            "id": character["int_id"],
            "campaign_id": character["campaign_id"],
            "name": character["name"],
            "player_name": character.get("player_name"),
            "race": character.get("race"),
            "class": character.get("class"),
            "level": character.get("level", 1),
            "data": character.get("data", {}),
            "created_at": character["created_at"],
            "updated_at": character["updated_at"]
        }
        character_list.append(Character(**character_dict))
    return character_list

def update_character_progress(character_id: int, current_location: Optional[str] = None, 
                             key_discoveries: Optional[List[str]] = None):
    # Get the current character
    character = get_character(character_id)
    
    # Prepare the campaign progress data
    campaign_progress = {}
    if current_location:
        campaign_progress["current_location"] = current_location
    if key_discoveries:
        campaign_progress["key_discoveries"] = key_discoveries
    
    # Update the character with the campaign progress
    return update_character(character_id, campaign_progress=campaign_progress) 