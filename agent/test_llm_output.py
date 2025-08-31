#!/usr/bin/env python3
"""
Test script to see exactly what the LLM is receiving and outputting
"""

import sys
import os
import json

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from enhanced_ai_agent import EnhancedAIAgent

def test_llm_output():
    """Test what the LLM is receiving and outputting"""
    print("🔍 Testing LLM Input/Output...")
    print("=" * 60)
    
    try:
        # Initialize the agent
        print("1. Initializing Enhanced AI Agent...")
        agent = EnhancedAIAgent()
        print("   ✅ AI Agent initialized successfully")
        
        # Test problematic query
        query = "afhentning"
        print(f"\n2. Testing query: '{query}'")
        print("   " + "-" * 40)
        
        # Search for components
        if agent.search_system:
            results = agent.search_system.search(query, top_k=3, min_similarity=0.2, min_quality_score=1.0)
            
            if results:
                print(f"   Found {len(results)} high-quality components:")
                for i, result in enumerate(results):
                    print(f"   {i+1}. {result.get('Opgave', 'N/A')}")
                    print(f"      UE: {result.get('UE', 0):,.0f} DKK")
                    print(f"      Tilbud: {result.get('Tilbud', 0):,.0f} DKK")
                    print(f"      Source: {result.get('source_file', 'N/A')}")
                    print()
                
                # Show what context components look like
                context_components = agent._prepare_context_components(results)
                print(f"   Context components for RAG:")
                print(f"   {json.dumps(context_components, indent=2, ensure_ascii=False)}")
                
                # Now let's see what the LLM actually receives
                print(f"\n3. Testing LLM generation...")
                print("   " + "-" * 40)
                
                # Generate component
                generated_component = agent.generate_component_with_rag(query, use_high_quality_only=True)
                
                if 'error' not in generated_component:
                    print(f"   ✅ LLM generated component:")
                    print(f"      {json.dumps(generated_component, indent=2, ensure_ascii=False)}")
                else:
                    print(f"   ❌ LLM failed: {generated_component['error']}")
            else:
                print("   No high-quality components found")
        else:
            print("   Search system not available")
        
        print("\n🎉 LLM test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_output()
