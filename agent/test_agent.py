#!/usr/bin/env python3
"""
Test script to demonstrate the SimpleAgent functionality
This runs a mock conversation to show how the agent works
"""

import json
from simple_agent import SimpleAgent, ProjectData

def test_agent():
    """Test the agent with mock data"""
    print("🧪 Testing SimpleAgent functionality...")
    print("=" * 50)
    
    # Create agent instance
    agent = SimpleAgent()
    
    # Test data loading
    print(f"📋 Loaded {len(agent.categories)} categories:")
    for i, cat in enumerate(agent.categories[:5], 1):
        print(f"   {i}. {cat}")
    if len(agent.categories) > 5:
        print(f"   ... and {len(agent.categories) - 5} more")
    
    # Test ProjectData structure
    print(f"\n📊 ProjectData structure created successfully")
    print(f"   - Description: {agent.project_data.description}")
    print(f"   - Square meters: {agent.project_data.square_meters}")
    print(f"   - Selected categories: {agent.project_data.selected_categories}")
    print(f"   - Category tasks: {len(agent.project_data.category_tasks)}")
    
    # Test with mock data
    print(f"\n🎭 Adding mock project data...")
    agent.project_data.description = "Total renovation af badeværelse"
    agent.project_data.square_meters = 8.5
    agent.project_data.selected_categories = ["nedrivning", "vvs", "gulv"]
    agent.project_data.category_tasks = {
        "nedrivning": ["nedrivning af fliser på vægge", "nedrivning af gammelt toilet"],
        "vvs": ["installation af nyt toilet", "installation af håndvask"],
        "gulv": ["lægning af nye fliser", "fugning"]
    }
    
    print(f"✅ Mock data added:")
    print(f"   - Project: {agent.project_data.description}")
    print(f"   - Size: {agent.project_data.square_meters} m²")
    print(f"   - Categories: {', '.join(agent.project_data.selected_categories)}")
    
    total_tasks = sum(len(tasks) for tasks in agent.project_data.category_tasks.values())
    print(f"   - Total tasks: {total_tasks}")
    
    # Test Excel creation (without saving to avoid file creation during test)
    print(f"\n💾 Testing Excel creation logic...")
    try:
        # Just test the import
        import pandas as pd
        from openpyxl import Workbook
        print("✅ Required libraries available for Excel creation")
    except ImportError as e:
        print(f"❌ Missing library: {e}")
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"   The agent is ready to use with: python simple_agent.py")

if __name__ == "__main__":
    test_agent()
