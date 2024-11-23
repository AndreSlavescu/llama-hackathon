from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    description = Column(String)
    vector = Column(Vector(384))  # Assuming a 384-dimensional vector for text embedding
