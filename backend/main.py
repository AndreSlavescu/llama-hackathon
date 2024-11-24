from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# llama model
from services.search import search_properties
from llm_generation.llm_generate import TextGenerator

# rag system
from llm_generation.rag_utils import RAGSystem

from services.get_images import get_image_urls
from services.upload_image import upload_image_to_storage
from schemas.requests import CreateRequest, SearchRequest
from schemas.responses import CreateResponse
from services.create import create_property

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextGeneratorWrapper:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TextGenerator()
        return cls._instance


class RAGSystemWrapper:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RAGSystem()
        return cls._instance


rag_wrapper = RAGSystemWrapper()
generator_wrapper = TextGeneratorWrapper()


@app.post("/search/")
def search(request: SearchRequest):
    return search_properties(
        request.description,
        request.location,
        generator_wrapper.get_instance(),
        rag_wrapper.get_instance(),
    )


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
