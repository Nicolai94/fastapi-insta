from typing import Optional, List, Dict

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool] = False
    tags: List[str] = []
    metadata: Dict[str, str] = {"key": "value"}
    image: Optional[Image] = None
