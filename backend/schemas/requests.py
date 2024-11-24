from typing import List, Optional
from pydantic import BaseModel, EncodedBytes


class SearchRequest(BaseModel):
    description: str
    location: str


class CreateRequest(BaseModel):
    address = str
    sqft = int
    price = float
    images = List[EncodedBytes]
    metadata = Optional[dict]