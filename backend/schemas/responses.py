from pydantic import BaseModel

from models.property import Property


class CreateResponse(BaseModel):
    property: Property