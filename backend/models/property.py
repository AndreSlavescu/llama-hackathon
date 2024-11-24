from typing import List, Optional
from pydantic import BaseModel, EncodedBytes


class Property(BaseModel):
    id: int
    address: str
    sqft: int
    price: float
    description: Optional[str]
    coordinates: Optional[List[float]]
    metadata: Optional[dict]
