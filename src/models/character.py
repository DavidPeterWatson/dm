from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any

class Ability(BaseModel):
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None

class Proficiencies(BaseModel):
    saving_throws: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    weapons: Optional[List[str]] = None
    armor: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    languages: Optional[List[str]] = None

class Personality(BaseModel):
    trait: Optional[str] = None
    ideal: Optional[str] = None
    bond: Optional[str] = None
    flaw: Optional[str] = None

class Spells(BaseModel):
    cantrips: Optional[List[str]] = None
    level_1: Optional[List[str]] = None
    level_2: Optional[List[str]] = None
    level_3: Optional[List[str]] = None
    level_4: Optional[List[str]] = None
    level_5: Optional[List[str]] = None
    level_6: Optional[List[str]] = None
    level_7: Optional[List[str]] = None
    level_8: Optional[List[str]] = None
    level_9: Optional[List[str]] = None

class Familiar(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    special_abilities: Optional[List[str]] = None

class Character(BaseModel):
    id: str
    campaign_id: str
    name: str
    player_name: Optional[str] = None
    race: Optional[str] = None
    character_class: Optional[str] = Field(None, alias="class")
    subclass: Optional[str] = None
    background: Optional[str] = None
    level: Optional[int] = 1
    ability_scores: Optional[Ability] = None
    modifiers: Optional[Ability] = None
    proficiencies: Optional[Proficiencies] = None
    personality: Optional[Personality] = None
    backstory: Optional[str] = None
    equipment: Optional[List[str]] = None
    spells: Optional[Spells] = None
    familiar: Optional[Familiar] = None
    motivations: Optional[List[str]] = None
    data: Dict = {}
    created_at: str
    updated_at: str
    
    class Config:
        populate_by_name = True 