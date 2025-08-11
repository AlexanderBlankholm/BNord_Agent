#!/usr/bin/env python3
"""
Demonstration of semantic search capabilities for the construction components knowledge base.
Shows how embeddings make searching smoother and more intuitive.
"""

from semantic_search import SemanticSearch
import time

def demonstrate_search_improvements():
    """Demonstrate how embeddings improve search capabilities."""
    
    print(" Semantic Search Demonstration")
    print("=" * 50)
    print("Showing how embeddings make searching smoother and more intuitive")
    print()
    
    search_system = SemanticSearch()
    
    # Example 1: Basic search
    print("Basic Search: 'badeværelse'")
    print("-" * 40)
    results = search_system.search("badeværelse", top_k=5)
    for i, result in enumerate(results[:3], 1):
        opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
        print(f"   {i}. {opgave}")
        print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
    print()
    
    # Example 2: Natural language search
    print("Natural Language: 'kitchen renovation work'")
    print("-" * 40)
    results = search_system.search("kitchen renovation work", top_k=5)
    for i, result in enumerate(results[:3], 1):
        opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
        print(f"   {i}. {opgave}")
        print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
    print()
    
    # Example 3: Category-specific search
    print("Category-Specific: 'electrical work' in EL category")
    print("-" * 40)
    results = search_system.search_by_category("electrical work", "EL", top_k=5)
    for i, result in enumerate(results[:3], 1):
        opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
        print(f"   {i}. {opgave}")
        print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
    print()
    
    # Example 4: Cost-range search
    print("Cost-Range Search: 'demolition work' under 10,000 DKK")
    print("-" * 40)
    results = search_system.search_by_cost_range("demolition work", 0, 10000, top_k=5)
    for i, result in enumerate(results[:3], 1):
        opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
        print(f"   {i}. {opgave}")
        print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
    print()
    
    # Example 5: Search summary
    print("Search Summary: 'renovation'")
    print("-" * 40)
    summary = search_system.get_search_summary("renovation", top_k=20)
    if 'total_results' in summary and summary['total_results'] > 0:
        print(f"   Total Results: {summary['total_results']}")
        print(f"   Total Cost: {summary['total_cost']:,.0f} DKK")
        print(f"   Average Cost: {summary['average_cost']:,.0f} DKK")
        print(f"   Top Categories: {', '.join([cat for cat, _ in summary['top_categories'][:3]])}")
    else:
        print("   No results found for 'renovation'")
    print()
    
    # Example 6: Complex query
    print("Complex Query: 'bathroom and kitchen renovation with new flooring'")
    print("-" * 40)
    results = search_system.search("bathroom and kitchen renovation with new flooring", top_k=5)
    for i, result in enumerate(results[:3], 1):
        opgave = result.get('Opgave', 'N/A')[:60] + "..." if len(result.get('Opgave', '')) > 60 else result.get('Opgave', 'N/A')
        print(f"   {i}. {opgave}")
        print(f"      Cost: {result.get('Tilbud', 0):,.0f} DKK | Similarity: {result.get('similarity_score', 0):.3f}")
    print()

def demonstrate_search_speed():
    """Demonstrate search speed and efficiency."""
    
    print("Search Speed Demonstration")
    print("=" * 40)
    
    search_system = SemanticSearch()
    
    # Test search speed
    queries = [
        "badeværelse",
        "køkken renovation",
        "nedrivning arbejde",
        "VVS installation",
        "el arbejde"
    ]
    
    total_time = 0
    for query in queries:
        start_time = time.time()
        results = search_system.search(query, top_k=10)
        end_time = time.time()
        query_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"Query: '{query}' → {len(results)} results in {query_time:.1f}ms")
        total_time += query_time
    
    avg_time = total_time / len(queries)
    print(f"\nAverage search time: {avg_time:.1f}ms")
    print(f"Total time for {len(queries)} queries: {total_time:.1f}ms")

def main():
    """Main demonstration function."""
    print("Construction Components Semantic Search Demo")
    print("=" * 60)
    print()
    
    # Demonstrate search improvements
    demonstrate_search_improvements()
    
    # Demonstrate search speed
    demonstrate_search_speed()
    
    print("\n Demonstration Complete!")
    print("\nKey Benefits of Embeddings:")
    print("• Natural language queries work smoothly")
    print("• Find related components even with different wording")
    print("• Fast search across 633 components")
    print("• Semantic understanding of construction terminology")
    print("• Easy to extend with new search features")

if __name__ == "__main__":
    main()
