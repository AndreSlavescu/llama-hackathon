from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np

from db import get_db
from schemas.requests import SearchRequest

app = FastAPI()


@app.post("/search/")
def search_properties(search: SearchRequest, db: Session = Depends(get_db)):
    print(search)

    return {"message": "Search successful"}
