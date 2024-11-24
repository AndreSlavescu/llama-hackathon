from typing import List, Optional
from db import db_client
from pydantic import EncodedBytes
import torch
from concurrent.futures import ThreadPoolExecutor

from models.property import Property
from utils.coordinates import get_coordinates

# vision model
from groq_utils.groq_inference import get_completion

# rag utils
from llm_generation.rag_utils import RAGSystem

# typing
from typing import List


def format_descriptions(descriptions: List[str]) -> str:
    final_description = ""
    for i, description in enumerate(descriptions):
        final_description += f"description of image {i+1}: {description}\n"
    return final_description


def create_property(
    address: str,
    sqft: int,
    price: float,
    image_paths: List[str],
    metadata: Optional[dict],
    rag_system: RAGSystem,
) -> Property:
    coordinates = get_coordinates(address)
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
    property = Property(**data)

    # Attach all images to the property in DB
    db_client.table("Images").insert(
        [{"id": property.id, "path": image_path} for image_path in image_paths]
    ).execute()

    images = [
        db_client.storage.from_("images").download(image_path)
        for image_path in image_paths
    ]

    batch_size = 4  
    descriptions = []
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = [
                executor.submit(get_completion, None, img)
                for img in batch
            ]
            batch_descriptions = []
            for future in futures:
                try:
                    result = future.result()
                    batch_descriptions.append(result)
                except Exception as e:
                    print(f"Error processing image: {e}")
                    batch_descriptions.append(None)
            
            descriptions.extend(batch_descriptions)
            
        for img in batch:
            del img
        torch.cuda.empty_cache()

    final_description = format_descriptions(descriptions=descriptions)

    embedding = rag_system.get_embeddings(final_description)
    embedding_list = embedding.flatten().tolist()

    db_response = (
        db_client.table("Property")
        .update({"description": final_description, "embedding": embedding_list})
        .eq("id", property.id)
        .execute()
    )

    data = db_response.data[0]
    property = Property(**data)
    return property.model_dump()
