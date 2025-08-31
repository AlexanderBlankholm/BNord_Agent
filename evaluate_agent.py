import json
import os
import sys
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import copy

# Add the agent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'knowledge_base', 'embeddings_and_search'))

from enhanced_ai_agent import EnhancedAIAgent
from semantic_search import SemanticSearch

@dataclass
class EvaluationResult:
    """Data structure to hold evaluation results"""
    test_case: int
    input_description: str
    ground_truth: Dict[str, float]
    generated_values: Dict[str, float]
    success: bool
    error_margin: float
    notes: str

class FilteredSemanticSearch:
    """Wrapper around SemanticSearch that filters out test set components"""
    
    def __init__(self, original_search_system: SemanticSearch, test_set_descriptions: List[str]):
        self.original_search = original_search_system
        self.test_set_descriptions = set(test_set_descriptions)
    
    def search(self, query: str, top_k: int = 5, min_similarity: float = 0.2, **kwargs) -> List[Dict[str, Any]]:
        """Search with filtering out test set components (ignores quality filtering during evaluation)"""
        # Get original results - ignore quality filtering during evaluation
        # We want to test the agent's generation capability with all available components
        original_results = self.original_search.search(query, top_k=top_k*2, min_similarity=min_similarity, min_quality_score=0.0)
        
        # Filter out test set components
        filtered_results = []
        for result in original_results:
            opgave = result.get('Opgave', '')
            if opgave not in self.test_set_descriptions:
                filtered_results.append(result)
                if len(filtered_results) >= top_k:
                    break
        
        return filtered_results

