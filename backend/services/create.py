from db import db_client


def create(
    address: str, description: str, size: int, listing_price: float, metadata=None
):
    db_client.table("Property").insert({""})
