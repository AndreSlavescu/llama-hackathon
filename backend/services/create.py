from typing import List, Optional
from db import db_client
from pydantic import EncodedBytes

from models.property import Property
from utils.coordinates import get_coordinates

# vision model
from groq_utils.


def create_property(
    address: str,
    sqft: int,
    price: float,
    image_paths: List[str],
    metadata: Optional[dict],
) -> Property:
    coordinates = get_coordinates(address)
    print("COORDINATES", coordinates)
    if not coordinates:
        raise Exception("Error: no coordinates")

    # init property in DB
    db_response = (
        db_client.table("Property")
        .insert(
            {
                "address": address,
                "sqft": sqft,
                "price": price,
                "metadata": metadata,
                "coordinates": coordinates,
            }
        )
        .execute()
    )

    data = db_response.data[0]
    print(data)
    property = Property(**data)

    print("PROPERTY", property)
    # Attach all images to the property in DB
    db_client.table("Images").insert(
        [{"id": property.id, "path": image_path} for image_path in image_paths]
    ).execute()

    images: list[bytes] = []
    for image_path in image_paths:
        # with open(f"assets/{image_path}", "wb+") as f:
        response = db_client.storage.from_("images").download(image_path)
        images.append(response)
        # f.write(response)
    # TODO: may have to convert from bytes to base64

    # TODO: Generate a description of the listing from photos
    description = ""

    # TODO: Generate an embedding of the description
    embedding = ""

    # TODO: Update the property in the DB with the description and embedding

    # TODO: Update the property pydantic object

    return None

    return property
