from pydantic import BaseModel
from typing import List
from .person import Person

class Article(BaseModel):
    id: str
    title: str
    uri: str
    state: str
    available_time: str
    payflag: str
    categories: List[str]
    hash_tags: List[str]
    timg_uri: str
    description: str
    persons: List[Person] 