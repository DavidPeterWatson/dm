from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
# from mcp.types import Message, UserMessage, AssistantMessage
from database.campaign_operations import (
    create_campaign,
    update_campaign,
    delete_campaign,
    search_campaigns,
    get_campaign,
    list_campaigns
)
from database.character_operations import (
    create_character,
    update_character,
    delete_character,
    get_character,
    list_characters,
    list_campaign_characters,
    search_characters,
    update_character_progress
)
from models.campaign import Campaign
from models.character import Character
from utils.helpers import validate_campaign_data, validate_character_data
from typing import List, Optional

mcp = FastMCP("D&D Game Master Assistant", dependencies=["pydantic", "sqlite-utils", "rich"])

# Campaign Management Tools

@mcp.tool()
def create_campaign_tool(name: str, description: str) -> Campaign:
    """
    Create a new campaign.
    """
    validate_campaign_data(name, description)
    return create_campaign(name, description)

@mcp.tool()
def update_campaign_tool(campaign_id: int, name: str, description: str) -> Campaign:
    """
    Update an existing campaign.
    """
    validate_campaign_data(name, description)
    return update_campaign(campaign_id, name, description)

@mcp.tool()
def delete_campaign_tool(campaign_id: int) -> bool:
    """
    Delete a campaign.
    """
    return delete_campaign(campaign_id)

@mcp.tool()
def search_campaigns_tool(query: str) -> list[Campaign]:
    """
    Search campaigns by name or description.
    """
    return search_campaigns(query)

# Character Management Tools

@mcp.tool()
def create_character_tool(name: str, campaign_id: int, player_name: Optional[str] = None,
                         race: Optional[str] = None, character_class: Optional[str] = None,
                         level: int = 1) -> Character:
    """
    Create a new character.
    """
    validate_character_data(name, campaign_id)
    return create_character(
        name=name,
        campaign_id=campaign_id,
        player_name=player_name,
        race=race,
        character_class=character_class,
        level=level
    )

@mcp.tool()
def update_character_tool(character_id: int, **kwargs) -> Character:
    """
    Update an existing character.
    """
    return update_character(character_id, **kwargs)

@mcp.tool()
def delete_character_tool(character_id: int) -> bool:
    """
    Delete a character.
    """
    return delete_character(character_id)

@mcp.tool()
def search_characters_tool(query: Optional[str] = None, campaign_id: Optional[int] = None,
                          character_class: Optional[str] = None, race: Optional[str] = None) -> list[Character]:
    """
    Search characters by name, race, class, etc.
    """
    return search_characters(
        query=query,
        campaign_id=campaign_id,
        character_class=character_class,
        race=race
    )

@mcp.tool()
def level_up_character_tool(character_id: int) -> Character:
    """
    Level up a character.
    """
    character = get_character(character_id)
    new_level = character.level + 1
    return update_character(character_id, level=new_level)

@mcp.tool()
def track_character_progress_tool(character_id: int, current_location: Optional[str] = None,
                                 key_discoveries: Optional[List[str]] = None) -> Character:
    """
    Update character campaign progress.
    """
    return update_character_progress(
        character_id=character_id,
        current_location=current_location,
        key_discoveries=key_discoveries
    )

# Campaign Resources

@mcp.resource("campaign://{campaign_id}")
def get_campaign_resource(campaign_id: int) -> Campaign:
    """
    Get campaign details.
    """
    return get_campaign(campaign_id)

@mcp.resource("campaign://list")
def list_campaigns_resource() -> list[Campaign]:
    """
    List all campaigns.
    """
    return list_campaigns()

# Character Resources

@mcp.resource("character://{character_id}")
def get_character_resource(character_id: int) -> Character:
    """
    Get character details.
    """
    return get_character(character_id)

@mcp.resource("character://list")
def list_characters_resource() -> list[Character]:
    """
    List all characters.
    """
    return list_characters()

@mcp.resource("character://campaign/{campaign_id}/list")
def list_campaign_characters_resource(campaign_id: int) -> list[Character]:
    """
    List all characters in a campaign.
    """
    return list_campaign_characters(campaign_id)

# Prompts

# @mcp.prompt()
# def create_new_campaign_prompt(name: str, description: str) -> Message:
#     return UserMessage(content=f"Create a new campaign named '{name}' with description '{description}'.")

# @mcp.prompt()
# def update_existing_campaign_prompt(campaign_id: int, name: str, description: str) -> Message:
#     return UserMessage(content=f"Update campaign ID {campaign_id} to name '{name}' with description '{description}'.")

if __name__ == "__main__":
    mcp.run() 