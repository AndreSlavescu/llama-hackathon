from typing import List, Optional
from db import db_client


def create(
    address: str,
    sqft: int,
    listing_price: float,
    coordinates: List[float],
    metadata: Optional[dict] = None,
):
    # Generate a description of the listing from photos
    description = ""

    # Generate an embedding of the description
    embedding = ""

    db_client.table("Property").insert(
        {
            "address": address,
            "description": description,
            "sqft": sqft,
            "listing_price": listing_price,
            "embedding": embedding,
            "coordinates": coordinates,
            "metadata": metadata,
        }
    )
