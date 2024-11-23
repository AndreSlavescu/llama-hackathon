from sqlmodel import Session
from backend import db
from backend.models import Property


def search(description: str, location: str, session: Session):
    # TODO: convert description to an embedding
    embedding = None

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
