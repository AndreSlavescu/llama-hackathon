from fastapi import FastAPI, Request
import numpy as np

# llama model
# from llm_generation.llm_generate import TextGenerator

# vision model
# from groq_utils.groq_inference import get_completion

from models.property import Listing
from schemas import CreateRequest, CreateResponse
from services.create import create_property

app = FastAPI()
# generator = TextGenerator()


# @app.post("/generate/")
# def generate_text(prompt: str):
#     text = generator.generate(prompt)
#     return {"text": text}


# @app.post("/vision/")
# def vision_inference(image_url: str):
#     text = get_completion(image_url)
#     return {"text": text}


# @app.post("/search/")
# def search_properties(search: SearchRequest):
#     print(search)

#     return {"message": "Search successful"}


@app.post("/create")
def create(request: CreateRequest):
    property = create_property(
        address=request.address,
        sqft=request.sqft,
        price=request.price,
        images=request.images,
        metadata=request.metadata
    )

    return CreateResponse(**property)
