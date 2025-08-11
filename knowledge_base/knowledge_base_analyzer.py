import json
from typing import Dict, List, Any, Optional
from collections import defaultdict
import statistics

class KnowledgeBaseAnalyzer:
    """
    Utility class for analyzing and querying the unified knowledge base.
    Provides common analysis functions and data insights.
    """
    
    def __init__(self, knowledge_base_path: str = "unified_knowledge_base.json"):
        """Initialize the analyzer with the knowledge base file."""
        self.kb_path = knowledge_base_path
        self.kb_data = None
        self.components = []
        self.metadata = {}
        self.load_knowledge_base()
    
    def load_knowledge_base(self) -> bool:
        """Load the knowledge base from file."""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                self.kb_data = json.load(f)
            
            self.components = self.kb_data.get("components", [])
            self.metadata = self.kb_data.get("metadata", {})
            
            print(f"✓ Loaded knowledge base with {len(self.components)} components")
            return True
            
        except Exception as e:
            print(f"✗ Error loading knowledge base: {str(e)}")
            return False
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get comprehensive summary statistics."""
        if not self.components:
            return {}
        
        stats = {
            "total_components": len(self.components),
            "total_files": self.metadata.get("total_files_processed", 0),
            "format_breakdown": self.metadata.get("format_breakdown", {}),
            "categories": {},
            "trades": {},
            "cost_ranges": {},
            "labor_stats": {},
            "material_stats": {}
        }
        
        # Category breakdown
        categories = defaultdict(int)
        trades = defaultdict(int)
        total_costs = []
        labor_hours = []
        material_costs = []
        
        for component in self.components:
            # Count categories
            kategori = component.get("kategori", "Unknown")
            categories[kategori] += 1
            
            # Count trades
            fag = component.get("Fag", "Unknown")
            trades[fag] += 1
            
            # Collect cost data
            tilbud = component.get("Tilbud", 0)
            if tilbud > 0:
                total_costs.append(tilbud)
            
            # Collect labor data
            timer = component.get("Timer", 0)
            if timer > 0:
                labor_hours.append(timer)
            
            # Collect material data
            materialer = component.get("Materialer", 0)
            if materialer > 0:
                material_costs.append(materialer)
        
        stats["categories"] = dict(categories)
        stats["trades"] = dict(trades)
        
        # Cost statistics
        if total_costs:
            stats["cost_ranges"] = {
                "min": min(total_costs),
                "max": max(total_costs),
                "average": statistics.mean(total_costs),
                "median": statistics.median(total_costs),
                "total": sum(total_costs)
            }
        
        # Labor statistics
        if labor_hours:
            stats["labor_stats"] = {
                "total_hours": sum(labor_hours),
                "average_hours": statistics.mean(labor_hours),
                "median_hours": statistics.median(labor_hours)
            }
        
        # Material statistics
        if material_costs:
            stats["material_stats"] = {
                "total_materials": sum(material_costs),
                "average_materials": statistics.mean(material_costs),
                "median_materials": statistics.median(material_costs)
            }
        
        return stats
    
    def search_components(self, 
                         kategori: Optional[str] = None,
                         fag: Optional[str] = None,
                         min_cost: Optional[float] = None,
                         max_cost: Optional[float] = None,
                         search_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search components based on various criteria."""
        results = []
        
        for component in self.components:
            # Apply filters
            if kategori and component.get("kategori") != kategori:
                continue
            
            if fag and component.get("Fag") != fag:
                continue
            
            if min_cost is not None and component.get("Tilbud", 0) < min_cost:
                continue
            
            if max_cost is not None and component.get("Tilbud", 0) > max_cost:
                continue
            
            if search_text:
                opgave = component.get("Opgave", "").lower()
                if search_text.lower() not in opgave:
                    continue
            
            results.append(component)
        
        return results
    
    def get_category_analysis(self, kategori: str) -> Dict[str, Any]:
        """Get detailed analysis for a specific category."""
        category_components = [c for c in self.components if c.get("kategori") == kategori]
        
        if not category_components:
            return {"error": f"Category '{kategori}' not found"}
        
        analysis = {
            "category": kategori,
            "component_count": len(category_components),
            "total_cost": sum(c.get("Tilbud", 0) for c in category_components),
            "total_labor_hours": sum(c.get("Timer", 0) for c in category_components),
            "total_materials": sum(c.get("Materialer", 0) for c in category_components),
            "trades_used": list(set(c.get("Fag", "") for c in category_components if c.get("Fag"))),
            "cost_distribution": {},
            "components": category_components
        }
        
        # Cost distribution
        costs = [c.get("Tilbud", 0) for c in category_components if c.get("Tilbud", 0) > 0]
        if costs:
            analysis["cost_distribution"] = {
                "min": min(costs),
                "max": max(costs),
                "average": statistics.mean(costs),
                "median": statistics.median(costs)
            }
        
        return analysis
    
    def get_trade_analysis(self, fag: str) -> Dict[str, Any]:
        """Get detailed analysis for a specific trade."""
        trade_components = [c for c in self.components if c.get("Fag") == fag]
        
        if not trade_components:
            return {"error": f"Trade '{fag}' not found"}
        
        analysis = {
            "trade": fag,
            "component_count": len(trade_components),
            "total_cost": sum(c.get("Tilbud", 0) for c in trade_components),
            "total_labor_hours": sum(c.get("Timer", 0) for c in trade_components),
            "total_materials": sum(c.get("Materialer", 0) for c in trade_components),
            "categories_worked": list(set(c.get("kategori", "") for c in trade_components if c.get("kategori"))),
            "average_markup": 0,
            "components": trade_components
        }
        
        # Calculate average markup
        markups = []
        for component in trade_components:
            påslag_mat = component.get("Påslag_MAT", 0)
            påslag_ue = component.get("Påslag_UE", 0)
            if påslag_mat > 0:
                markups.append(påslag_mat)
            if påslag_ue > 0:
                markups.append(påslag_ue)
        
        if markups:
            analysis["average_markup"] = statistics.mean(markups)
        
        return analysis
    
    def compare_projects(self, project_names: List[str]) -> Dict[str, Any]:
        """Compare multiple projects based on their components."""
        comparison = {}
        
        for project_name in project_names:
            project_components = [c for c in self.components if c.get("source_file") == project_name]
            
            if project_components:
                comparison[project_name] = {
                    "component_count": len(project_components),
                    "total_cost": sum(c.get("Tilbud", 0) for c in project_components),
                    "total_labor_hours": sum(c.get("Timer", 0) for c in project_components),
                    "total_materials": sum(c.get("Materialer", 0) for c in project_components),
                    "categories": list(set(c.get("kategori", "") for c in project_components if c.get("kategori"))),
                    "trades_used": list(set(c.get("Fag", "") for c in project_components if c.get("Fag")))
                }
        
        return comparison
    
    def export_analysis(self, output_file: str, analysis_type: str = "summary") -> bool:
        """Export analysis results to a JSON file."""
        try:
            if analysis_type == "summary":
                data = self.get_summary_stats()
            elif analysis_type == "all":
                data = {
                    "summary": self.get_summary_stats(),
                    "components": self.components
                }
            else:
                print(f"Unknown analysis type: {analysis_type}")
                return False
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✓ Analysis exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error exporting analysis: {str(e)}")
            return False

