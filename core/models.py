from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    name: str
    type: str
    priority: int = 3
    est: int = 30
    complete: bool = False
    chain: Optional[str] = None

@dataclass
class SavedTask:
    name: str
    type: str
    default_est: int
    default_priority: int = 3
    note: Optional[str] = None
