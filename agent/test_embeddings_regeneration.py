#!/usr/bin/env python3
"""
Test script to force regeneration of embeddings with corrected knowledge base data.
"""

import os
import sys

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

from component_embeddings import ComponentEmbeddings

def main():
    """Force regeneration of embeddings."""
    print("🔄 Forcing regeneration of embeddings...")
    
    # Initialize embeddings manager with the corrected knowledge base
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
    embeddings_manager = ComponentEmbeddings(knowledge_base_path=kb_path)
    
    # Force regeneration
    print("📊 Regenerating embeddings...")
    success = embeddings_manager.generate_embeddings(force_regenerate=True)
    
    if success:
        print("✅ Embeddings regenerated successfully!")
        print(f"📁 Knowledge base: {kb_path}")
        print(f"📊 Components loaded: {len(embeddings_manager.components)}")
        
        # Test search to verify data is correct
        print("\n🔍 Testing search with 'fodpaneler'...")
        results = embeddings_manager.search_components("fodpaneler", top_k=3)
        
        if results:
            print(f"✅ Found {len(results)} results")
            for i, (comp_idx, similarity, component) in enumerate(results, 1):
                print(f"\n{i}. {component.get('Opgave', 'N/A')}")
                print(f"   Timer: {component.get('Timer', 'N/A')}")
                print(f"   Takst: {component.get('Takst', 'N/A')}")
                print(f"   Materialer: {component.get('Materialer', 'N/A')}")
                print(f"   Kostpris_EP: {component.get('Kostpris_EP', 'N/A')}")
                print(f"   UE: {component.get('UE', 'N/A')}")
                print(f"   Tilbud: {component.get('Tilbud', 'N/A')}")
                print(f"   Similarity: {similarity:.3f}")
        else:
            print("❌ No results found")
    else:
        print("❌ Failed to regenerate embeddings")

if __name__ == "__main__":
    main()
