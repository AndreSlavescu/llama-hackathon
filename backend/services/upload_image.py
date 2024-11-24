from fastapi import UploadFile
from db import db_client


def upload_image_to_storage(contents: bytes, filepath: str) -> str:
    bucket = "images"

    response = db_client.storage.from_(bucket).upload(
        file=contents,
        path=filepath,
        file_options={"cache-control": 3600, "upsert": "true"},
    )
    public_url = db_client.storage.from_(bucket).get_public_url(filepath)

    return public_url
