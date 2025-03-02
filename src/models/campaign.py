from pydantic import BaseModel
from typing import Dict, Optional

class Campaign(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    data: Dict
    created_at: str
    updated_at: str 