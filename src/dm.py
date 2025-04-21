from mcp.server.fastmcp import FastMCP
from database.db_operations import Database, init_db
import os
import argparse
import sys

from database.campaign_operations import (
    create_campaign,
    update_campaign,
    delete_campaign,
    search_campaigns,
    get_campaign,
    list_campaigns,
    delete_all_campaigns
)
from database.character_operations import (
    create_character,
    update_character,
    delete_character,
    get_character,
    list_characters,
    list_campaign_characters,
    search_characters
)
from database.setting_operations import (
    create_setting,
    update_setting,
    delete_setting,
    search_settings,
    get_setting,
    list_settings,
    filter_settings_by_type,
    get_setting_by_name,
    delete_all_settings
)
from models.campaign import Campaign
from models.character import Character
from models.setting import Setting
from utils.helpers import validate_campaign_data, validate_character_data, validate_setting_data
from typing import List, Optional, Dict

# Initialize database connection
db = Database()

# Setup MCP
mcp = FastMCP("D&D Game Master Assistant", dependencies=["pydantic", "sqlite-utils", "rich"])

# Flag to track whether database is initialized
is_db_initialized = False

def initialize_db(db_name: str):
    """Initialize the database with the given name"""
    global is_db_initialized
    if is_db_initialized:
        raise RuntimeError(f"Database '{db_name}' has already been initialized")
    
    init_db(db, db_name=db_name)
    print(f"Database '{db_name}' initialized")
    is_db_initialized = True

# Campaign Management Tools

@mcp.tool()
def create_campaign_tool(name: str, description: str) -> Campaign:
    """
    Create a new campaign.
    """
    validate_campaign_data(name, description)
    return create_campaign(db, name, description)

@mcp.tool()
def update_campaign_tool(campaign_id: int, name: str, description: str) -> Campaign:
    """
    Update an existing campaign.
    """
    validate_campaign_data(name, description)
    return update_campaign(db, campaign_id, name, description)

@mcp.tool()
def delete_campaign_tool(campaign_id: int) -> bool:
    """
    Delete a campaign.
    """
    return delete_campaign(db, campaign_id)

@mcp.tool()
def search_campaigns_tool(query: str) -> list[Campaign]:
    """
    Search campaigns by name or description.
    """
    return search_campaigns(db, query)

@mcp.tool()
def delete_all_campaigns_tool() -> int:
    """
    Delete all campaigns from the database.
    """
    return delete_all_campaigns(db)

# Character Management Tools

@mcp.tool()
def create_character_tool(name: str, campaign_id: str, player_name: Optional[str] = None,
                         race: Optional[str] = None, character_class: Optional[str] = None,
                         level: int = 1, subclass: Optional[str] = None, 
                         background: Optional[str] = None, backstory: Optional[str] = None,
                         ability_scores: Optional[Dict] = None, modifiers: Optional[Dict] = None,
                         proficiencies: Optional[Dict] = None, personality: Optional[Dict] = None,
                         equipment: Optional[List[str]] = None, spells: Optional[Dict] = None,
                         familiar: Optional[Dict] = None, motivations: Optional[List[str]] = None,
                         data: Optional[Dict] = None) -> Character:
    """
    Create a new character with all available character attributes.
    """
    validate_character_data(name, campaign_id)
    
    character = Character(
        id="temp",  # Will be replaced by the database operation
        campaign_id=campaign_id,
        name=name,
        player_name=player_name,
        race=race,
        character_class=character_class,
        level=level,
        subclass=subclass,
        background=background,
        backstory=backstory,
        ability_scores=ability_scores,
        modifiers=modifiers,
        proficiencies=proficiencies,
        personality=personality,
        equipment=equipment,
        spells=spells,
        familiar=familiar,
        motivations=motivations,
        data=data or {},
        created_at="",  # Will be set by the database operation
        updated_at=""   # Will be set by the database operation
    )
    
    return create_character(db, character)

