from pydantic import BaseModel
from typing import List
from models.article import Article

class JoongangAPIResponse(BaseModel):
    year: int
    month: int
    day: int
    count: int
    articles: List[Article] 