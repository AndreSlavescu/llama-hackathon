from transformers import AutoModel, AutoTokenizer
import torch

class RAGSystem:
    def __init__(self):
        self.embedding_model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True).cuda()
        
        self.reranker = AutoModel.from_pretrained("castorini/rank_zephyr_7b_v1_full").cuda()
        self.reranker_tokenizer = AutoTokenizer.from_pretrained("castorini/rank_zephyr_7b_v1_full")

    def generate_embedding(self, description: str) -> str:
        embedding = self.embedding_model.encode(description, task="text-matching")
        return embedding
    
    def rerank(self, description: str, docs: list[str], top_k: int = 12) -> list[str]:
        inputs = self.reranker_tokenizer(
            [description] + docs,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to('cuda')  
        
        with torch.no_grad():
            outputs = self.reranker(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]
        
        query_embedding = embeddings[0]
        doc_embeddings = embeddings[1:]
        scores = torch.nn.functional.cosine_similarity(query_embedding.unsqueeze(0), doc_embeddings)
        
        sorted_indices = scores.argsort(descending=True)
        ranked_docs = [docs[i] for i in sorted_indices.cpu().numpy()]
        
        return ranked_docs[:top_k]

def test():
    if not torch.cuda.is_available():
        raise RuntimeError("This code requires a CUDA-enabled GPU")
        
    rag_system = RAGSystem()
    
    # Test embedding
    embedding = rag_system.generate_embedding("This is a test description")
    embedding2 = rag_system.generate_embedding("What is AI?")
    print("Embedding:", embedding)
    print("Embedding2:", embedding2)

    # Test reranking
    test_docs = [
        "This is a test document",
        "This is another test document",
        "This is a completely different document"
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
        "Introduction to neural networks and backpropagation"
    ]
    
    ranked_docs = rag_system.rerank(
        description="This is a test description",
        docs=test_docs
    )
    ranked_docs2 = rag_system.rerank(
        description="Which one talks about AI?",
        docs=test_docs2
    )
    print("\nRanked documents:", ranked_docs)
    print("\nRanked documents2:", ranked_docs2)

if __name__ == "__main__":
    test()