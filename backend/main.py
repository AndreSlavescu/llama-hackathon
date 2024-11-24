from fastapi import FastAPI, UploadFile

# llama model
# from llm_generation.llm_generate import TextGenerator

# rag system
from llm_generation.rag_utils import RAGSystem

# vision model
# from groq_utils.groq_inference import get_completion


from services.get_images import get_image_urls
from services.upload_image import upload_image_to_storage
from schemas.requests import CreateRequest
from schemas.responses import CreateResponse
from services.create import create_property
from db import db_client

app = FastAPI()
# generator = TextGenerator()

class RAGSystemWrapper:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RAGSystem()
        return cls._instance

rag_wrapper = RAGSystemWrapper()

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


@app.post("/create", response_model=CreateResponse)
def create(request: CreateRequest):
    rag_system = rag_wrapper.get_instance()
    property_dict = create_property(
        address=request.address,
        sqft=request.sqft,
        price=request.price,
        image_paths=request.image_paths,
        metadata=request.metadata,
        rag_system=rag_system,
    )
    return CreateResponse(property=property_dict)


@app.post("/upload-image")
async def upload_image(image: UploadFile):
    contents = await image.read()
    filepath = f"public/{image.filename}"
    public_url = upload_image_to_storage(contents, filepath)

    return {"image_path": filepath}


@app.get("/{property_id}/images")
def images(property_id: int):
    return get_image_urls(property_id)
