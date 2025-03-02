from typing import Optional

def validate_campaign_data(name: str, description: str) -> None:
    """
    Validate campaign data.
    """
    if not name:
        raise ValueError("Campaign name cannot be empty")
    if len(name) > 100:
        raise ValueError("Campaign name is too long (max 100 characters)")
    if len(description) > 1000:
        raise ValueError("Campaign description is too long (max 1000 characters)")

def validate_character_data(name: str, campaign_id: int, player_name: Optional[str] = None) -> None:
    """
    Validate character data.
    """
    if not name:
        raise ValueError("Character name cannot be empty")
    if len(name) > 100:
        raise ValueError("Character name is too long (max 100 characters)")
    if campaign_id <= 0:
        raise ValueError("Invalid campaign ID")
    if player_name and len(player_name) > 100:
        raise ValueError("Player name is too long (max 100 characters)") 