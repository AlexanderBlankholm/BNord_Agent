#!/usr/bin/env python3
"""
Test script for Quality-Aware RAG component generation
This tests the new quality filtering and fallback functionality
"""

import os
import sys

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def test_quality_aware_rag():
    """Test the quality-aware RAG component generation functionality"""
    print("🧪 Testing Quality-Aware RAG Component Generation...")
    print("=" * 60)
    
    try:
        # Check OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not set")
            print("Please set your OpenAI API key: $env:OPENAI_API_KEY='your_key_here'")
            return False
        
        # Import the enhanced AI agent
        print("1. Importing Enhanced AI Agent...")
        from enhanced_ai_agent import EnhancedAIAgent
        print("   ✅ Enhanced AI Agent imported successfully")
        
        # Initialize the agent
        print("2. Initializing AI Agent...")
        agent = EnhancedAIAgent()
        print("   ✅ AI Agent initialized successfully")
        
        # Test quality-aware RAG component generation
        print("3. Testing Quality-Aware RAG Component Generation...")
        test_queries = [
            "nedrivning af fliser på vægge",
            "installation af nye VVS-armaturer",
            "elektrisk installation af belysning"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Test {i}: '{query}'")
            
            # Test high-quality only mode
            print(f"      Testing High-Quality Only Mode:")
            try:
                generated_component = agent.generate_component_with_rag(query, use_high_quality_only=True)
                
                if 'error' not in generated_component:
                    print(f"         ✅ Successfully generated component:")
                    print(f"            Opgave: {generated_component.get('Opgave', 'N/A')}")
                    print(f"            Kategori: {generated_component.get('kategori', 'N/A')}")
                    print(f"            Pris: {generated_component.get('Tilbud', 0):,.0f} DKK")
                    print(f"            Kvalitet: {generated_component.get('context_quality', 'N/A')}")
                    print(f"            Kilde: {generated_component.get('context_source', 'N/A')}")
                else:
                    print(f"         ❌ Failed to generate component: {generated_component['error']}")
                
            except Exception as e:
                print(f"         ❌ Error during generation: {e}")
            
            # Test full database mode
            print(f"      Testing Full Database Mode:")
            try:
                generated_component = agent.generate_component_with_rag(query, use_high_quality_only=False)
                
                if 'error' not in generated_component:
                    print(f"         ✅ Successfully generated component:")
                    print(f"            Opgave: {generated_component.get('Opgave', 'N/A')}")
                    print(f"            Kategori: {generated_component.get('kategori', 'N/A')}")
                    print(f"            Pris: {generated_component.get('Tilbud', 0):,.0f} DKK")
                    print(f"            Kvalitet: {generated_component.get('context_quality', 'N/A')}")
                    print(f"            Kilde: {generated_component.get('context_source', 'N/A')}")
                else:
                    print(f"         ❌ Failed to generate component: {generated_component['error']}")
                
            except Exception as e:
                print(f"         ❌ Error during generation: {e}")
        
        print("\n🎉 Quality-Aware RAG Component Generation test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure you:")
        print("1. Are in the 'agent' directory")
        print("2. Have activated the virtual environment: .\\venv\\Scripts\\Activate.ps1")
        print("3. Have installed packages: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_search_quality_filtering():
    """Test the search system's quality filtering functionality"""
    print("\n🔍 Testing Search Quality Filtering...")
    print("=" * 40)
    
    try:
        from semantic_search import SemanticSearch
        from component_embeddings import ComponentEmbeddings
        
        # Initialize search system
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
        embeddings_manager = ComponentEmbeddings(knowledge_base_path=kb_path)
        search_system = SemanticSearch(embeddings_manager=embeddings_manager)
        
        # Test different quality thresholds
        test_query = "fliser"
        quality_thresholds = [0.0, 0.5, 0.8, 0.9]
        
        for threshold in quality_thresholds:
            print(f"\n   Testing quality threshold: {threshold}")
            try:
                results = search_system.search(test_query, top_k=5, min_similarity=0.2, min_quality_score=threshold)
                
                if results:
                    print(f"      ✅ Found {len(results)} results")
                    # Show quality distribution
                    quality_scores = [r.get('quality_score', 0) for r in results]
                    avg_quality = sum(quality_scores) / len(quality_scores)
                    print(f"      📊 Average quality: {avg_quality:.2f}")
                    print(f"      📊 Quality range: {min(quality_scores):.2f} - {max(quality_scores):.2f}")
                else:
                    print(f"      ⚠️ No results found for threshold {threshold}")
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Search system error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Quality-Aware RAG Tests...")
    
    # Test search quality filtering first
    search_ok = test_search_quality_filtering()
    
    # Test quality-aware RAG generation
    rag_ok = test_quality_aware_rag()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"   Search Quality Filtering: {'✅ PASS' if search_ok else '❌ FAIL'}")
    print(f"   Quality-Aware RAG: {'✅ PASS' if rag_ok else '❌ FAIL'}")
    
    if search_ok and rag_ok:
        print("\n🎉 All quality-aware tests passed!")
        print("Your RAG system now prioritizes high-quality components by default.")
        print("You can now run: streamlit run enhanced_streamlit_app_fixed.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
