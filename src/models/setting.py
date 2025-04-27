from pydantic import BaseModel
from typing import Dict, Optional, List

class Setting(BaseModel):
    id: str
    setting_type: str  # Village, Town, City, Fortress, Forest, etc.
    name: str
    region: str
    scale: str  # Size indicator (small village, sprawling metropolis, etc.)
    population: str  # Approximate number and diversity of inhabitants
    first_impression: Optional[str] = None  # Read-aloud text for first approach
    distinctive_features: Optional[List[str]] = None  # 3-5 unique features
    atmosphere: Optional[str] = None  # Mood, activity level, sensory details
    key_locations: Optional[List[str]] = None  # 5-8 notable places
    points_of_interest: Optional[List[str]] = None  # Hidden or less obvious locations
    travel_routes: Optional[List[str]] = None  # Major roads, paths, transportation
    factions: Optional[List[str]] = None  # 2-4 influential groups
    power_structure: Optional[str] = None  # Governance and decision-making
    local_customs: Optional[str] = None  # Traditions, taboos, practices
    economic_basis: Optional[str] = None  # Primary industries, trades, resources
    origin: Optional[str] = None  # Brief founding story
    recent_history: Optional[str] = None  # 2-3 significant recent events
    hidden_past: Optional[str] = None  # Secrets or forgotten aspects
    integration_notes: Optional[str] = None  # Campaign arc connections
    encounter_recommendations: Optional[List[str]] = None  # Suitable encounter types
    dramatic_element_opportunities: Optional[List[str]] = None  # Enhanced dramatic elements
    parent_id: Optional[str] = None  # ID of the parent setting (for hierarchical relationships)
    notes: Optional[str] = None  # Additional notes about the setting
    created_at: str
    updated_at: str 