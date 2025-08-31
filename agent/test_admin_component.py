#!/usr/bin/env python3
"""
Test script for admin component generation with enhanced prompts
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from enhanced_ai_agent import EnhancedAIAgent

def test_admin_component_generation():
    """Test admin component generation specifically"""
    print("🧪 Testing Admin Component Generation...")
    print("=" * 60)
    
    try:
        # Initialize the agent
        print("1. Initializing Enhanced AI Agent...")
        agent = EnhancedAIAgent()
        print("   ✅ AI Agent initialized successfully")
        
        # Test admin component generation
        print("\n2. Testing Admin Component Generation...")
        
        admin_queries = [
            "Projektledelse",
            "Administration og koordinering",
            "Projektstyring"
        ]
        
        for query in admin_queries:
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
                
                # Check if it follows admin component rules
                is_admin_component = (
                    generated_component.get('Materialer', 0) == 0 and
                    generated_component.get('Timer', 0) == 0 and
                    generated_component.get('Takst', 0) == 0 and
                    generated_component.get('Påslag_MAT', 0) == 0 and
                    generated_component.get('Påslag_UE', 0) == 0
                )
                
                if is_admin_component:
                    print("      🎯 Component follows admin rules correctly!")
                else:
                    print("      ⚠️ Component doesn't follow admin rules")
                    
            else:
                print(f"   ❌ Failed to generate component: {generated_component['error']}")
        
        print("\n🎉 Admin Component Generation test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_admin_component_generation()
