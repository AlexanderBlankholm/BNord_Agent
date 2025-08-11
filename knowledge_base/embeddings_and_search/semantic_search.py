import json
from component_embeddings import ComponentEmbeddings
from typing import List, Dict, Any

class SemanticSearch:
    """
    Simple semantic search interface for the construction components knowledge base.
    """
    
    def __init__(self, embeddings_manager=None):
        """Initialize the semantic search system."""
        if embeddings_manager:
            self.embeddings_manager = embeddings_manager
        else:
            self.embeddings_manager = ComponentEmbeddings()
        
        if not self.embeddings_manager.embeddings:
            print("Generating embeddings...")
            self.embeddings_manager.generate_embeddings()
    
    def search(self, query: str, top_k: int = 10, min_similarity: float = 0.1) -> List[Dict[str, Any]]:
        """
        Search for components using natural language.
        
        Args:
            query: Natural language search query
            top_k: Maximum number of results to return
            min_similarity: Minimum similarity score (0.0 to 1.0)
        
        Returns:
            List of component dictionaries with similarity scores
        """
        results = self.embeddings_manager.search_components(query, top_k=top_k)
        
        # Filter by minimum similarity and format results
        formatted_results = []
        for comp_idx, similarity, component in results:
            if similarity >= min_similarity:
                result = component.copy()
                result['similarity_score'] = similarity
                result['component_index'] = comp_idx
                formatted_results.append(result)
        
        return formatted_results
    
    def search_by_category(self, query: str, kategori: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for components within a specific category.
        
        Args:
            query: Natural language search query
            kategori: Category to filter by
            top_k: Maximum number of results to return
        
        Returns:
            List of filtered component dictionaries
        """
        all_results = self.search(query, top_k=top_k * 2)  # Get more results to filter
        
        # Filter by category
        category_results = [
            result for result in all_results 
            if result.get('kategori', '').lower() == kategori.lower()
        ]
        
        return category_results[:top_k]
    
    def search_by_cost_range(self, query: str, min_cost: float = 0, max_cost: float = None, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for components within a specific cost range.
        
        Args:
            query: Natural language search query
            min_cost: Minimum cost filter
            max_cost: Maximum cost filter (None for no upper limit)
            top_k: Maximum number of results to return
        
        Returns:
            List of filtered component dictionaries
        """
        all_results = self.search(query, top_k=top_k * 2)  # Get more results to filter
        
        # Filter by cost range
        cost_results = []
        for result in all_results:
            tilbud = result.get('Tilbud', 0)
            if tilbud >= min_cost and (max_cost is None or tilbud <= max_cost):
                cost_results.append(result)
        
        return cost_results[:top_k]
    
    def get_search_summary(self, query: str, top_k: int = 20) -> Dict[str, Any]:
        """
        Get a summary of search results including statistics.
        
        Args:
            query: Natural language search query
            top_k: Maximum number of results to analyze
        
        Returns:
            Dictionary with search summary statistics
        """
        results = self.search(query, top_k=top_k)
        
        if not results:
            return {"query": query, "total_results": 0, "message": "No results found"}
        
        # Calculate statistics
        total_cost = sum(result.get('Tilbud', 0) for result in results)
        avg_cost = total_cost / len(results) if results else 0
        
        categories = {}
        trades = {}
        
        for result in results:
            kategori = result.get('kategori', 'Unknown')
            fag = result.get('Fag', 'Unknown')
            
            categories[kategori] = categories.get(kategori, 0) + 1
            trades[fag] = trades.get(fag, 0) + 1
        
        # Sort by frequency
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        top_trades = sorted(trades.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "query": query,
            "total_results": len(results),
            "total_cost": total_cost,
            "average_cost": avg_cost,
            "top_categories": top_categories,
            "top_trades": top_trades,
            "cost_range": {
                "min": min(result.get('Tilbud', 0) for result in results),
                "max": max(result.get('Tilbud', 0) for result in results)
            }
        }
    
    def interactive_search(self):
        """Interactive search interface for testing."""
        print("Semantic Search Interface")
        print("=" * 40)
        print("Type 'quit' to exit, 'help' for commands")
        print()
        
        while True:
            try:
                query = input("Search query: ").strip()
                
                if query.lower() == 'quit':
                    break
                elif query.lower() == 'help':
                    print("\nCommands:")
                    print("  help - Show this help")
                    print("  quit - Exit the search")
                    print("  summary <query> - Get search summary")
                    print("  category <query> <category> - Search within category")
                    print("  cost <query> <min> <max> - Search within cost range")
                    print()
                    continue
                elif query.lower().startswith('summary '):
                    search_query = query[8:]  # Remove 'summary ' prefix
                    summary = self.get_search_summary(search_query)
                    self._print_summary(summary)
                    continue
                elif query.lower().startswith('category '):
                    parts = query.split(' ', 2)
                    if len(parts) >= 3:
                        search_query = parts[1]
                        category = parts[2]
                        results = self.search_by_category(search_query, category)
                        self._print_results(results, f"Results for '{search_query}' in category '{category}'")
                    else:
                        print("Usage: category <query> <category>")
                    continue
                elif query.lower().startswith('cost '):
                    parts = query.split(' ', 3)
                    if len(parts) >= 4:
                        search_query = parts[1]
                        min_cost = float(parts[2])
                        max_cost = float(parts[3])
                        results = self.search_by_cost_range(search_query, min_cost, max_cost)
                        self._print_results(results, f"Results for '{search_query}' with cost {min_cost}-{max_cost} DKK")
                    else:
                        print("Usage: cost <query> <min_cost> <max_cost>")
                    continue
                
                # Regular search
                if query:
                    results = self.search(query, top_k=10)
                    self._print_results(results, f"Results for '{query}'")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        print("\nGoodbye!")
    
    def _print_results(self, results: List[Dict[str, Any]], title: str):
        """Print search results in a formatted way."""
        print(f"\n{title}")
        print("-" * len(title))
        
        if not results:
            print("No results found.")
            return
        
        for i, result in enumerate(results, 1):
            opgave = result.get('Opgave', 'N/A')
            kategori = result.get('kategori', 'N/A')
            fag = result.get('Fag', 'N/A')
            tilbud = result.get('Tilbud', 0)
            similarity = result.get('similarity_score', 0)
            
            # Truncate long descriptions
            if len(opgave) > 80:
                opgave = opgave[:77] + "..."
            
            print(f"{i:2d}. {opgave}")
            print(f"     Category: {kategori:15} | Trade: {fag:10} | Cost: {tilbud:8.0f} DKK | Similarity: {similarity:.3f}")
        
        print(f"\nTotal: {len(results)} results")
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print search summary in a formatted way."""
        print(f"\n Search Summary: '{summary['query']}'")
        print("=" * 50)
        
        if summary['total_results'] == 0:
            print("No results found.")
            return
        
        print(f"Total Results: {summary['total_results']}")
        print(f"Total Cost: {summary['total_cost']:,.0f} DKK")
        print(f"Average Cost: {summary['average_cost']:,.0f} DKK")
        print(f"Cost Range: {summary['cost_range']['min']:,.0f} - {summary['cost_range']['max']:,.0f} DKK")
        
        print(f"\n Top Categories:")
        for category, count in summary['top_categories']:
            print(f"  {category}: {count} components")
        
        print(f"\n🔧 Top Trades:")
        for trade, count in summary['top_trades']:
            print(f"  {trade}: {count} components")

def main():
    """Main function to run the semantic search interface."""
    print("Starting Semantic Search System")
    print("=" * 40)
    
    search_system = SemanticSearch()
    
    # Run interactive search
    search_system.interactive_search()

if __name__ == "__main__":
    main()
