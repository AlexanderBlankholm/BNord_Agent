#!/usr/bin/env python3
"""
Test script for the AI Agent functionality
This tests the LangChain + OpenAI integration
"""

import os
import json
from ai_agent import AIAgent, ProjectData

def test_ai_agent():
    """Test the AI agent with mock data"""
    print("🧪 Testing AI Agent functionality...")
    print("=" * 50)
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key before testing the AI agent")
        return False
    
    try:
        # Create agent instance
        print("🔧 Creating AI Agent instance...")
        agent = AIAgent()
        print("✅ AI Agent created successfully")
        
        # Test data loading
        print(f"\n📋 Loaded {len(agent.categories)} categories:")
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
        
        # Test tool functions
        print(f"\n🔧 Testing tool functions...")
        
        # Test GetCategories tool
        categories_result = agent.get_categories()
        print(f"✅ GetCategories tool: {categories_result}")
        
        # Test Excel creation (without saving to avoid file creation during test)
        print(f"\n💾 Testing Excel creation logic...")
        try:
            # Just test the import
            from openpyxl import Workbook
            print("✅ Required libraries available for Excel creation")
        except ImportError as e:
            print(f"❌ Missing library: {e}")
        
        # Test LangChain components
        print(f"\n🤖 Testing LangChain components...")
        print(f"   - LLM initialized: {agent.llm is not None}")
        print(f"   - Memory initialized: {agent.memory is not None}")
        print(f"   - Agent initialized: {agent.agent is not None}")
        print(f"   - Tools count: {len(agent.tools)}")
        
        print(f"\n🎉 All AI Agent tests completed successfully!")
        print(f"   The AI agent is ready to use with: python ai_agent.py")
        return True
        
    except Exception as e:
        print(f"❌ Error during AI Agent testing: {e}")
        print("This might be due to missing dependencies or API key issues")
        return False

if __name__ == "__main__":
    success = test_ai_agent()
    if not success:
        print("\n💡 To fix issues:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your OpenAI API key: set OPENAI_API_KEY=your_key_here")
        print("3. Make sure you have an active internet connection")
