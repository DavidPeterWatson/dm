from datetime import datetime, timezone
from typing import List, Optional
from models.character import Character
from bson.objectid import ObjectId
from .db_operations import objectid_to_str
from .campaign_operations import get_campaign
from .db_operations import Database

def create_character(db: Database, character: Character):

    # Verify campaign exists
    try:
        get_campaign(db, character.campaign_id)
    except ValueError:
        raise ValueError(f"Campaign with ID {character.campaign_id} does not exist.")
    
    # Check if a character with this name already exists
    existing_character = db.characters_collection.find_one({"name": character.name})
    if existing_character:
        raise ValueError(f"Character with name '{character.name}' already exists.")
    
    now = datetime.now(timezone.utc)
    # Create a new ObjectId first
    oid = ObjectId()
    str_id = objectid_to_str(oid)
    
    # Convert character to dict and prepare for MongoDB
    character_dict = character.model_dump()
    
    # Set ID and timestamps
    character_dict["_id"] = oid
    character_dict["id"] = str_id
    character_dict["created_at"] = now.isoformat()
    character_dict["updated_at"] = now.isoformat()
    
    # Handle class field specially
    if "character_class" in character_dict:
        character_dict["class"] = character_dict.pop("character_class")
    
    # Insert into database
    db.characters_collection.insert_one(character_dict)
    
    return _convert_db_character_to_model(character_dict)

    # character.id = character_dict["id"]
    # character.created_at = character_dict["created_at"]
    # character.updated_at = character_dict["updated_at"] 
    # return character

    # # Return updated character
    # return Character(
    #     id=str_id,
    #     campaign_id=character.campaign_id,
    #     name=character.name,
    #     player_name=character.player_name,
    #     race=character.race,
    #     character_class=character_dict.get("class"),
    #     level=character.level,
    #     subclass=character.subclass,
    #     background=character.background,
    #     ability_scores=character.ability_scores,
    #     modifiers=character.modifiers,
    #     proficiencies=character.proficiencies,
    #     personality=character.personality,
    #     backstory=character.backstory,
    #     equipment=character.equipment,
    #     spells=character.spells,
    #     familiar=character.familiar,
    #     motivations=character.motivations,
    #     data=character.data,
    #     created_at=now.isoformat(),
    #     updated_at=now.isoformat()
    # )

def update_character(db: Database, character_id: str, **kwargs):
    # Find by string ID
    character = db.characters_collection.find_one({"id": character_id})
    if not character:
        raise ValueError(f"Character with ID {character_id} does not exist.")
    
    now = datetime.now(timezone.utc)
    
    # Prepare update fields
    updated_fields = {"updated_at": now.isoformat()}
    
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
    
    db.characters_collection.update_one({"id": character_id}, {"$set": updated_fields})
    
    updated_character = db.characters_collection.find_one({"id": character_id})
    return _convert_db_character_to_model(updated_character)

def delete_character(db: Database, character_id: str) -> bool:
    result = db.characters_collection.delete_one({"id": character_id})
    if result.deleted_count > 0:
        return True
    return False

def _convert_db_character_to_model(character: dict) -> Character:
    character_dict = {
        "id": character["id"],
        "campaign_id": character["campaign_id"],
        "name": character["name"],
        "player_name": character.get("player_name"),
        "race": character.get("race"),
        "character_class": character.get("class"),
        "subclass": character.get("subclass"),
        "background": character.get("background"),
        "level": character.get("level", 1),
        "ability_scores": character.get("ability_scores"),
        "modifiers": character.get("modifiers"),
        "proficiencies": character.get("proficiencies"),
        "personality": character.get("personality"),
        "backstory": character.get("backstory"),
        "equipment": character.get("equipment"),
        "spells": character.get("spells"),
        "familiar": character.get("familiar"),
        "motivations": character.get("motivations"),
        "data": character.get("data", {}),
        "created_at": character["created_at"],
        "updated_at": character["updated_at"]
    }
    return Character(**character_dict)

def get_character(db: Database, character_id: str):
    character = db.characters_collection.find_one({"id": character_id})
    if not character:
        raise ValueError(f"Character with ID {character_id} does not exist.")
    
    return _convert_db_character_to_model(character)

def get_character_by_name(db: Database, name: str):
    query = {"name": name}
    character = db.characters_collection.find_one(query)
    
    if not character:
        raise ValueError(f"Character with name '{name}' does not exist.")
    
    return _convert_db_character_to_model(character)

def list_characters(db: Database) -> List[Character]:
    characters = db.characters_collection.find()
    return [_convert_db_character_to_model(character) for character in characters]

def list_campaign_characters(db: Database, campaign_id: str) -> List[Character]:
    characters = db.characters_collection.find({"campaign_id": campaign_id})
    return [_convert_db_character_to_model(character) for character in characters]

def search_characters(db: Database, query: str = None, campaign_id: Optional[str] = None, 
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
    
    characters = db.characters_collection.find(search_query)
    return [_convert_db_character_to_model(character) for character in characters]

def update_character_progress(db: Database, character_id: str, current_location: Optional[str] = None, 
                             key_discoveries: Optional[List[str]] = None):
    # Get the current character
    character = get_character(db, character_id)
    
    # Prepare the campaign progress data
    campaign_progress = {}
    if current_location:
        campaign_progress["current_location"] = current_location
    if key_discoveries:
        campaign_progress["key_discoveries"] = key_discoveries
    
    # Update the character with the campaign progress
    return update_character(db, character_id, campaign_progress=campaign_progress) 