def main():
    """Main function to demonstrate the analyzer."""
    print("Knowledge Base Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = KnowledgeBaseAnalyzer()
    
    if not analyzer.kb_data:
        print("Failed to load knowledge base. Exiting.")
        return
    
    # Get summary statistics
    print("\n📊 SUMMARY STATISTICS")
    print("-" * 30)
    stats = analyzer.get_summary_stats()
    
    print(f"Total Components: {stats['total_components']}")
    print(f"Total Files: {stats['total_files']}")
    print(f"Format Breakdown: {stats['format_breakdown']}")
    
    if stats['cost_ranges']:
        print(f"Cost Range: {stats['cost_ranges']['min']:.2f} - {stats['cost_ranges']['max']:.2f}")
        print(f"Average Cost: {stats['cost_ranges']['average']:.2f}")
    
    # Show top categories
    print("\n🏗️ TOP CATEGORIES")
    print("-" * 30)
    categories = sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:5]
    for category, count in categories:
        print(f"{category}: {count} components")
    
    # Show top trades
    print("\n🔧 TOP TRADES")
    print("-" * 30)
    trades = sorted(stats['trades'].items(), key=lambda x: x[1], reverse=True)[:5]
    for trade, count in trades:
        print(f"{trade}: {count} components")
    
    # Example searches
    print("\n🔍 EXAMPLE SEARCHES")
    print("-" * 30)
    
    # Find VVS components
    vvs_components = analyzer.search_components(kategori="VVS")
    print(f"VVS Components: {len(vvs_components)} found")
    
    # Find expensive components (>50,000)
    expensive_components = analyzer.search_components(min_cost=50000)
    print(f"Expensive Components (>50,000): {len(expensive_components)} found")
    
    # Find components with "badeværelse" in description
    bathroom_components = analyzer.search_components(search_text="badeværelse")
    print(f"Bathroom Components: {len(bathroom_components)} found")
    
    # Export summary analysis
    print("\n💾 EXPORTING ANALYSIS")
    print("-" * 30)
    analyzer.export_analysis("knowledge_base_summary.json", "summary")
    
    print("\n✅ Analysis complete! Use the exported files for further analysis.")

if __name__ == "__main__":
    main()
