#!/usr/bin/env python3
"""
Test script for problematic queries that were generating 0 DKK components
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from enhanced_ai_agent import EnhancedAIAgent

def test_problematic_queries():
    """Test problematic queries that were generating 0 DKK components"""
    print("🧪 Testing Problematic Queries...")
    print("=" * 60)
    
    try:
        # Initialize the agent
        print("1. Initializing Enhanced AI Agent...")
        agent = EnhancedAIAgent()
        print("   ✅ AI Agent initialized successfully")
        
        # Test problematic queries
        print("\n2. Testing Problematic Queries...")
        
        problematic_queries = [
            "afhentning",
            "nedrivning af fliser",
            "affald",
            "rengøring"
        ]
        
        for query in problematic_queries:
            print(f"\n   Testing: '{query}'")
            print("   " + "-" * 40)
            
            # Generate component
            generated_component = agent.generate_component_with_rag(query, use_high_quality_only=True)
            
            if 'error' not in generated_component:
                print(f"   ✅ Successfully generated component:")
                print(f"      Opgave: {generated_component.get('Opgave', 'N/A')}")
                print(f"      Kategori: {generated_component.get('kategori', 'N/A')}")
                print(f"      Fag: {generated_component.get('Fag', 'N/A')}")
                print(f"      Admin: {generated_component.get('Admin', 0):,.0f} DKK")
                print(f"      Kostpris_EP: {generated_component.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"      Materialer: {generated_component.get('Materialer', 0):,.0f} DKK")
                print(f"      Timer: {generated_component.get('Timer', 0):.1f}")
                print(f"      Takst: {generated_component.get('Takst', 0):,.0f} DKK")
                print(f"      Påslag_MAT: {generated_component.get('Påslag_MAT', 0):.1f}%")
                print(f"      Påslag_UE: {generated_component.get('Påslag_UE', 0):.1f}%")
                print(f"      Tilbud: {generated_component.get('Tilbud', 0):,.0f} DKK")
                print(f"      Kvalitet: {generated_component.get('context_quality', 'unknown')}")
                print(f"      Kilde: {generated_component.get('context_source', 'unknown')}")
                
                # Check if pricing is realistic
                if generated_component.get('Tilbud', 0) > 0:
                    print("      🎯 Component has realistic pricing!")
                else:
                    print("      ⚠️ Component has 0 DKK pricing - this is the problem we're fixing!")
                    
                # Check component type logic
                if 'afhentning' in query.lower() or 'affald' in query.lower() or 'rengøring' in query.lower():
                    is_flat_fee = (
                        generated_component.get('Materialer', 0) == 0 and
                        generated_component.get('Timer', 0) == 0 and
                        generated_component.get('Takst', 0) == 0 and
                        generated_component.get('Påslag_MAT', 0) == 0 and
                        generated_component.get('Påslag_UE', 0) == 0
                    )
                    if is_flat_fee:
                        print("      ✅ Component follows flat fee rules correctly!")
                    else:
                        print("      ⚠️ Component doesn't follow flat fee rules")
                        
                elif 'nedrivning' in query.lower():
                    is_demolition = (
                        generated_component.get('Materialer', 0) == 0 and
                        generated_component.get('Timer', 0) > 0 and
                        generated_component.get('Takst', 0) > 0
                    )
                    if is_demolition:
                        print("      ✅ Component follows demolition rules correctly!")
                    else:
                        print("      ⚠️ Component doesn't follow demolition rules")
                        
            else:
                print(f"   ❌ Failed to generate component: {generated_component['error']}")
        
        print("\n🎉 Problematic Queries test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_problematic_queries()

