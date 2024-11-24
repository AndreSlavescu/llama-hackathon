from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    num_results: Optional[int] = 5

class CreateRequest(BaseModel):
    address: str
    sqft: int
    price: float
    coordinates: List[float]
    description: str
    images: List[str]
    metadata: Optional[dict] = None

class CreateResponse(BaseModel):
    id: int
    embedding: str 