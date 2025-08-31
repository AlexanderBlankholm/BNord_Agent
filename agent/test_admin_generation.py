#!/usr/bin/env python3
"""
Test script to see what the AI agent actually generates for admin components.
"""

import os
import sys
import json

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def main():
    """Test AI agent generation for admin components."""
    print("🧪 Testing AI Agent Generation for Admin Components")
    print("=" * 60)
    
    try:
        # Import the AI agent
        from enhanced_ai_agent import EnhancedAIAgent
        
        # Initialize the agent
        print("🚀 Initializing AI Agent...")
        agent = EnhancedAIAgent()
        
        if not agent.search_system:
            print("❌ Search system not available")
            return
        
        # Test query for admin component
        test_query = "admin"
        print(f"\n🔍 Testing query: '{test_query}'")
        
        # Search for components first
        print("📊 Searching for context components...")
        search_results = agent.search_system.search(test_query, top_k=3, min_similarity=0.2, min_quality_score=0.0)
        
        if search_results:
            print(f"✅ Found {len(search_results)} context components:")
            for i, result in enumerate(search_results, 1):
                print(f"   {i}. {result.get('Opgave', 'N/A')}")
                print(f"      Admin: {result.get('Admin', 0):,.0f} DKK")
                print(f"      Kostpris_EP: {result.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"      Tilbud: {result.get('Tilbud', 0):,.0f} DKK")
                print(f"      Source: {result.get('source_file', 'N/A')}")
                print()
            
            # Show what context components look like
            print("🔍 Context components being sent to LLM:")
            context_components = agent._prepare_context_components(search_results)
            for i, comp in enumerate(context_components):
                print(f"  Component {i+1}: Admin={comp.get('Admin', 'NOT_FOUND')}, Tilbud={comp.get('Tilbud', 'NOT_FOUND')}")
            
            # Test component generation
            print(f"\n🤖 Testing component generation...")
            generated_component = agent.generate_component_with_rag(test_query, use_high_quality_only=True)
            
            if 'error' not in generated_component:
                print(f"✅ Component generated successfully!")
                print(f"   Opgave: {generated_component.get('Opgave', 'N/A')}")
                print(f"   Kategori: {generated_component.get('kategori', 'N/A')}")
                print(f"   Fag: {generated_component.get('Fag', 'N/A')}")
                print(f"   Admin: {generated_component.get('Admin', 0):,.0f} DKK")
                print(f"   Kostpris_EP: {generated_component.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"   Materialer: {generated_component.get('Materialer', 0):,.0f} DKK")
                print(f"   Timer: {generated_component.get('Timer', 0):.1f}")
                print(f"   Takst: {generated_component.get('Takst', 0):,.0f} DKK")
                print(f"   Tilbud: {generated_component.get('Tilbud', 0):,.0f} DKK")
                print(f"   Source: {generated_component.get('source_file', 'N/A')}")
                
                # Check for discrepancies
                print(f"\n🔍 DISCREPANCY CHECK:")
                print(f"   Generated Kostpris_EP: {generated_component.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"   Generated Tilbud: {generated_component.get('Tilbud', 0):,.0f} DKK")
                
                if generated_component.get('Kostpris_EP', 0) != generated_component.get('Tilbud', 0):
                    print(f"   ⚠️ WARNING: Kostpris_EP and Tilbud don't match!")
                    print(f"   💡 This could cause UI display issues")
                else:
                    print(f"   ✅ Kostpris_EP and Tilbud match correctly")
                
                # Show the full generated component
                print(f"\n📋 Full generated component:")
                print(json.dumps(generated_component, indent=2, ensure_ascii=False))
                
            else:
                print(f"❌ Component generation failed: {generated_component.get('error')}")
        
        else:
            print("❌ No search results found")
        
        print(f"\n🎉 Test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
