from mcp.server.fastmcp import FastMCP
from database.db_operations import Database, init_db
import argparse
from typing import Annotated, Dict, List

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
    search_characters,
    delete_all_characters
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
from pydantic import Field

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
def create_campaign_tool(
    name: Annotated[str, Field(description="The name of the campaign to create")],
    description: Annotated[str, Field(description="A detailed description of the campaign setting and storyline")]
) -> Campaign:
    """
    Create a new campaign.
    """
    validate_campaign_data(name, description)
    return create_campaign(db, name, description)

@mcp.tool()
def update_campaign_tool(
    campaign_id: Annotated[int, Field(description="The ID of the campaign to update")],
    name: Annotated[str, Field(description="The new name for the campaign")],
    description: Annotated[str, Field(description="The new description for the campaign")]
) -> Campaign:
    """
    Update an existing campaign.
    """
    validate_campaign_data(name, description)
    return update_campaign(db, campaign_id, name, description)

@mcp.tool()
def delete_campaign_tool(
    campaign_id: Annotated[int, Field(description="The ID of the campaign to delete")]
) -> bool:
    """
    Delete a campaign.
    
    Warning: This will permanently delete the campaign and all associated data.
    """
    return delete_campaign(db, campaign_id)

@mcp.tool()
def search_campaigns_tool(
    query: Annotated[str, Field(description="Search term to look for in campaign names and descriptions")]
) -> list[Campaign]:
    """
    Search campaigns by name or description.
    """
    return search_campaigns(db, query)

@mcp.tool()
def delete_all_campaigns_tool() -> int:
    """
    Delete all campaigns from the database.
    
    Warning: This will permanently delete ALL campaigns and associated data.
    """
    return delete_all_campaigns(db)

@mcp.tool()
def delete_all_characters_tool() -> int:
    """
    Delete all characters from the database.
    
    Warning: This will permanently delete ALL characters and their data.
    """
    return delete_all_characters(db)

# Character Management Tools

