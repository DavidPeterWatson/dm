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
    name: str,
    description: str
) -> Campaign:
    """
    Create a new campaign.

    Args:
        name: The name of the campaign to create
        description: A detailed description of the campaign setting and storyline
    """
    validate_campaign_data(name, description)
    return create_campaign(db, name, description)

@mcp.tool()
def update_campaign_tool(
    campaign_id: int,
    name: str,
    description: str
) -> Campaign:
    """
    Update an existing campaign.

    Args:
        campaign_id: The ID of the campaign to update
        name: The new name for the campaign
        description: The new description for the campaign
    """
    validate_campaign_data(name, description)
    return update_campaign(db, campaign_id, name, description)

@mcp.tool()
def delete_campaign_tool(
    campaign_id: int
) -> bool:
    """
    Delete a campaign.

    Args:
        campaign_id: The ID of the campaign to delete

    Warning: This will permanently delete the campaign and all associated data.
    """
    return delete_campaign(db, campaign_id)

@mcp.tool()
def search_campaigns_tool(
    query: str
) -> list[Campaign]:
    """
    Search campaigns by name or description.

    Args:
        query: Search term to look for in campaign names and descriptions
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
    name: str,
    campaign_id: str,
    player_name: str | None = None,
    race: str | None = None,
    character_class: str | None = None,
    level: int = 1,
    subclass: str | None = None,
    background: str | None = None,
    backstory: str | None = None,
    ability_scores: Dict | None = None,
    modifiers: Dict | None = None,
    proficiencies: Dict | None = None,
    personality: Dict | None = None,
    equipment: List[str] | None = None,
    spells: Dict | None = None,
    familiar: Dict | None = None,
    motivations: List[str] | None = None,
    data: Dict | None = None
) -> Character:
    """
    Create a new character with all available character attributes.

    Args:
        name: The character's name
        campaign_id: The ID of the campaign this character belongs to
        player_name: The player's real name
        race: The character's race (e.g., Human, Elf, Dwarf)
        character_class: The character's class (e.g., Fighter, Wizard, Cleric)
        level: The character's level
        subclass: The character's subclass specialization
        background: The character's background (e.g., Noble, Soldier)
        backstory: The character's detailed backstory narrative
        ability_scores: The character's ability scores (STR, DEX, CON, INT, WIS, CHA)
        modifiers: Various modifiers affecting the character
        proficiencies: Skills, tools, and other proficiencies
        personality: Personality traits, ideals, bonds, and flaws
        equipment: List of items and equipment carried
        spells: Spells known and spell slots available
        familiar: Details about any familiar or companion
        motivations: Character's goals and motivations
        data: Additional custom data for the character
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
    character_id: int,
    name: str | None = None,
    campaign_id: str | None = None,
    player_name: str | None = None,
    race: str | None = None,
    character_class: str | None = None,
    level: int | None = None,
    subclass: str | None = None,
    background: str | None = None,
    backstory: str | None = None,
    ability_scores: Dict | None = None,
    modifiers: Dict | None = None,
    proficiencies: Dict | None = None,
    personality: Dict | None = None,
    equipment: List[str] | None = None,
    spells: Dict | None = None,
    familiar: Dict | None = None,
    motivations: List[str] | None = None,
    data: Dict | None = None
) -> Character:
    """
    Update an existing character.

    Args:
        character_id: The ID of the character to update
        name: The character's new name
        campaign_id: The ID of the campaign this character belongs to
        player_name: The player's real name
        race: The character's race (e.g., Human, Elf, Dwarf)
        character_class: The character's class (e.g., Fighter, Wizard, Cleric)
        level: The character's level
        subclass: The character's subclass specialization
        background: The character's background (e.g., Noble, Soldier)
        backstory: The character's detailed backstory narrative
        ability_scores: The character's ability scores (STR, DEX, CON, INT, WIS, CHA)
        modifiers: Various modifiers affecting the character
        proficiencies: Skills, tools, and other proficiencies
        personality: Personality traits, ideals, bonds, and flaws
        equipment: List of items and equipment carried
        spells: Spells known and spell slots available
        familiar: Details about any familiar or companion
        motivations: Character's goals and motivations
        data: Additional custom data for the character
    """
    update_data = {k: v for k, v in locals().items() 
                  if k not in ['character_id', 'db'] and v is not None}
    return update_character(db, character_id, **update_data)

@mcp.tool()
def delete_character_tool(character_id: int) -> bool:
    """
    Delete a character.

    Args:
        character_id: The ID of the character to delete
    """
    return delete_character(db, character_id)

