    "dungeon_master": {
      "command": "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv",
      "args": [
        "--directory",
        "/Users/david/Library/Mobile Documents/com~apple~CloudDocs/Documents/repos/github/dm/src",
        "run",
        "dm.py"
      ]
    }



    def get_campaign_by_name(name: str) -> Campaign:
    campaign = campaigns_collection.find_one({"name": name})
    if not campaign:
        raise ValueError(f"Campaign with name {name} does not exist.")
    
    # Format the document to match the Campaign model structure
    campaign_dict = {
        "id": campaign["int_id"],
        "name": campaign["name"],
        "description": campaign["description"],
        "data": campaign.get("data", {}),
        "created_at": campaign["created_at"],
        "updated_at": campaign["updated_at"]
    }
    return Campaign(**campaign_dict)