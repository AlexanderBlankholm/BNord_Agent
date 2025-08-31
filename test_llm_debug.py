#!/usr/bin/env python3
"""
Debug script to test LLM generation and understand why fallback logic is triggered
"""

import os
import sys
import json

# Add the agent directory to the path
sys.path.append(os.path.dirname(__file__))

from enhanced_ai_agent import EnhancedAIAgent

def test_llm_generation():
    """Test LLM generation to see what's happening"""
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        return
    
    # Initialize agent
    print("🚀 Initializing Enhanced AI Agent...")
    agent = EnhancedAIAgent()
    
    # Test query
    test_query = "Opsætning af nye fodpaneler"
    
    print(f"\n🔍 Testing query: '{test_query}'")
    print("=" * 60)
    
    try:
        # Generate component
        print("🤖 Generating component with RAG...")
        result = agent.generate_component_with_rag(test_query, use_high_quality_only=False)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print("\n✅ Component generated successfully!")
        print("\n📊 Generated Component Details:")
        print("-" * 40)
        
        # Show all fields
        for key, value in result.items():
            if key == 'context_components_used':
                print(f"{key}: {len(value)} context components")
            else:
                print(f"{key}: {value}")
        
        # Check if fallback was used
        if 'pricing_explanation' in result:
            print(f"\n💰 Pricing Explanation: {result['pricing_explanation']}")
        
        # Show context components
        if 'context_components_used' in result:
            print(f"\n🔍 Context Components Used ({len(result['context_components_used'])}):")
            print("-" * 40)
            for i, ctx in enumerate(result['context_components_used']):
                print(f"\n{i+1}. {ctx.get('Opgave', 'N/A')}")
                print(f"   - Kategori: {ctx.get('kategori', 'N/A')}")
                print(f"   - Fag: {ctx.get('Fag', 'N/A')}")
                print(f"   - Tilbud: {ctx.get('Tilbud', 0):,.0f} DKK")
                print(f"   - Source: {ctx.get('source_file', 'N/A')}")
                print(f"   - Quality: {ctx.get('quality_score', 0.5)}")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_generation()