@mcp.tool()
def search_characters_tool(
    query: str | None = None,
    campaign_id: int | None = None,
    character_class: str | None = None,
    race: str | None = None
) -> list[Character]:
    """
    Search characters by name, race, class, etc.

    Args:
        query: Search term to look for in character names and details
        campaign_id: Filter characters by campaign ID
        character_class: Filter characters by character class
        race: Filter characters by race
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
    setting_type: str,
    name: str,
    region: str,
    scale: str,
    population: str,
    first_impression: str = None,
    distinctive_features: list[str] = None,
    atmosphere: str = None,
    key_locations: list[str] = None,
    points_of_interest: list[str] = None,
    travel_routes: list[str] = None,
    factions: list[str] = None,
    power_structure: str = None,
    local_customs: str = None,
    economic_basis: str = None,
    origin: str = None,
    recent_history: str = None,
    hidden_past: str = None,
    integration_notes: str = None,
    encounter_recommendations: list[str] = None,
    dramatic_element_opportunities: list[str] = None,
    parent_id: str = None,
    notes: str = None
) -> Setting:
    """
    Create a new setting with detailed information.

    Args:
        setting_type: The type of setting (e.g., City, Town, Dungeon, Forest)
        name: The name of the setting
        region: The region where this setting is located
        scale: The scale of the setting (e.g., Small, Medium, Large)
        population: The population size of the setting
        first_impression: The first impression visitors get of this setting
        distinctive_features: List of distinctive features of this setting
        atmosphere: The general atmosphere or mood of the setting
        key_locations: List of key locations within this setting
        points_of_interest: List of interesting points or landmarks
        travel_routes: Major travel routes to and from this setting
        factions: Major factions or groups present in this setting
        power_structure: The power structure and leadership of this setting
        local_customs: Local customs, traditions, and cultural notes
        economic_basis: The economic foundation of this setting
        origin: The origin story or founding of this setting
        recent_history: Recent historical events affecting this setting
        hidden_past: Secret or hidden history of this setting
        integration_notes: Notes on how to integrate this setting into a campaign
        encounter_recommendations: Recommended encounters for this setting
        dramatic_element_opportunities: Potential dramatic scenarios for this setting
        parent_id: ID of the parent setting if this is a sub-location
        notes: Additional notes about the setting
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
        "parent_id": parent_id,
        "notes": notes
    }
    
    # Remove None values
    setting_data = {k: v for k, v in setting_data.items() if v is not None}
    
    return create_setting(db, **setting_data)

@mcp.tool()
def update_setting_tool(
    setting_id: str,
    setting_type: str | None = None,
    name: str | None = None,
    region: str | None = None,
    scale: str | None = None,
    population: str | None = None,
    first_impression: str | None = None,
    distinctive_features: List[str] | None = None,
    atmosphere: str | None = None,
    key_locations: List[str] | None = None,
    points_of_interest: List[str] | None = None,
    travel_routes: List[str] | None = None,
    factions: List[str] | None = None,
    power_structure: str | None = None,
    local_customs: str | None = None,
    economic_basis: str | None = None,
    origin: str | None = None,
    recent_history: str | None = None,
    hidden_past: str | None = None,
    integration_notes: str | None = None,
    encounter_recommendations: List[str] | None = None,
    dramatic_element_opportunities: List[str] | None = None,
    parent_id: str | None = None,
    notes: str | None = None
) -> dict:
    """
    Update an existing setting.

    Args:
        setting_id: The ID of the setting to update
        setting_type: The type of setting (e.g., City, Town, Dungeon, Forest)
        name: The name of the setting
        region: The region where this setting is located
        scale: The scale of the setting (e.g., Small, Medium, Large)
        population: The population size of the setting
        first_impression: The first impression visitors get of this setting
        distinctive_features: List of distinctive features of this setting
        atmosphere: The general atmosphere or mood of the setting
        key_locations: List of key locations within this setting
        points_of_interest: List of interesting points or landmarks
        travel_routes: Major travel routes to and from this setting
        factions: Major factions or groups present in this setting
        power_structure: The power structure and leadership of this setting
        local_customs: Local customs, traditions, and cultural notes
        economic_basis: The economic foundation of this setting
        origin: The origin story or founding of this setting
        recent_history: Recent historical events affecting this setting
        hidden_past: Secret or hidden history of this setting
        integration_notes: Notes on how to integrate this setting into a campaign
        encounter_recommendations: Recommended encounters for this setting
        dramatic_element_opportunities: Potential dramatic scenarios for this setting
        parent_id: ID of the parent setting if this is a sub-location
        notes: Additional notes about the setting
    Returns:
        dict: The updated Setting and a warning message if unknown fields were provided.
    """
    from models.setting import Setting
    # Collect all update data from locals except setting_id and db, and only include non-None values
    update_data = {k: v for k, v in locals().items() if k not in ['setting_id', 'db'] and v is not None}
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
    setting_id: str
) -> bool:
    """
    Delete a setting.

    Args:
        setting_id: The ID of the setting to delete

    Warning: This will permanently delete the setting and all its data.
    """
    return delete_setting(db, setting_id)

@mcp.tool()
def search_settings_tool(
    query: str
) -> Dict:
    """
    Search settings by name, region, or description.

    Args:
        query: Search term to look for in setting names, regions, or descriptions

    Returns:
        dict: The matching settings, a message, and a count.
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
    setting_type: str
) -> Dict:
    """
    Filter settings by their type (e.g., City, Town, Forest).

    Args:
        setting_type: The type of setting to filter by (e.g., City, Town, Forest)

    Returns:
        dict: The matching settings, a message, and a count.
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
    parent_id: str
) -> Dict:
    """
    Filter settings by their parent setting ID.

    Args:
        parent_id: The ID of the parent setting to filter by

    Returns:
        dict: Child settings of the specified parent, a message, and a count.
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
    name: str
) -> Setting:
    """
    Get a setting by its name.

    Args:
        name: The name of the setting to retrieve

    Raises:
        ValueError: If the setting is not found
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

@mcp.tool()
def get_database_info_tool() -> dict:
    """
    Get database information including name and counts for campaigns, characters, and settings.
    """
    return db.get_info()

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