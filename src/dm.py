from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
# from mcp.types import Message, UserMessage, AssistantMessage
from database.operations import (
    create_campaign,
    update_campaign,
    delete_campaign,
    search_campaigns,
    get_campaign,
    list_campaigns,
)
from models.campaign import Campaign
from utils.helpers import validate_campaign_data

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

# Prompts

# @mcp.prompt()
# def create_new_campaign_prompt(name: str, description: str) -> Message:
#     return UserMessage(content=f"Create a new campaign named '{name}' with description '{description}'.")

# @mcp.prompt()
# def update_existing_campaign_prompt(campaign_id: int, name: str, description: str) -> Message:
#     return UserMessage(content=f"Update campaign ID {campaign_id} to name '{name}' with description '{description}'.")

if __name__ == "__main__":
    mcp.run() 