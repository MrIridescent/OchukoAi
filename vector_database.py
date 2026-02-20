"""
Phase 4: Vector Database Integration
Semantic search with in-memory embeddings and similarity-based retrieval
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math
from datetime import datetime

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


@dataclass
class EmbeddingDocument:
    """Document with embedding vector"""
    id: str
    content: str
    embedding: List[float]
    metadata: Dict = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class SimpleEmbeddingGenerator:
    """Generate simple embeddings using TF-IDF-like approach"""
    
    def __init__(self, vocab_size: int = 100):
        self.vocab_size = vocab_size
        self.word_counts: Dict[str, int] = {}
    
    def generate(self, text: str) -> List[float]:
        """Generate embedding from text"""
        words = text.lower().split()
        
        embedding = [0.0] * min(len(words), self.vocab_size)
        
        for i, word in enumerate(words[:self.vocab_size]):
            embedding[i] = len(word) / 20.0 * math.sin(hash(word) % 100 / 100.0)
        
        norm = math.sqrt(sum(x**2 for x in embedding)) or 1.0
        embedding = [x / norm for x in embedding]
        
        return embedding


class SimilarityMetrics:
    """Calculate similarity between embeddings"""
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a**2 for a in vec1)) or 1.0
        mag2 = math.sqrt(sum(b**2 for b in vec2)) or 1.0
        
        return dot_product / (mag1 * mag2)
    
    @staticmethod
    def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
        """Calculate euclidean distance"""
        if len(vec1) != len(vec2):
            return float('inf')
        
        return math.sqrt(sum((a - b)**2 for a, b in zip(vec1, vec2)))
    
    @staticmethod
    def manhattan_distance(vec1: List[float], vec2: List[float]) -> float:
        """Calculate manhattan distance"""
        if len(vec1) != len(vec2):
            return float('inf')
        
        return sum(abs(a - b) for a, b in zip(vec1, vec2))


class VectorIndex:
    """In-memory vector index for similarity search"""
    
    def __init__(self):
        self.documents: Dict[str, EmbeddingDocument] = {}
        self.embedding_generator = SimpleEmbeddingGenerator()
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict] = None,
        embedding: Optional[List[float]] = None
    ) -> EmbeddingDocument:
        """Add document to index"""
        if embedding is None:
            embedding = self.embedding_generator.generate(content)
        
        doc = EmbeddingDocument(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata
        )
        
        self.documents[doc_id] = doc
        logger.info("Document added to index", doc_id=doc_id, content_len=len(content))
        
        return doc
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_metric: str = "cosine"
    ) -> List[Tuple[EmbeddingDocument, float]]:
        """Search for similar documents"""
        query_embedding = self.embedding_generator.generate(query)
        
        if similarity_metric == "cosine":
            similarity_fn = SimilarityMetrics.cosine_similarity
        elif similarity_metric == "euclidean":
            similarity_fn = lambda a, b: -SimilarityMetrics.euclidean_distance(a, b)
        else:
            similarity_fn = SimilarityMetrics.cosine_similarity
        
        similarities = []
        for doc in self.documents.values():
            score = similarity_fn(query_embedding, doc.embedding)
            similarities.append((doc, score))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        logger.info("Search completed", query_len=len(query), results=len(similarities[:top_k]))
        
        return similarities[:top_k]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document from index"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            logger.info("Document deleted", doc_id=doc_id)
            return True
        return False
    
    def update_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Optional[EmbeddingDocument]:
        """Update document"""
        if doc_id not in self.documents:
            return None
        
        embedding = self.embedding_generator.generate(content)
        doc = EmbeddingDocument(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata
        )
        
        self.documents[doc_id] = doc
        logger.info("Document updated", doc_id=doc_id)
        
        return doc
    
    def get_document(self, doc_id: str) -> Optional[EmbeddingDocument]:
        """Get document by ID"""
        return self.documents.get(doc_id)
    
    def list_documents(self) -> List[EmbeddingDocument]:
        """List all documents"""
        return list(self.documents.values())
    
    def size(self) -> int:
        """Get number of documents"""
        return len(self.documents)


class VectorDatabaseInterface:
    """High-level interface for vector database operations"""
    
    def __init__(self):
        self.index = VectorIndex()
        self.collections: Dict[str, VectorIndex] = {}
    
    def create_collection(self, name: str) -> VectorIndex:
        """Create new collection"""
        self.collections[name] = VectorIndex()
        logger.info("Collection created", name=name)
        return self.collections[name]
    
    def get_collection(self, name: str) -> Optional[VectorIndex]:
        """Get collection"""
        return self.collections.get(name)
    
    def add_to_collection(
        self,
        collection: str,
        doc_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> EmbeddingDocument:
        """Add document to collection"""
        idx = self.collections.get(collection)
        if not idx:
            idx = self.create_collection(collection)
        
        return idx.add_document(doc_id, content, metadata)
    
    def search_collection(
        self,
        collection: str,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[EmbeddingDocument, float]]:
        """Search within collection"""
        idx = self.collections.get(collection)
        if not idx:
            return []
        
        return idx.search(query, top_k)
    
    def semantic_search(
        self,
        query: str,
        collection: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Semantic search with formatted results"""
        if collection:
            results = self.search_collection(collection, query, top_k)
            idx = self.collections[collection]
        else:
            results = self.index.search(query, top_k)
            idx = self.index
        
        formatted = []
        for doc, score in results:
            formatted.append({
                "id": doc.id,
                "content": doc.content[:200],
                "similarity_score": score,
                "metadata": doc.metadata,
                "collection": collection or "default"
            })
        
        logger.info("Semantic search completed", query=query, results=len(formatted))
        return formatted
    
    def get_collection_stats(self, collection: str) -> Dict:
        """Get collection statistics"""
        idx = self.collections.get(collection)
        if not idx:
            return {}
        
        return {
            "collection": collection,
            "document_count": idx.size(),
            "documents": [
                {
                    "id": doc.id,
                    "content_length": len(doc.content),
                    "created_at": doc.created_at.isoformat()
                }
                for doc in idx.list_documents()
            ]
        }


global_vector_db = VectorDatabaseInterface()
