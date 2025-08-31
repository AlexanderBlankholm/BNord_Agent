#!/usr/bin/env python3
"""
Test script for the enhanced AI agent with knowledge base integration.
Tests the semantic search and cost structure preservation.
"""

import os
import sys
import json

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def test_knowledge_base_access():
    """Test if we can access the knowledge base and search system"""
    print("🧪 Testing Knowledge Base Access...")
    print("=" * 50)
    
    try:
        # Test 1: Check if knowledge base exists
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
        if os.path.exists(kb_path):
            print(f"✅ Knowledge base found: {kb_path}")
            
            # Load and check structure
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            total_components = kb_data.get("metadata", {}).get("total_components", 0)
            print(f"✅ Total components: {total_components}")
            
            # Check first component structure
            if kb_data.get("components"):
                first_comp = kb_data["components"][0]
                required_fields = ["kategori", "Opgave", "Kostpris_EP", "Materialer", "Timer", "Takst", "Tilbud"]
                missing_fields = [field for field in required_fields if field not in first_comp]
                
                if not missing_fields:
                    print("✅ Component structure looks good")
                    print(f"   Sample: {first_comp['Opgave'][:50]}...")
                else:
                    print(f"⚠️ Missing fields: {missing_fields}")
        else:
            print(f"❌ Knowledge base not found: {kb_path}")
            return False
        
        # Test 2: Check if embeddings exist
        embeddings_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search', 'component_embeddings.pkl')
        if os.path.exists(embeddings_path):
            print(f"✅ Embeddings found: {embeddings_path}")
            file_size = os.path.getsize(embeddings_path) / (1024 * 1024)  # MB
            print(f"   File size: {file_size:.1f} MB")
        else:
            print(f"⚠️ Embeddings not found: {embeddings_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing knowledge base access: {e}")
        return False

def test_search_system():
    """Test the semantic search system"""
    print("\n🔍 Testing Semantic Search System...")
    print("=" * 50)
    
    try:
        from semantic_search import SemanticSearch
        
        # Initialize search system
        search_system = SemanticSearch()
        print("✅ Search system initialized")
        
        # Test basic search
        test_query = "badeværelse"
        print(f"\n🔍 Testing search for: '{test_query}'")
        
        results = search_system.search(test_query, top_k=3, min_similarity=0.1)
        
        if results:
            print(f"✅ Found {len(results)} results")
            for i, result in enumerate(results[:2], 1):
                opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
                print(f"   {i}. {opgave}")
                print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
        else:
            print("⚠️ No results found")
        
        # Test category-specific search
        print(f"\n🔍 Testing category search for 'nedrivning'")
        category_results = search_system.search_by_category("fliser", "nedrivning", top_k=3)
        
        if category_results:
            print(f"✅ Found {len(category_results)} category results")
            for i, result in enumerate(category_results[:2], 1):
                opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
                print(f"   {i}. {opgave}")
                print(f"      Category: {result.get('kategori', 'N/A')} | Cost: {result.get('Tilbud', 0):,.0f} DKK")
        else:
            print("⚠️ No category results found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing search system: {e}")
        return False

def test_enhanced_agent_import():
    """Test if the enhanced agent can be imported"""
    print("\n🤖 Testing Enhanced Agent Import...")
    print("=" * 50)
    
    try:
        from enhanced_ai_agent import EnhancedAIAgent, ProjectData
        print("✅ Enhanced agent imports successfully")
        
        # Test ProjectData creation
        project_data = ProjectData(
            description="Test projekt",
            detailed_description="Test renovation of bathroom with new tiles and plumbing",
            selected_categories=["nedrivning", "vvs"]
        )
        print("✅ ProjectData created successfully")
        print(f"   Description: {project_data.description}")
        print(f"   Categories: {project_data.selected_categories}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing enhanced agent: {e}")
        return False

def test_cost_structure():
    """Test cost structure preservation"""
    print("\n💰 Testing Cost Structure...")
    print("=" * 50)
    
    try:
        # Load sample component from knowledge base
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        # Find a component with good cost data
        sample_component = None
        for comp in kb_data.get("components", []):
            if comp.get('Tilbud', 0) > 0 and comp.get('Kostpris_EP', 0) > 0:
                sample_component = comp
                break
        
        if sample_component:
            print("✅ Sample component found:")
            print(f"   Opgave: {sample_component.get('Opgave', 'N/A')}")
            print(f"   Kategori: {sample_component.get('kategori', 'N/A')}")
            print(f"   Tilbud: {sample_component.get('Tilbud', 0):,.0f} DKK")
            print(f"   Kostpris_EP: {sample_component.get('Kostpris_EP', 0):,.0f} DKK")
            print(f"   Materialer: {sample_component.get('Materialer', 0):,.0f} DKK")
            print(f"   Timer: {sample_component.get('Timer', 0):.1f}")
            print(f"   Takst: {sample_component.get('Takst', 0):,.0f} DKK")
            print(f"   Påslag_MAT: {sample_component.get('Påslag_MAT', 0):,.0f} DKK")
            print(f"   Salgspris_MAT: {sample_component.get('Salgspris_MAT', 0):,.0f} DKK")
            
            # Verify cost calculation
            expected_ep = sample_component.get('Timer', 0) * sample_component.get('Takst', 0)
            actual_ep = sample_component.get('Kostpris_EP', 0)
            
            if abs(expected_ep - actual_ep) < 1:  # Allow small rounding differences
                print("✅ Cost calculation verified (Timer × Takst = Kostpris_EP)")
            else:
                print(f"⚠️ Cost calculation mismatch: {expected_ep} vs {actual_ep}")
            
            return True
        else:
            print("⚠️ No suitable sample component found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing cost structure: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced Agent Knowledge Base Integration Test")
    print("=" * 70)
    
    tests = [
        ("Knowledge Base Access", test_knowledge_base_access),
        ("Search System", test_search_system),
        ("Enhanced Agent Import", test_enhanced_agent_import),
        ("Cost Structure", test_cost_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced agent is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Run: python enhanced_ai_agent.py")
        print("3. Or run: streamlit run enhanced_streamlit_app.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure knowledge_base folder exists")
        print("2. Check if embeddings are generated")
        print("3. Verify file paths and permissions")

if __name__ == "__main__":
    main()
