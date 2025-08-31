#!/usr/bin/env python3
"""
Simple test script to verify the evaluation works
"""

import json
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from evaluate_agent import AgentEvaluator

def test_evaluation():
    """Test the evaluation with a small subset"""
    print("🧪 Testing Agent Evaluation")
    
    # Check if test set exists
    if not os.path.exists('test_set.json'):
        print("❌ Error: test_set.json not found!")
        print("Please run generate_test_set.py first to create the test set.")
        return
    
    # Load test set and take first 3 items for testing
    with open('test_set.json', 'r', encoding='utf-8') as f:
        full_test_set = json.load(f)
    
    # Create a small test set for quick testing
    small_test_set = full_test_set[:3]
    
    # Save small test set temporarily
    with open('test_set_small.json', 'w', encoding='utf-8') as f:
        json.dump(small_test_set, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Testing with {len(small_test_set)} components")
    
    # Run evaluation with small test set
    evaluator = AgentEvaluator('test_set_small.json')
    summary = evaluator.run_evaluation()
    
    # Print results
    evaluator.print_summary(summary)
    
    # Clean up
    if os.path.exists('test_set_small.json'):
        os.remove('test_set_small.json')
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_evaluation()
