from fastapi import FastAPI, UploadFile

# llama model
# from llm_generation.llm_generate import TextGenerator

# vision model
# from groq_utils.groq_inference import get_completion

from services.upload_image import upload_image_to_storage
from schemas.requests import CreateRequest
from schemas.responses import CreateResponse
from services.create import create_property
from db import db_client

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


@app.get("/")
def health():
    return {"status": "healthy"}


@app.post("/create")
def create(request: CreateRequest):
    property = create_property(
        address=request.address,
        sqft=request.sqft,
        price=request.price,
        image_paths=request.image_paths,
        metadata=request.metadata,
    )
    return CreateResponse(**property)


@app.post("/upload-image")
async def upload_image(image: UploadFile):
    contents = await image.read()
    filepath = f"public/{image.filename}"
    public_url = upload_image_to_storage(contents, filepath)

    return {"image_path": filepath}
