def validate_campaign_data(name: str, description: str):
    if not name:
        raise ValueError("Campaign name cannot be empty.")
    if not description:
        raise ValueError("Campaign description cannot be empty.") 