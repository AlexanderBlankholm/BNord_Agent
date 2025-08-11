import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import pickle
import os

class ComponentEmbeddings:
    """
    Generate and manage embeddings for construction components to enable semantic search.
    Focuses on the 'Opgave' field for smooth, intelligent searching.
    """
    
    def __init__(self, knowledge_base_path: str = "unified_knowledge_base.json"):
        """Initialize the embeddings manager."""
        self.kb_path = knowledge_base_path
        self.embeddings_path = "component_embeddings.pkl"
        self.kb_data = None
        self.components = []
        self.embeddings = {}
        self.component_ids = []
        
        # Load knowledge base
        self.load_knowledge_base()
    
    def load_knowledge_base(self) -> bool:
        """Load the knowledge base from file."""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                self.kb_data = json.load(f)
            
            self.components = self.kb_data.get("components", [])
            print(f"✓ Loaded knowledge base with {len(self.components)} components")
            return True
            
        except Exception as e:
            print(f"✗ Error loading knowledge base: {str(e)}")
            return False
    
    def generate_embeddings(self, force_regenerate: bool = False) -> bool:
        """
        Generate embeddings for all components using a simple but effective approach.
        Uses TF-IDF style vectorization for now (can be upgraded to neural embeddings later).
        """
        if not force_regenerate and os.path.exists(self.embeddings_path):
            print("Loading existing embeddings...")
            return self.load_embeddings()
        
        print("Generating new embeddings...")
        
        # Create a simple vocabulary from all Opgave texts
        all_texts = []
        for i, component in enumerate(self.components):
            opgave = component.get("Opgave", "")
            if opgave:
                all_texts.append((i, opgave.lower()))
        
        # Build vocabulary (simple word-based approach)
        vocabulary = set()
        for _, text in all_texts:
            words = text.split()
            vocabulary.update(words)
        
        vocabulary = sorted(list(vocabulary))
        print(f"Built vocabulary with {len(vocabulary)} unique words")
        
        # Generate embeddings (simple TF-IDF style)
        for i, component in enumerate(self.components):
            opgave = component.get("Opgave", "")
            if not opgave:
                # Empty Opgave gets zero vector
                self.embeddings[i] = np.zeros(len(vocabulary))
                continue
            
            # Create simple word frequency vector
            text_words = opgave.lower().split()
            vector = np.zeros(len(vocabulary))
            
            for word in text_words:
                if word in vocabulary:
                    word_idx = vocabulary.index(word)
                    vector[word_idx] += 1
            
            # Normalize vector
            if np.sum(vector) > 0:
                vector = vector / np.sum(vector)
            
            self.embeddings[i] = vector
        
        # Store component IDs for easy lookup
        self.component_ids = list(range(len(self.components)))
        
        # Save embeddings
        self.save_embeddings()
        
        print(f"✓ Generated embeddings for {len(self.components)} components")
        return True
    
    def save_embeddings(self) -> bool:
        """Save embeddings to disk."""
        try:
            embedding_data = {
                "embeddings": self.embeddings,
                "component_ids": self.component_ids,
                "total_components": len(self.components)
            }
            
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(embedding_data, f)
            
            print(f"✓ Saved embeddings to {self.embeddings_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving embeddings: {str(e)}")
            return False
    
    def load_embeddings(self) -> bool:
        """Load embeddings from disk."""
        try:
            with open(self.embeddings_path, 'rb') as f:
                embedding_data = pickle.load(f)
            
            self.embeddings = embedding_data["embeddings"]
            self.component_ids = embedding_data["component_ids"]
            
            print(f"✓ Loaded embeddings for {len(self.embeddings)} components")
            return True
            
        except Exception as e:
            print(f"✗ Error loading embeddings: {str(e)}")
            return False
    
    def search_components(self, query: str, top_k: int = 10) -> List[Tuple[int, float, Dict[str, Any]]]:
        """
        Search for components using semantic similarity.
        Returns list of (component_index, similarity_score, component_data) tuples.
        """
        if not self.embeddings:
            print("No embeddings available. Please generate embeddings first.")
            return []
        
        # Create query embedding (same approach as component embeddings)
        query_words = query.lower().split()
        
        # Build vocabulary from existing embeddings
        vocab_size = len(next(iter(self.embeddings.values())))
        query_vector = np.zeros(vocab_size)
        
        # Simple word matching for now
        for word in query_words:
            # Find word in any component's text
            for comp_idx, component in enumerate(self.components):
                opgave = component.get("Opgave", "").lower()
                if word in opgave:
                    # Add to query vector
                    query_vector += self.embeddings[comp_idx]
        
        # Normalize query vector
        if np.sum(query_vector) > 0:
            query_vector = query_vector / np.sum(query_vector)
        
        # Calculate similarities
        similarities = []
        for comp_idx in self.component_ids:
            if comp_idx in self.embeddings:
                comp_embedding = self.embeddings[comp_idx]
                
                # Cosine similarity
                similarity = np.dot(query_vector, comp_embedding) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(comp_embedding) + 1e-8
                )
                
                similarities.append((comp_idx, similarity))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for comp_idx, similarity in similarities[:top_k]:
            if similarity > 0:  # Only return relevant results
                component_data = self.components[comp_idx]
                results.append((comp_idx, similarity, component_data))
        
        return results
    
    def get_component_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """Get component data by index."""
        if 0 <= index < len(self.components):
            return self.components[index]
        return None
    
    def test_search(self, test_queries: List[str]) -> None:
        """Test the search functionality with example queries."""
        print("\n🔍 Testing Component Search")
        print("=" * 40)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            print("-" * 30)
            
            results = self.search_components(query, top_k=5)
            
            if not results:
                print("No results found")
                continue
            
            for i, (comp_idx, similarity, component) in enumerate(results, 1):
                opgave = component.get("Opgave", "N/A")
                kategori = component.get("kategori", "N/A")
                tilbud = component.get("Tilbud", 0)
                
                print(f"{i}. {opgave}")
                print(f"   Category: {kategori} | Cost: {tilbud:.0f} DKK | Similarity: {similarity:.3f}")

def main():
    """Main function to demonstrate the embedding system."""
    print("Component Embeddings System")
    print("=" * 40)
    
    # Initialize embeddings manager
    embeddings_manager = ComponentEmbeddings()
    
    if not embeddings_manager.kb_data:
        print("Failed to load knowledge base. Exiting.")
        return
    
    # Generate embeddings
    print("\n🚀 Generating Embeddings")
    print("-" * 30)
    success = embeddings_manager.generate_embeddings()
    
    if not success:
        print("Failed to generate embeddings. Exiting.")
        return
    
    # Test search functionality
    print("\n🧪 Testing Search Functionality")
    print("-" * 30)
    
    test_queries = [
        "badeværelse",
        "køkken",
        "nedrivning",
        "murer arbejde",
        "tømrer",
        "VVS installation"
    ]
    
    embeddings_manager.test_search(test_queries)
    
    print("\n✅ Embedding system ready!")
    print("You can now use semantic search to find components more smoothly.")

if __name__ == "__main__":
    main()