@mcp.tool()
def update_character_tool(character_id: int, name: Optional[str] = None, campaign_id: Optional[str] = None,
                         player_name: Optional[str] = None, race: Optional[str] = None, 
                         character_class: Optional[str] = None, level: Optional[int] = None, 
                         subclass: Optional[str] = None, background: Optional[str] = None, 
                         backstory: Optional[str] = None, ability_scores: Optional[Dict] = None, 
                         modifiers: Optional[Dict] = None, proficiencies: Optional[Dict] = None, 
                         personality: Optional[Dict] = None, equipment: Optional[List[str]] = None, 
                         spells: Optional[Dict] = None, familiar: Optional[Dict] = None, 
                         motivations: Optional[List[str]] = None, data: Optional[Dict] = None) -> Character:
    """
    Update an existing character.
    """
    update_data = {k: v for k, v in locals().items() 
                  if k not in ['character_id', 'db'] and v is not None}
    return update_character(db, character_id, **update_data)

@mcp.tool()
def delete_character_tool(character_id: int) -> bool:
    """
    Delete a character.
    """
    return delete_character(db, character_id)

@mcp.tool()
def search_characters_tool(query: Optional[str] = None, campaign_id: Optional[int] = None,
                          character_class: Optional[str] = None, race: Optional[str] = None) -> list[Character]:
    """
    Search characters by name, race, class, etc.
    """
    return search_characters(
        db,
        query=query,
        campaign_id=campaign_id,
        character_class=character_class,
        race=race
    )

# Setting Management Tools

@mcp.tool()
def create_setting_tool(setting_type: str, name: str, region: str, scale: str, population: str,
                       first_impression: Optional[str] = None, distinctive_features: Optional[List[str]] = None,
                       atmosphere: Optional[str] = None, key_locations: Optional[List[str]] = None,
                       points_of_interest: Optional[List[str]] = None, travel_routes: Optional[List[str]] = None,
                       factions: Optional[List[str]] = None, power_structure: Optional[str] = None,
                       local_customs: Optional[str] = None, economic_basis: Optional[str] = None,
                       origin: Optional[str] = None, recent_history: Optional[str] = None,
                       hidden_past: Optional[str] = None, integration_notes: Optional[str] = None,
                       encounter_recommendations: Optional[List[str]] = None,
                       dramatic_element_opportunities: Optional[List[str]] = None,
                       parent_id: Optional[str] = None) -> Setting:
    """
    Create a new setting with detailed information.
    """
    validate_setting_data(name, setting_type)
    
    setting_data = {
        "setting_type": setting_type,
        "name": name,
        "region": region,
        "scale": scale,
        "population": population,
        "first_impression": first_impression,
        "distinctive_features": distinctive_features,
        "atmosphere": atmosphere,
        "key_locations": key_locations,
        "points_of_interest": points_of_interest,
        "travel_routes": travel_routes,
        "factions": factions,
        "power_structure": power_structure,
        "local_customs": local_customs,
        "economic_basis": economic_basis,
        "origin": origin,
        "recent_history": recent_history,
        "hidden_past": hidden_past,
        "integration_notes": integration_notes,
        "encounter_recommendations": encounter_recommendations,
        "dramatic_element_opportunities": dramatic_element_opportunities,
        "parent_id": parent_id
    }
    
    # Remove None values
    setting_data = {k: v for k, v in setting_data.items() if v is not None}
    
    return create_setting(db, **setting_data)

@mcp.tool()
def update_setting_tool(setting_id: str, setting_type: Optional[str] = None, name: Optional[str] = None, 
                       region: Optional[str] = None, scale: Optional[str] = None, 
                       population: Optional[str] = None, first_impression: Optional[str] = None, 
                       distinctive_features: Optional[List[str]] = None, atmosphere: Optional[str] = None, 
                       key_locations: Optional[List[str]] = None, points_of_interest: Optional[List[str]] = None, 
                       travel_routes: Optional[List[str]] = None, factions: Optional[List[str]] = None, 
                       power_structure: Optional[str] = None, local_customs: Optional[str] = None, 
                       economic_basis: Optional[str] = None, origin: Optional[str] = None, 
                       recent_history: Optional[str] = None, hidden_past: Optional[str] = None, 
                       integration_notes: Optional[str] = None, encounter_recommendations: Optional[List[str]] = None,
                       dramatic_element_opportunities: Optional[List[str]] = None,
                       parent_id: Optional[str] = None) -> Setting:
    """
    Update an existing setting.
    """
    update_data = {k: v for k, v in locals().items() 
                  if k not in ['setting_id', 'db'] and v is not None}
    return update_setting(db, setting_id, **update_data)

