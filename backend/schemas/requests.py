from pydantic import BaseModel


class SearchRequest(BaseModel):
    description: str
    location: str
