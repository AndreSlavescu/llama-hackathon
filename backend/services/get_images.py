from typing import List
from db import db_client


def get_image_urls(property_id: int) -> List[str]:
    db_response = (
        db_client.table("Images").select("path").eq("id", property_id).execute()
    )
    data = db_response.data
    print(data)
    result = [image["path"] for image in data]
    return result
