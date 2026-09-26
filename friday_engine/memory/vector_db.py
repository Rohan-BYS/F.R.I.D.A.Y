"""
F.R.I.D.A.Y. Infinite Vector Knowledge Base (The Brain).
Uses ChromaDB for embedding large document repositories locally.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from friday_engine.logger import logger

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class VectorBrain:
    """
    RAG Database for massive document retrieval.
    """
    def __init__(self, db_dir: str = "data/vector_brain"):
        self.db_dir = Path(db_dir)
        self.enabled = CHROMA_AVAILABLE
        self.client = None
        self.collection = None
        
        if self.enabled:
            self._init_db()

    def _init_db(self):
        try:
            self.db_dir.mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(path=str(self.db_dir))
            # Use default embedding function for now (all-MiniLM-L6-v2)
            self.collection = self.client.get_or_create_collection(name="friday_knowledge")
            logger.info("Vector Brain (ChromaDB) initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.enabled = False

    def ingest_text(self, document_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Chunk and embed a large text document into the Vector Database."""
        if not self.enabled: return False
        
        # Simple chunking logic
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [metadata or {} for _ in chunks]
        
        try:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Ingested document {document_id} into Vector Brain ({len(chunks)} chunks).")
            return True
        except Exception as e:
            logger.error(f"Failed to ingest document: {e}")
            return False

    def query(self, search_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Semantic search against the Knowledge Base."""
        if not self.enabled: return []
        
        try:
            results = self.collection.query(
                query_texts=[search_text],
                n_results=n_results
            )
            
            extracted = []
            for i in range(len(results['documents'][0])):
                extracted.append({
                    "id": results['ids'][0][i],
                    "document": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i]
                })
            return extracted
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
