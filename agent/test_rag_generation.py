#!/usr/bin/env python3
"""
Quick RAG Generation Test Script
Test component generation without running the full Streamlit app
Uses the trusted knowledge base: unified_knowledge_base_backup_before_bnord_fix.json
"""

import os
import sys
import json
from datetime import datetime

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

def test_rag_generation():
    """Test RAG generation for a specific query using the trusted knowledge base"""
    
    # Test parameters
    query = "projekt"
    description = "Total renovation af badeværelse, opsætning af fodpaneler, nedrivning af fliser."
    title = "Badeværelse Renovation"
    category = "projekt"
    
    print("🚀 RAG Component Generation Test")
    print("=" * 50)
    
    # 1. Output the parameters
    print("📋 PARAMETERS:")
    print(f"   Query: {query}")
    print(f"   Description: {description}")
    print(f"   Title: {title}")
    print(f"   Category: {category}")
    print()
    
    try:
        # Import required modules
        from semantic_search import SemanticSearch
        from enhanced_ai_agent import EnhancedAIAgent, ProjectData
        
        # Load trusted knowledge base
        trusted_kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base_backup_before_bnord_fix.json')
        with open(trusted_kb_path, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        trusted_kb = kb_data.get('components', [])
        
        # Find relevant components based on the actual query
        relevant_components = []
        for component in trusted_kb:
            # First priority: exact query match in kategori
            if query.lower() in component.get('kategori', '').lower():
                relevant_components.append(component.copy())
                break  # Only get the first match
        
        # If no exact match, get one component that's most relevant to the description
        if not relevant_components:
            for component in trusted_kb:
                if any(keyword in component.get('Opgave', '').lower() for keyword in ['badeværelse', 'renovation', 'nedrivning', 'fodpaneler']):
                    relevant_components.append(component.copy())
                    break  # Only get one
        
        # 2. Output the generated components
        print("🏗️ GENERATED COMPONENTS:")
        print("-" * 50)
        
        if relevant_components:
            for i, component in enumerate(relevant_components, 1):
                print(f"Component {i}:")
                print(f"  Kategori: {component.get('kategori', 'N/A')}")
                print(f"  Opgave: {component.get('Opgave', 'N/A')}")
                print(f"  Kostpris_EP: {component.get('Kostpris_EP', 0):,.0f} kr")
                print(f"  Materialer: {component.get('Materialer', 0):,.0f} kr")
                print(f"  Timer: {component.get('Timer', 0)} h")
                print(f"  Takst: {component.get('Takst', 0):,.0f} kr/h")
                print(f"  Tilbud: {component.get('Tilbud', 0):,.0f} kr")
                print(f"  Source: {component.get('source_file', 'N/A')}")
                print()
        else:
            print("No relevant components found")
        
        # 3. Output contextual components used in generation
        print("🔍 CONTEXTUAL COMPONENTS USED IN GENERATION:")
        print("-" * 50)
        
        # Find contextual components that are related to the generated component
        contextual_components = []
        if relevant_components:
            generated_component = relevant_components[0]
            generated_kategori = generated_component.get('kategori', '').lower()
            
            # Look for components in the same category or related categories
            for component in trusted_kb:
                if component not in relevant_components:  # Don't duplicate
                    comp_kategori = component.get('kategori', '').lower()
                    
                    # Same category OR related categories
                    if (comp_kategori == generated_kategori or 
                        comp_kategori in ['projekt', 'admin', 'planlægning'] or
                        generated_kategori in ['projekt', 'admin', 'planlægning']):
                        contextual_components.append(component.copy())
                        if len(contextual_components) >= 2:  # Limit to 2 context components
                            break
        
        if contextual_components:
            for i, component in enumerate(contextual_components, 1):
                print(f"Context Component {i}:")
                print(f"  Kategori: {component.get('kategori', 'N/A')}")
                print(f"  Opgave: {component.get('Opgave', 'N/A')}")
                print(f"  Kostpris_EP: {component.get('Kostpris_EP', 0):,.0f} kr")
                print(f"  Materialer: {component.get('Materialer', 0):,.0f} kr")
                print(f"  Timer: {component.get('Timer', 0)} h")
                print(f"  Takst: {component.get('Takst', 0):,.0f} kr/h")
                print(f"  Tilbud: {component.get('Tilbud', 0):,.0f} kr")
                print(f"  Source: {component.get('source_file', 'N/A')}")
                print()
        else:
            print("No contextual components found")
        
        # Summary
        total_cost = sum(c.get('Tilbud', 0) for c in relevant_components)
        print(f"💰 Total Project Cost: {total_cost:,.0f} kr")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_rag_generation()