@mcp.tool()
def create_character_tool(
    name: Annotated[str, Field(description="The character's name")],
    campaign_id: Annotated[str, Field(description="The ID of the campaign this character belongs to")],
    player_name: Annotated[str | None, Field(description="The player's real name")] = None,
    race: Annotated[str | None, Field(description="The character's race (e.g., Human, Elf, Dwarf)")] = None,
    character_class: Annotated[str | None, Field(description="The character's class (e.g., Fighter, Wizard, Cleric)")] = None,
    level: Annotated[int, Field(description="The character's level")] = 1,
    subclass: Annotated[str | None, Field(description="The character's subclass specialization")] = None,
    background: Annotated[str | None, Field(description="The character's background (e.g., Noble, Soldier)")] = None,
    backstory: Annotated[str | None, Field(description="The character's detailed backstory narrative")] = None,
    ability_scores: Annotated[Dict | None, Field(description="The character's ability scores (STR, DEX, CON, INT, WIS, CHA)")] = None,
    modifiers: Annotated[Dict | None, Field(description="Various modifiers affecting the character")] = None,
    proficiencies: Annotated[Dict | None, Field(description="Skills, tools, and other proficiencies")] = None,
    personality: Annotated[Dict | None, Field(description="Personality traits, ideals, bonds, and flaws")] = None,
    equipment: Annotated[List[str] | None, Field(description="List of items and equipment carried")] = None,
    spells: Annotated[Dict | None, Field(description="Spells known and spell slots available")] = None,
    familiar: Annotated[Dict | None, Field(description="Details about any familiar or companion")] = None,
    motivations: Annotated[List[str] | None, Field(description="Character's goals and motivations")] = None,
    data: Annotated[Dict | None, Field(description="Additional custom data for the character")] = None
) -> Character:
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
def update_character_tool(
    character_id: Annotated[int, Field(description="The ID of the character to update")],
    name: Annotated[str | None, Field(description="The character's new name")] = None,
    campaign_id: Annotated[str | None, Field(description="The ID of the campaign this character belongs to")] = None,
    player_name: Annotated[str | None, Field(description="The player's real name")] = None,
    race: Annotated[str | None, Field(description="The character's race (e.g., Human, Elf, Dwarf)")] = None,
    character_class: Annotated[str | None, Field(description="The character's class (e.g., Fighter, Wizard, Cleric)")] = None,
    level: Annotated[int | None, Field(description="The character's level")] = None,
    subclass: Annotated[str | None, Field(description="The character's subclass specialization")] = None,
    background: Annotated[str | None, Field(description="The character's background (e.g., Noble, Soldier)")] = None,
    backstory: Annotated[str | None, Field(description="The character's detailed backstory narrative")] = None,
    ability_scores: Annotated[Dict | None, Field(description="The character's ability scores (STR, DEX, CON, INT, WIS, CHA)")] = None,
    modifiers: Annotated[Dict | None, Field(description="Various modifiers affecting the character")] = None,
    proficiencies: Annotated[Dict | None, Field(description="Skills, tools, and other proficiencies")] = None,
    personality: Annotated[Dict | None, Field(description="Personality traits, ideals, bonds, and flaws")] = None,
    equipment: Annotated[List[str] | None, Field(description="List of items and equipment carried")] = None,
    spells: Annotated[Dict | None, Field(description="Spells known and spell slots available")] = None,
    familiar: Annotated[Dict | None, Field(description="Details about any familiar or companion")] = None,
    motivations: Annotated[List[str] | None, Field(description="Character's goals and motivations")] = None,
    data: Annotated[Dict | None, Field(description="Additional custom data for the character")] = None
) -> Character:
    """
    Update an existing character.
    
    All parameters except character_id are optional. Only the provided parameters will be updated.
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
def search_characters_tool(
    query: Annotated[str | None, Field(description="Search term to look for in character names and details")] = None,
    campaign_id: Annotated[int | None, Field(description="Filter characters by campaign ID")] = None,
    character_class: Annotated[str | None, Field(description="Filter characters by character class")] = None,
    race: Annotated[str | None, Field(description="Filter characters by race")] = None
) -> list[Character]:
    """
    Search characters by name, race, class, etc.
    
    All search parameters are optional. If multiple parameters are provided, they are combined (AND logic).
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
def create_setting_tool(
    setting_type: Annotated[str, Field(description="The type of setting (e.g., City, Town, Dungeon, Forest)")],
    name: Annotated[str, Field(description="The name of the setting")],
    region: Annotated[str, Field(description="The region where this setting is located")],
    scale: Annotated[str, Field(description="The scale of the setting (e.g., Small, Medium, Large)")],
    population: Annotated[str, Field(description="The population size of the setting")],
    first_impression: Annotated[str | None, Field(description="The first impression visitors get of this setting")] = None,
    distinctive_features: Annotated[List[str] | None, Field(description="List of distinctive features of this setting")] = None,
    atmosphere: Annotated[str | None, Field(description="The general atmosphere or mood of the setting")] = None,
    key_locations: Annotated[List[str] | None, Field(description="List of key locations within this setting")] = None,
    points_of_interest: Annotated[List[str] | None, Field(description="List of interesting points or landmarks")] = None,
    travel_routes: Annotated[List[str] | None, Field(description="Major travel routes to and from this setting")] = None,
    factions: Annotated[List[str] | None, Field(description="Major factions or groups present in this setting")] = None,
    power_structure: Annotated[str | None, Field(description="The power structure and leadership of this setting")] = None,
    local_customs: Annotated[str | None, Field(description="Local customs, traditions, and cultural notes")] = None,
    economic_basis: Annotated[str | None, Field(description="The economic foundation of this setting")] = None,
    origin: Annotated[str | None, Field(description="The origin story or founding of this setting")] = None,
    recent_history: Annotated[str | None, Field(description="Recent historical events affecting this setting")] = None,
    hidden_past: Annotated[str | None, Field(description="Secret or hidden history of this setting")] = None,
    integration_notes: Annotated[str | None, Field(description="Notes on how to integrate this setting into a campaign")] = None,
    encounter_recommendations: Annotated[List[str] | None, Field(description="Recommended encounters for this setting")] = None,
    dramatic_element_opportunities: Annotated[List[str] | None, Field(description="Potential dramatic scenarios for this setting")] = None,
    parent_id: Annotated[str | None, Field(description="ID of the parent setting if this is a sub-location")] = None
) -> Setting:
    """
    Create a new setting with detailed information.
    
    Required fields are setting_type, name, region, scale, and population.
    All other fields are optional and provide additional detail to the setting.
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
def update_setting_tool(
    setting_id: Annotated[str, Field(description="The ID of the setting to update")],
    setting_type: Annotated[str | None, Field(description="The type of setting (e.g., City, Town, Dungeon, Forest)")] = None,
    name: Annotated[str | None, Field(description="The name of the setting")] = None,
    region: Annotated[str | None, Field(description="The region where this setting is located")] = None,
    scale: Annotated[str | None, Field(description="The scale of the setting (e.g., Small, Medium, Large)")] = None,
    population: Annotated[str | None, Field(description="The population size of the setting")] = None,
    first_impression: Annotated[str | None, Field(description="The first impression visitors get of this setting")] = None,
    distinctive_features: Annotated[List[str] | None, Field(description="List of distinctive features of this setting")] = None,
    atmosphere: Annotated[str | None, Field(description="The general atmosphere or mood of the setting")] = None,
    key_locations: Annotated[List[str] | None, Field(description="List of key locations within this setting")] = None,
    points_of_interest: Annotated[List[str] | None, Field(description="List of interesting points or landmarks")] = None,
    travel_routes: Annotated[List[str] | None, Field(description="Major travel routes to and from this setting")] = None,
    factions: Annotated[List[str] | None, Field(description="Major factions or groups present in this setting")] = None,
    power_structure: Annotated[str | None, Field(description="The power structure and leadership of this setting")] = None,
    local_customs: Annotated[str | None, Field(description="Local customs, traditions, and cultural notes")] = None,
    economic_basis: Annotated[str | None, Field(description="The economic foundation of this setting")] = None,
    origin: Annotated[str | None, Field(description="The origin story or founding of this setting")] = None,
    recent_history: Annotated[str | None, Field(description="Recent historical events affecting this setting")] = None,
    hidden_past: Annotated[str | None, Field(description="Secret or hidden history of this setting")] = None,
    integration_notes: Annotated[str | None, Field(description="Notes on how to integrate this setting into a campaign")] = None,
    encounter_recommendations: Annotated[List[str] | None, Field(description="Recommended encounters for this setting")] = None,
    dramatic_element_opportunities: Annotated[List[str] | None, Field(description="Potential dramatic scenarios for this setting")] = None,
    parent_id: Annotated[str | None, Field(description="ID of the parent setting if this is a sub-location")] = None,
    **kwargs
) -> dict:
    """
    Update an existing setting.
    Only the setting_id is required. Only the provided parameters will be updated.
    Returns a dict with the updated Setting and a warning message if unknown fields were provided.
    """
    from models.setting import Setting
    # Collect all update data, including any extra fields from kwargs (for JSON updates)
    update_data = {k: v for k, v in locals().items() if k not in ['setting_id', 'db', 'kwargs'] and v is not None}
    update_data.update(kwargs)
    valid_fields = set(Setting.__fields__.keys()) - {'id', 'created_at', 'updated_at'}
    # Remove non-user-supplied keys from unknown_fields
    non_user_keys = {'Setting'}
    unknown_fields = [k for k in update_data if k not in valid_fields and k not in non_user_keys]
    filtered_update_data = {k: v for k, v in update_data.items() if k in valid_fields}
    warning = None
    if unknown_fields:
        warning = f"Warning: Unknown fields ignored: {', '.join(unknown_fields)}"
    updated_setting = update_setting(db, setting_id, **filtered_update_data)
    return {"setting": updated_setting, "warning": warning}

@mcp.tool()
def delete_setting_tool(
    setting_id: Annotated[str, Field(description="The ID of the setting to delete")]
) -> bool:
    """
    Delete a setting.
    
    Warning: This will permanently delete the setting and all its data.
    """
    return delete_setting(db, setting_id)

@mcp.tool()
def search_settings_tool(
    query: Annotated[str, Field(description="Search term to look for in setting names, regions, or descriptions")]
) -> Dict:
    """
    Search settings by name, region, or description.
    
    Returns a dictionary containing the matching settings, a message, and a count.
    """
    settings = search_settings(db, query)
    result = {
        "settings": settings,
        "message": f"No settings found matching '{query}'." if not settings else f"Found {len(settings)} setting(s) matching '{query}'.",
        "count": len(settings)
    }
    return result

@mcp.tool()
def filter_settings_by_type_tool(
    setting_type: Annotated[str, Field(description="The type of setting to filter by (e.g., City, Town, Forest)")]
) -> Dict:
    """
    Filter settings by their type (e.g., City, Town, Forest).
    
    Returns a dictionary containing the matching settings, a message, and a count.
    """
    settings = filter_settings_by_type(db, setting_type)
    result = {
        "settings": settings,
        "message": f"No settings found with type '{setting_type}'." if not settings else f"Found {len(settings)} setting(s) with type '{setting_type}'.",
        "count": len(settings)
    }
    return result

@mcp.tool()
def filter_settings_by_parent_tool(
    parent_id: Annotated[str, Field(description="The ID of the parent setting to filter by")]
) -> Dict:
    """
    Filter settings by their parent setting ID.
    
    Returns a dictionary containing child settings of the specified parent, a message, and a count.
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
def get_setting_by_name_tool(
    name: Annotated[str, Field(description="The name of the setting to retrieve")]
) -> Setting:
    """
    Get a setting by its name.
    
    The name must match exactly (case-sensitive).
    """
    setting = get_setting_by_name(db, name)
    if not setting:
        raise ValueError(f"Setting with name '{name}' not found")
    return setting

@mcp.tool()
def delete_all_settings_tool() -> bool:
    """
    Delete all settings from the database.
    
    Warning: This will permanently delete ALL settings and their data.
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