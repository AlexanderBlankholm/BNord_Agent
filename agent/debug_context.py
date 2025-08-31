#!/usr/bin/env python3
"""
Debug script to see what context components look like for problematic queries
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from enhanced_ai_agent import EnhancedAIAgent

def debug_context():
    """Debug what context components look like for problematic queries"""
    print("🔍 Debugging Context Components...")
    print("=" * 60)
    
    try:
        # Initialize the agent
        print("1. Initializing Enhanced AI Agent...")
        agent = EnhancedAIAgent()
        print("   ✅ AI Agent initialized successfully")
        
        # Test problematic queries
        print("\n2. Debugging Context Components...")
        
        problematic_queries = [
            "afhentning",
            "nedrivning af fliser"
        ]
        
        for query in problematic_queries:
            print(f"\n   Query: '{query}'")
            print("   " + "-" * 40)
            
            # Search for components
            if agent.search_system:
                results = agent.search_system.search(query, top_k=3, min_similarity=0.2, min_quality_score=1.0)
                
                if results:
                    print(f"   Found {len(results)} high-quality components:")
                    for i, result in enumerate(results):
                        print(f"   {i+1}. {result.get('Opgave', 'N/A')}")
                        print(f"      Kategori: {result.get('kategori', 'N/A')}")
                        print(f"      Fag: {result.get('Fag', 'N/A')}")
                        print(f"      Admin: {result.get('Admin', 0):,.0f} DKK")
                        print(f"      Kostpris_EP: {result.get('Kostpris_EP', 0):,.0f} DKK")
                        print(f"      Materialer: {result.get('Materialer', 0):,.0f} DKK")
                        print(f"      Timer: {result.get('Timer', 0):.1f}")
                        print(f"      Takst: {result.get('Takst', 0):,.0f} DKK")
                        print(f"      Tilbud: {result.get('Tilbud', 0):,.0f} DKK")
                        print(f"      Source: {result.get('source_file', 'N/A')}")
                        print()
                    
                    # Show what context components look like
                    context_components = agent._prepare_context_components(results)
                    print(f"   Context components for RAG:")
                    print(f"   {context_components}")
                else:
                    print("   No high-quality components found")
            else:
                print("   Search system not available")
        
        print("\n🎉 Context debugging completed!")
        
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_context()