@mcp.tool()
def delete_setting_tool(setting_id: str) -> bool:
    """
    Delete a setting.
    """
    return delete_setting(db, setting_id)

@mcp.tool()
def search_settings_tool(query: str) -> Dict:
    """
    Search settings by name, region, or description.
    """
    settings = search_settings(db, query)
    result = {
        "settings": settings,
        "message": f"No settings found matching '{query}'." if not settings else f"Found {len(settings)} setting(s) matching '{query}'.",
        "count": len(settings)
    }
    return result

@mcp.tool()
def filter_settings_by_type_tool(setting_type: str) -> Dict:
    """
    Filter settings by their type (e.g., City, Town, Forest).
    """
    settings = filter_settings_by_type(db, setting_type)
    result = {
        "settings": settings,
        "message": f"No settings found with type '{setting_type}'." if not settings else f"Found {len(settings)} setting(s) with type '{setting_type}'.",
        "count": len(settings)
    }
    return result

@mcp.tool()
def filter_settings_by_parent_tool(parent_id: str) -> Dict:
    """
    Filter settings by their parent setting ID.
    """
    # Get all settings and filter by parent_id
    all_settings = list_settings(db)
    settings = [s for s in all_settings if s.parent_id == parent_id]
    
    result = {
        "settings": settings,
        "message": f"No child settings found for parent ID '{parent_id}'." if not settings else f"Found {len(settings)} child setting(s) for parent ID '{parent_id}'.",
        "count": len(settings)
    }
    return result

@mcp.tool()
def get_setting_by_name_tool(name: str) -> Setting:
    """
    Get a setting by its name.
    """
    setting = get_setting_by_name(db, name)
    if not setting:
        raise ValueError(f"Setting with name '{name}' not found")
    return setting

@mcp.tool()
def delete_all_settings_tool() -> bool:
    """
    Delete all settings from the database.
    """
    return delete_all_settings(db)

# Campaign Resources

@mcp.resource("campaign://{campaign_id}")
def get_campaign_resource(campaign_id: int) -> Campaign:
    """
    Get campaign details.
    """
    return get_campaign(db, campaign_id)

@mcp.resource("campaign://list")
def list_campaigns_resource() -> list[Campaign]:
    """
    List all campaigns.
    """
    return list_campaigns(db)

# Character Resources

@mcp.resource("character://{character_id}")
def get_character_resource(character_id: int) -> Character:
    """
    Get character details.
    """
    return get_character(db, character_id)

@mcp.resource("character://list")
def list_characters_resource() -> list[Character]:
    """
    List all characters.
    """
    return list_characters(db)

@mcp.resource("character://campaign/{campaign_id}/list")
def list_campaign_characters_resource(campaign_id: int) -> list[Character]:
    """
    List all characters in a campaign.
    """
    return list_campaign_characters(db, campaign_id)

# Setting Resources

@mcp.resource("setting://{setting_id}")
def get_setting_resource(setting_id: str) -> Setting:
    """
    Get setting details.
    """
    return get_setting(db, setting_id)

@mcp.resource("setting://list")
def list_settings_resource() -> Dict:
    """
    List all settings.
    """
    settings = list_settings(db)
    result = {
        "settings": settings,
        "message": "No settings found. Use the create_setting_tool to add new settings." if not settings else "",
        "count": len(settings)
    }
    return result

@mcp.resource("setting://name/{name}")
def get_setting_by_name_resource(name: str) -> Setting:
    """
    Get setting details by name.
    """
    return get_setting_by_name(db, name)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="D&D Game Master Assistant")
    parser.add_argument("--db-name", required=True, help="Database name (required)")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()
    db_name = args.db_name
    
    # Initialize the database
    initialize_db(db_name)
    
    # Run the MCP application
    mcp.run()