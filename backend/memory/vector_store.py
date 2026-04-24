from backend.utils.logger import setup_logger

logger = setup_logger("vector_store")

class VectorStore:
    def __init__(self):
        self.documents = []
        logger.info("Initialized simple in-memory vector store.")

    def add_document(self, text: str, metadata: dict = None):
        self.documents.append({"text": text, "metadata": metadata or {}})
        logger.info(f"Added document: {text[:30]}...")

    def search(self, query: str, top_k: int = 3):
        # Stub implementation: just return all documents (in reality, compute embeddings and similarity)
        logger.info(f"Searching vector store for: {query}")
        return self.documents[:top_k]

vector_store = VectorStore()
