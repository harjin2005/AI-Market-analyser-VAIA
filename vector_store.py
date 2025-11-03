"""Vector store management with ChromaDB and HuggingFace embeddings."""
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from config import config

class VectorStoreManager:
    """Manages vector database operations using free HuggingFace embeddings."""
    
    def __init__(self, model_name=None, persist_directory=None):
        self.model_name = model_name or config.EMBEDDING_MODEL_NAME
        self.persist_directory = persist_directory or config.VECTOR_DB_PATH

        print(f"✓ Loading HuggingFace embedding model: {self.model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"}
        )
        
        self.vector_store = None

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        print(f"✓ Creating vector store with {len(documents)} documents...")
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=config.COLLECTION_NAME
        )

        print(f"✓ Vector store created at: {self.persist_directory}")
        print(f"✓ Embedding model: {self.model_name}")
        return self.vector_store

    def load_vector_store(self) -> Chroma:
        print(f"✓ Loading vector store from: {self.persist_directory}")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=config.COLLECTION_NAME
        )
        return self.vector_store

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def get_retriever(self, k: int = 3):
        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")
        return self.vector_store.as_retriever(search_kwargs={"k": k})
