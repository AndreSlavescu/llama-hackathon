from db import db_client
from models.property import Property
import os
import json

# rag_system
from llm_generation.rag_utils import RAGSystem

# text_generator
from llm_generation.llm_generate import TextGenerator

# services_system_prompts
from services.services_system_prompts import SEARCH_SYSTEM_PROMPT


def search_properties(
    description: str,
    location: str,
    text_generator: TextGenerator,
    rag_system: RAGSystem,
):
    # rewritten_description = text_generator.generate(
    #     SEARCH_SYSTEM_PROMPT.format(description=description)
    # )
    rewritten_description = description
    embedding = rag_system.get_embeddings(rewritten_description)

    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()

    if isinstance(embedding[0], list):
        embedding = embedding[0]

    embedding_str = "[" + ",".join(str(float(x)) for x in embedding) + "]"

    EMBEDDING_THRESHOLD = 0.1
    DISTANCE_THRESHOLD = 0.1

    db_response = db_client.rpc(
        "match_documents",
        {
            "query_embedding": embedding_str,
            "match_threshold": EMBEDDING_THRESHOLD,
            "match_count": 20,
        },
    ).execute()

    data = db_response.data

    results = []
    for item in data:
        if isinstance(item, dict):
            results.append(item)

    reranked_results = rag_system.rerank(description, results, content_key="content")

    final_results = []
    for result in reranked_results:
        if isinstance(result["metadata"], str):
            try:
                result["metadata"] = json.loads(result["metadata"])
            except json.JSONDecodeError:
                result["metadata"] = {}

        final_results.append(Property(**result))

    return final_results
