from dataclasses import dataclass

@dataclass

class Command:    
    alias: str
    name: str
    path: str
    id: int | None = None
