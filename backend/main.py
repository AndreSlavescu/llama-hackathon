from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np

# llama model
from llm_generation.generate import TextGenerator

from db import get_db
from schemas.requests import SearchRequest

app = FastAPI()
generator = TextGenerator()

@app.post("/generate/")
def generate_text(prompt: str):
    text = generator.generate(prompt)
    return {"text": text}

@app.post("/search/")
def search_properties(search: SearchRequest, db: Session = Depends(get_db)):
    print(search)

    return {"message": "Search successful"}
