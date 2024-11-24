from sqlmodel import Session
from backend import db
from backend.models import Property
import os
from dotenv import load_dotenv

# embedding model
from llm_generation.rag_utils import RAGSystem

rag_system = RAGSystem()

def search(description: str, location: str):
    embedding = rag_system.generate_embedding(description)

    results = (
        db.query(Property)
        .filter(
            cosine_distance(Property.embedding, embedding)
            < EMBEDDING_THRESHOLD
        )
        .all()
    )

    session.scalars(select(Item.embedding.l2_distance([3, 1, 2])))

    if results:
        ranked_docs = rag_system.rerank(description, results)
    else:
        return []

    return ranked_docs
