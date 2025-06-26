from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    name: str
    role: Optional[str] = None 