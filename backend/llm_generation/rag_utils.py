from typing import List
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F
from liger_kernel.transformers import apply_liger_kernel_to_mistral
from sentence_transformers import SentenceTransformer
import numpy as np
import gc
import os

apply_liger_kernel_to_mistral(
    rope=True,
    cross_entropy=False,
    fused_linear_cross_entropy=True,
    rms_norm=True,
    swiglu=True,
    model=None,
)

class RAGSystem:
    def __init__(self):
        torch.backends.cuda.enable_flash_sdp(True)
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

        self.embedding_model = SentenceTransformer(
            "nvidia/NV-Embed-v2", 
            trust_remote_code=True,
        )

        self.embedding_model.max_seq_length = 512
        self.embedding_model.tokenizer.padding_side = "right"

        self.task_instructions = {
            "retrieval": "Given a question, retrieve passages that answer the question",
            "reranking": "Given a question and a list of passages, rerank the passages based on their relevance to the question",
        }

        self.query_prefix = (
            "Instruct: " + self.task_instructions["retrieval"] + "\nQuery: "
        )
        self.passage_prefix = (
            "Instruct: " + self.task_instructions["reranking"] + "\nPassage: "
        )
        self.max_length = 32768

    def get_embeddings(self, texts, is_query=False) -> torch.Tensor:
        prefix = self.query_prefix if is_query else self.passage_prefix
        if isinstance(texts, str):
            texts = [texts]
        
        texts = [text[:4000] for text in texts]
        texts = [text + self.embedding_model.tokenizer.eos_token for text in texts]
        
        with torch.cuda.amp.autocast():
            embeddings = self.embedding_model.encode(
                texts,
                batch_size=1,
                prompt=prefix if is_query else None,
                normalize_embeddings=True,
                convert_to_tensor=True,
                show_progress_bar=False,
            )
        
        result = embeddings.cpu()
        del embeddings
        gc.collect()
        torch.cuda.empty_cache()
        return result

    def compute_similarity(
        self, query_embeddings: torch.Tensor, doc_embeddings: torch.Tensor
    ) -> torch.Tensor:
        return (query_embeddings @ doc_embeddings.T) * 100

    def rerank(self, description: str, docs: list[dict], content_key: str = "content", top_k: int = 12, batch_size: int = 1) -> list[dict]:
        gc.collect()
        torch.cuda.empty_cache()
        
        query_embedding = self.get_embeddings([description], is_query=True)
        
        all_scores = []
        all_docs = []
        
        try:
            for i in range(0, len(docs), batch_size):
                batch_docs = docs[i:i + batch_size]
                
                batch_contents = [str(doc[content_key]) for doc in batch_docs]
                doc_embeddings = self.get_embeddings(batch_contents, is_query=False)
                
                with torch.no_grad():
                    scores = self.compute_similarity(query_embedding, doc_embeddings)
                
                scores = scores.squeeze().cpu().numpy()
                if scores.ndim == 0:
                    scores = np.array([scores])
                
                all_scores.extend(scores)
                all_docs.extend(batch_docs)
                
                del doc_embeddings, scores
                gc.collect()
                torch.cuda.empty_cache()

        except Exception as e:
            print(f"Error during reranking: {e}")
            return docs[:top_k]
        
        del query_embedding
        gc.collect()
        torch.cuda.empty_cache()
        
        sorted_indices = np.argsort(all_scores)[::-1]
        ranked_docs = [all_docs[i] for i in sorted_indices]

        return ranked_docs[:top_k]


def test():
    if not torch.cuda.is_available():
        raise RuntimeError("This code requires a CUDA-enabled GPU")

    rag_system = RAGSystem()

    # Test embedding
    embedding = rag_system.get_embeddings(["This is a test description"])
    embedding2 = rag_system.get_embeddings(["What is AI?"])
    print("Embedding:", embedding)
    print("Embedding2:", embedding2)

    # Test reranking
    test_docs = [
        "This is a test document",
        "This is another test document",
        "This is a completely different document",
    ]
    test_docs2 = [
        "This is a document about machine learning and AI",
        "Here is an article about real estate prices in San Francisco",
        "Documentation for a Python web framework",
        "Research paper on natural language processing",
        "Blog post about software engineering best practices"
        "News article about artificial intelligence breakthroughs",
        "Recipe for chocolate chip cookies",
        "Tutorial on deep learning with PyTorch",
        "Weather forecast for next week",
        "History of computing and early AI research",
        "Movie review of the latest sci-fi film",
        "Guide to buying your first home",
        "Overview of machine learning algorithms",
        "Latest developments in autonomous vehicles",
        "Introduction to neural networks and backpropagation",
    ]

    ranked_docs = rag_system.rerank(
        description="This is a test description", docs=test_docs
    )
    ranked_docs2 = rag_system.rerank(
        description="Which one talks about AI?", docs=test_docs2
    )
    print("\nRanked documents:", ranked_docs)
    print("\nRanked documents2:", ranked_docs2)


if __name__ == "__main__":
    test()
