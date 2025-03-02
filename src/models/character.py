from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class Character(BaseModel):
    id: int
    campaign_id: int
    name: str
    player_name: Optional[str] = None
    race: Optional[str] = None
    character_class: Optional[str] = Field(None, alias="class")
    level: Optional[int] = 1
    data: Dict = {}
    created_at: str
    updated_at: str
    
    class Config:
        populate_by_name = True 