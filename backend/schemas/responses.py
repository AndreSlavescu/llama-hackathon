from pydantic import BaseModel

from models import Property


class CreateResponse(BaseModel):
    property = Property