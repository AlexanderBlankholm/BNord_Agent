#!/usr/bin/env python3
"""
Test script to check if search is returning correct data.
"""

import os
import sys

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

from component_embeddings import ComponentEmbeddings

def main():
    """Test search functionality."""
    print("🔍 Testing search functionality...")
    
    # Initialize embeddings manager
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
    embeddings_manager = ComponentEmbeddings(knowledge_base_path=kb_path)
    
    # Test search
    print("📊 Searching for 'fodpaneler'...")
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
            print(f"   Source: {component.get('source_file', 'N/A')}")
    else:
        print("❌ No results found")

if __name__ == "__main__":
    main()
