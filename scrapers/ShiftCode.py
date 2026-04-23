from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass
class ShiftCode:
    code: str
    found_on: datetime
    source: str
    game: Optional[str] = None
    reward: Optional[str] = None
    expires: Optional[datetime] = None
    expired: bool = False
