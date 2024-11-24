from typing import List, Optional
from pydantic import BaseModel, EncodedBytes


class Property(BaseModel):
    id: int
    address: str
    sqft: int
    price: float
    description: Optional[str]
    embedding: Optional[List[float]]  # TODO: check if correct type
    metadata: Optional[dict]