class AgentEvaluator:
    """Evaluates the agent's performance on the test set"""
    
    def __init__(self, test_set_path: str = 'test_set.json'):
        self.test_set_path = test_set_path
        self.test_set = self.load_test_set()
        self.results = []
        
        # Tolerance settings for evaluation
        self.tolerance_settings = {
            'Admin': 0.1,  # 10% tolerance
            'Timer': 0.2,  # 20% tolerance
            'Takst': 0.15,  # 15% tolerance
            'Kostpris_EP': 0.15,  # 15% tolerance
            'Materialer': 0.2,  # 20% tolerance
            'Påslag_MAT': 0.25,  # 25% tolerance
            'Salgspris_MAT': 0.2,  # 20% tolerance
            'UE': 0.2,  # 20% tolerance
            'Påslag_UE': 0.25,  # 25% tolerance
            'Salgspris_UE': 0.2,  # 20% tolerance
            'Tilbud': 0.15,  # 15% tolerance
        }
    
    def load_test_set(self) -> List[Tuple[str, Dict[str, float]]]:
        """Load the test set from JSON file"""
        try:
            with open(self.test_set_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [(item[0], item[1]) for item in data]
        except FileNotFoundError:
            print(f"Error: Test set file {self.test_set_path} not found")
            return []
    
    def create_filtered_agent(self) -> EnhancedAIAgent:
        """Create an agent with filtered search system"""
        # Create the original agent
        agent = EnhancedAIAgent()
        
        # Extract test set descriptions
        test_descriptions = [description for description, _ in self.test_set]
        
        # Create filtered search system
        if agent.search_system:
            filtered_search = FilteredSemanticSearch(agent.search_system, test_descriptions)
            agent.search_system = filtered_search
        
        return agent
    
    def compare_values(self, ground_truth: Dict[str, float], generated: Dict[str, float]) -> Tuple[bool, float, str]:
        """Compare generated values with ground truth"""
        total_error = 0
        field_errors = []
        all_fields_match = True
        
        for field, tolerance in self.tolerance_settings.items():
            if field not in ground_truth or field not in generated:
                continue
            
            gt_value = ground_truth[field]
            gen_value = generated[field]
            
            if gt_value == 0 and gen_value == 0:
                continue  # Both zero, perfect match
            
            if gt_value == 0:
                # Ground truth is zero, generated should be close to zero
                if abs(gen_value) > 100:  # Allow small non-zero values
                    all_fields_match = False
                    field_errors.append(f"{field}: GT=0, Gen={gen_value:.2f}")
            else:
                # Calculate relative error
                error = abs(gen_value - gt_value) / abs(gt_value)
                total_error += error
                
                if error > tolerance:
                    all_fields_match = False
                    field_errors.append(f"{field}: GT={gt_value:.2f}, Gen={gen_value:.2f}, Error={error:.2%}")
        
        avg_error = total_error / len(self.tolerance_settings) if total_error > 0 else 0
        notes = "; ".join(field_errors) if field_errors else "All fields within tolerance"
        
        return all_fields_match, avg_error, notes
    

    
    def evaluate_single_test(self, agent: EnhancedAIAgent, test_case: int, 
                           description: str, ground_truth: Dict[str, float]) -> EvaluationResult:
        """Evaluate a single test case"""
        print(f"\n--- Test Case {test_case}: {description[:50]}... ---")
        
        try:
            # Use the agent's actual generation method
            generated_component = agent.generate_component_with_rag(description, use_high_quality_only=True)
            
            # Check if generation was successful
            if "error" in generated_component:
                return EvaluationResult(
                    test_case=test_case,
                    input_description=description,
                    ground_truth=ground_truth,
                    generated_values={},
                    success=False,
                    error_margin=1.0,
                    notes=f"Generation error: {generated_component['error']}"
                )
            
            # Extract the relevant fields from the generated component
            generated_values = {
                'Admin': generated_component.get('Admin', 0.0),
                'Timer': generated_component.get('Timer', 0.0),
                'Takst': generated_component.get('Takst', 0.0),
                'Kostpris_EP': generated_component.get('Kostpris_EP', 0.0),
                'Materialer': generated_component.get('Materialer', 0.0),
                'Påslag_MAT': generated_component.get('Påslag_MAT', 0.0),
                'Salgspris_MAT': generated_component.get('Salgspris_MAT', 0.0),
                'UE': generated_component.get('UE', 0.0),
                'Påslag_UE': generated_component.get('Påslag_UE', 0.0),
                'Salgspris_UE': generated_component.get('Salgspris_UE', 0.0),
                'Tilbud': generated_component.get('Tilbud', 0.0)
            }
            
            # Compare with ground truth
            success, error_margin, notes = self.compare_values(ground_truth, generated_values)
            
            result = EvaluationResult(
                test_case=test_case,
                input_description=description,
                ground_truth=ground_truth,
                generated_values=generated_values,
                success=success,
                error_margin=error_margin,
                notes=notes
            )
            
            print(f"Success: {success}")
            print(f"Error Margin: {error_margin:.2%}")
            print(f"Generated Tilbud: {generated_values.get('Tilbud', 0):.2f}")
            print(f"Ground Truth Tilbud: {ground_truth.get('Tilbud', 0):.2f}")
            print(f"Notes: {notes}")
            
            return result
            
        except Exception as e:
            print(f"Error in test case {test_case}: {e}")
            return EvaluationResult(
                test_case=test_case,
                input_description=description,
                ground_truth=ground_truth,
                generated_values={},
                success=False,
                error_margin=1.0,
                notes=f"Error: {str(e)}"
            )
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run the complete evaluation"""
        print("🚀 Starting Agent Evaluation")
        print(f"📊 Test Set Size: {len(self.test_set)}")
        print("=" * 60)
        
        # Create filtered agent
        print("🔧 Creating filtered agent (excluding test set components)...")
        agent = self.create_filtered_agent()
        
        # Run evaluation
        successful_tests = 0
        total_error = 0
        
        for i, (description, ground_truth) in enumerate(self.test_set, 1):
            result = self.evaluate_single_test(agent, i, description, ground_truth)
            self.results.append(result)
            
            if result.success:
                successful_tests += 1
            
            total_error += result.error_margin
            
            # Add delay to avoid rate limiting
            time.sleep(1)
        
        # Calculate metrics
        success_rate = successful_tests / len(self.test_set) if self.test_set else 0
        avg_error = total_error / len(self.test_set) if self.test_set else 0
        
        evaluation_summary = {
            'total_tests': len(self.test_set),
            'successful_tests': successful_tests,
            'success_rate': success_rate,
            'average_error': avg_error,
            'results': self.results
        }
        
        return evaluation_summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print evaluation summary"""
        print("\n" + "=" * 60)
        print("📈 EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful Tests: {summary['successful_tests']}")
        print(f"Success Rate: {summary['success_rate']:.2%}")
        print(f"Average Error: {summary['average_error']:.2%}")
        
        print("\n📋 Detailed Results:")
        for result in summary['results']:
            status = "✅" if result.success else "❌"
            print(f"{status} Test {result.test_case}: {result.input_description[:40]}...")
            if not result.success:
                print(f"   Notes: {result.notes}")
    
    def save_results(self, summary: Dict[str, Any], filename: str = 'evaluation_results.json'):
        """Save evaluation results to file"""
        # Convert dataclass to dict for JSON serialization
        results_dict = []
        for result in summary['results']:
            results_dict.append({
                'test_case': result.test_case,
                'input_description': result.input_description,
                'ground_truth': result.ground_truth,
                'generated_values': result.generated_values,
                'success': result.success,
                'error_margin': result.error_margin,
                'notes': result.notes
            })
        
        output = {
            'summary': {
                'total_tests': summary['total_tests'],
                'successful_tests': summary['successful_tests'],
                'success_rate': summary['success_rate'],
                'average_error': summary['average_error']
            },
            'results': results_dict
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")

def main():
    """Main function to run the evaluation"""
    print("🤖 Agent Evaluation Script")
    print("This script evaluates the agent's performance on the test set")
    print("while ensuring the agent cannot access test set components in its RAG pipeline.")
    print()
    
    # Check if test set exists
    if not os.path.exists('test_set.json'):
        print("❌ Error: test_set.json not found!")
        print("Please run generate_test_set.py first to create the test set.")
        return
    
    # Run evaluation
    evaluator = AgentEvaluator()
    summary = evaluator.run_evaluation()
    
    # Print and save results
    evaluator.print_summary(summary)
    evaluator.save_results(summary)

if __name__ == "__main__":
    main()
