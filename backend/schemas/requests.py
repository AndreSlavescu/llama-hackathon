from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel, EncodedBytes


class SearchRequest(BaseModel):
    description: str
    location: str


class CreateRequest(BaseModel):
    address: str
    sqft: int
    price: float
    image_paths: List[str]
    metadata: Optional[dict]
