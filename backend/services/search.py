from sqlmodel import Session
from backend import db
from backend.models import Property
from openai import OpenAI


def search(description: str, location: str, session: Session):
    embedding = get_embedding(description)

    EMBEDDING_THRESHOLD = 0.1
    DISTANCE_THRESHOLD = 0.1

    results = (
        db.query(Property)
        .filter(
            cosine_distance(Property.embedding, embedding)
            < EMBEDDING_THRESHOLD  # Threshold can be tuned
        )
        .all()
    )

    session.scalars(select(Item.embedding.l2_distance([3, 1, 2])))

    # TODO: rerank results

    if not results:
        return []

    return [{"id": prop.id} for prop in results]

def get_embedding(text: str, model="text-embedding-3-small"):
   client = OpenAI()
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding
