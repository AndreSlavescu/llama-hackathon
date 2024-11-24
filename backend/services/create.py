from typing import List, Optional
from db import db_client
from pydantic import EncodedBytes

from models.property import Property
from utils import get_coordinates


def create_property(
    address: str,
    sqft: int,
    price: float,
    images: List[EncodedBytes],
    metadata: Optional[dict]
) -> Property:
    coordinates = get_coordinates(address)
    if not coordinates:
        raise Exception("Error: no coordinates")

    # TODO: Generate a description of the listing from photos
    description = ""

    # TODO: Generate an embedding of the description
    embedding = ""

    print(coordinates)
    print(images)

    return

    db_response = db_client.table("Property").insert(
        {
            "address": address,
            "description": description,
            "sqft": sqft,
            "price": price,
            "embedding": embedding,
            "coordinates": coordinates,
            "metadata": metadata,
        }
    )

    property = Property(**db_response)

    return property