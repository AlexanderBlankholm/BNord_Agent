#!/usr/bin/env python3
"""
Test script to test the AI agent with fodpaneler components (non-Projekt category).
"""

import os
import sys
import json

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def main():
    """Test AI agent generation for fodpaneler components."""
    print("🧪 Testing AI Agent Generation for Fodpaneler Components")
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
        
        # Test query for fodpaneler component
        test_query = "fodpaneler"
        print(f"\n🔍 Testing query: '{test_query}'")
        
        # Search for components first
        print("📊 Searching for context components...")
        search_results = agent.search_system.search(test_query, top_k=3, min_similarity=0.2, min_quality_score=0.0)
        
        if search_results:
            print(f"✅ Found {len(search_results)} context components:")
            for i, result in enumerate(search_results, 1):
                print(f"   {i}. {result.get('Opgave', 'N/A')}")
                print(f"      Kategori: {result.get('kategori', 'N/A')}")
                print(f"      Fag: {result.get('Fag', 'N/A')}")
                print(f"      Timer: {result.get('Timer', 0):.1f}")
                print(f"      Takst: {result.get('Takst', 0):,.0f} DKK")
                print(f"      Kostpris_EP: {result.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"      Materialer: {result.get('Materialer', 0):,.0f} DKK")
                print(f"      Tilbud: {result.get('Tilbud', 0):,.0f} DKK")
                print(f"      Source: {result.get('source_file', 'N/A')}")
                print()
            
            # Test component generation
            print(f"\n🤖 Testing component generation...")
            generated_component = agent.generate_component_with_rag(test_query, use_high_quality_only=False)
            
            if 'error' not in generated_component:
                print(f"✅ Component generated successfully!")
                print(f"   Opgave: {generated_component.get('Opgave', 'N/A')}")
                print(f"   Kategori: {generated_component.get('kategori', 'N/A')}")
                print(f"   Fag: {generated_component.get('Fag', 'N/A')}")
                print(f"   Admin: {generated_component.get('Admin', 0):,.0f} DKK")
                print(f"   Timer: {generated_component.get('Timer', 0):.1f}")
                print(f"   Takst: {generated_component.get('Takst', 0):,.0f} DKK")
                print(f"   Kostpris_EP: {generated_component.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"   Materialer: {generated_component.get('Materialer', 0):,.0f} DKK")
                print(f"   Påslag_MAT: {generated_component.get('Påslag_MAT', 0):.1f}%")
                print(f"   Salgspris_MAT: {generated_component.get('Salgspris_MAT', 0):,.0f} DKK")
                print(f"   UE: {generated_component.get('UE', 0):,.0f} DKK")
                print(f"   Påslag_UE: {generated_component.get('Påslag_UE', 0):.1f}%")
                print(f"   Salgspris_UE: {generated_component.get('Salgspris_UE', 0):,.0f} DKK")
                print(f"   Tilbud: {generated_component.get('Tilbud', 0):,.0f} DKK")
                
                # Check business rule compliance
                print(f"\n🔍 BUSINESS RULE COMPLIANCE CHECK:")
                
                # Check mathematical relationships
                expected_kostpris = generated_component.get('Timer', 0) * generated_component.get('Takst', 0)
                actual_kostpris = generated_component.get('Kostpris_EP', 0)
                if abs(expected_kostpris - actual_kostpris) < 1:
                    print(f"   ✅ Kostpris_EP = Timer × Takst: {expected_kostpris:.0f} DKK")
                else:
                    print(f"   ❌ Kostpris_EP mismatch: Expected {expected_kostpris:.0f}, Got {actual_kostpris:.0f}")
                
                # Check Bnord rules
                if generated_component.get('Fag', '') == 'Bnord':
                    if generated_component.get('UE', 0) == 0 and generated_component.get('Påslag_UE', 0) == 0 and generated_component.get('Salgspris_UE', 0) == 0:
                        print(f"   ✅ Bnord rules enforced: UE = 0, Påslag_UE = 0, Salgspris_UE = 0")
                    else:
                        print(f"   ❌ Bnord rules violated: UE = {generated_component.get('UE', 0)}, Påslag_UE = {generated_component.get('Påslag_UE', 0)}, Salgspris_UE = {generated_component.get('Salgspris_UE', 0)}")
                
                # Check final calculation
                expected_tilbud = (generated_component.get('Admin', 0) + 
                                 generated_component.get('Kostpris_EP', 0) + 
                                 generated_component.get('Salgspris_MAT', 0) + 
                                 generated_component.get('Salgspris_UE', 0))
                actual_tilbud = generated_component.get('Tilbud', 0)
                if abs(expected_tilbud - actual_tilbud) < 1:
                    print(f"   ✅ Tilbud calculation: {expected_tilbud:.0f} DKK")
                else:
                    print(f"   ❌ Tilbud mismatch: Expected {expected_tilbud:.0f}, Got {actual_tilbud:.0f}")
                
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
