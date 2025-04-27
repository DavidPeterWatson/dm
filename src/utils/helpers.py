from typing import Optional, List

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

def validate_character_data(name: str, campaign_id: str, player_name: Optional[str] = None) -> None:
    """
    Validate character data.
    """
    if not name:
        raise ValueError("Character name cannot be empty")
    if len(name) > 100:
        raise ValueError("Character name is too long (max 100 characters)")
    if not campaign_id:
        raise ValueError("Invalid campaign ID")
    if player_name and len(player_name) > 100:
        raise ValueError("Player name is too long (max 100 characters)")
        
def validate_setting_data(name: str, setting_type: str) -> None:
    """
    Validate setting data.
    """
    if not name:
        raise ValueError("Setting name cannot be empty")
    if len(name) > 100:
        raise ValueError("Setting name is too long (max 100 characters)")
    if not setting_type:
        raise ValueError("Setting type cannot be empty")
    if len(setting_type) > 50:
        raise ValueError("Setting type is too long (max 50 characters)") 