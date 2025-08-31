#!/usr/bin/env python3
"""
Debug script to test admin component generation and show the discrepancy.
"""

import os
import sys
import json

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def main():
    """Debug admin component generation."""
    print("🔍 Debugging Admin Component Generation")
    print("=" * 60)
    
    # Load the knowledge base
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
    
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        print(f"✅ Loaded knowledge base: {kb_path}")
        print(f"📊 Total components: {len(kb_data.get('components', []))}")
        
        # Find the specific component from the UI
        target_component = None
        for component in kb_data.get('components', []):
            if (component.get('Opgave') == 'Projektledelse, Administration og Parkering' and 
                component.get('Fag') == 'Bnord' and 
                component.get('kategori') == 'Projekt'):
                target_component = component
                break
        
        if target_component:
            print(f"\n🎯 Found target component:")
            print(f"   Opgave: {target_component.get('Opgave')}")
            print(f"   Kategori: {target_component.get('kategori')}")
            print(f"   Fag: {target_component.get('Fag')}")
            print(f"   Admin: {target_component.get('Admin', 0):,.0f} DKK")
            print(f"   Kostpris_EP: {target_component.get('Kostpris_EP', 0):,.0f} DKK")
            print(f"   Materialer: {target_component.get('Materialer', 0):,.0f} DKK")
            print(f"   Timer: {target_component.get('Timer', 0):.1f}")
            print(f"   Takst: {target_component.get('Takst', 0):,.0f} DKK")
            print(f"   Tilbud: {target_component.get('Tilbud', 0):,.0f} DKK")
            print(f"   Source: {target_component.get('source_file', 'N/A')}")
            
            # Show the discrepancy
            print(f"\n🚨 DISCREPANCY ANALYSIS:")
            print(f"   UI shows Kostpris_EP: 7,000 DKK")
            print(f"   Knowledge base shows Kostpris_EP: {target_component.get('Kostpris_EP', 0):,.0f} DKK")
            
            if target_component.get('Kostpris_EP', 0) == 0:
                print(f"   ❌ PROBLEM: Kostpris_EP is 0 in knowledge base!")
                print(f"   💡 This explains why the UI shows 0 DKK for Kostpris_EP")
            else:
                print(f"   ✅ Kostpris_EP matches between UI and knowledge base")
            
            # Check if this is a transformed component
            if target_component.get('original_format') == 'old':
                print(f"\n📝 Component Analysis:")
                print(f"   This is an OLD format component that was transformed")
                print(f"   Original kostpris field was: {target_component.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"   Admin field: {target_component.get('Admin', 0):,.0f} DKK")
                print(f"   Tilbud field: {target_component.get('Tilbud', 0):,.0f} DKK")
                
                # Check if Admin should be used instead
                if target_component.get('Admin', 0) > 0:
                    print(f"   💡 SUGGESTION: Use Admin field ({target_component.get('Admin', 0):,.0f} DKK) for Kostpris_EP")
                elif target_component.get('Tilbud', 0) > 0:
                    print(f"   💡 SUGGESTION: Use Tilbud field ({target_component.get('Tilbud', 0):,.0f} DKK) for Kostpris_EP")
            
        else:
            print(f"❌ Could not find target component in knowledge base")
            
        # Check for similar components
        print(f"\n🔍 Searching for similar admin/project components...")
        admin_components = []
        for component in kb_data.get('components', []):
            if (component.get('kategori') == 'Projekt' and 
                component.get('Fag') == 'Bnord' and
                'admin' in component.get('Opgave', '').lower()):
                admin_components.append(component)
        
        if admin_components:
            print(f"✅ Found {len(admin_components)} similar admin components:")
            for i, comp in enumerate(admin_components[:5], 1):
                print(f"   {i}. {comp.get('Opgave', 'N/A')}")
                print(f"      Admin: {comp.get('Admin', 0):,.0f} DKK")
                print(f"      Kostpris_EP: {comp.get('Kostpris_EP', 0):,.0f} DKK")
                print(f"      Tilbud: {comp.get('Tilbud', 0):,.0f} DKK")
                print(f"      Source: {comp.get('source_file', 'N/A')}")
                print()
        
        print(f"\n🎉 Debug analysis completed!")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")

if __name__ == "__main__":
    main()
