#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
Run this to check if the virtual environment is working
"""

print("🧪 Testing Streamlit App Imports...")
print("=" * 50)

try:
    print("1. Testing basic imports...")
    import os
    import json
    from datetime import datetime
    print("   ✅ Basic imports successful")
    
    print("2. Testing LangChain imports...")
    from langchain.agents import initialize_agent, AgentType, Tool
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.memory import ConversationBufferMemory
    print("   ✅ LangChain imports successful")
    
    print("3. Testing Streamlit import...")
    import streamlit as st
    print(f"   ✅ Streamlit {st.__version__} import successful")
    
    print("4. Testing AI Agent import...")
    from ai_agent import AIAgent
    print("   ✅ AI Agent import successful")
    
    print("5. Testing Simple Agent import...")
    from simple_agent import SimpleAgent, ProjectData
    print("   ✅ Simple Agent import successful")
    
    print("6. Testing Streamlit app import...")
    from streamlit_app import load_categories
    categories = load_categories()
    print(f"   ✅ Streamlit app import successful - {len(categories)} categories loaded")
    
    print("\n🎉 All imports successful! Your virtual environment is working correctly.")
    print("You can now run: streamlit run streamlit_app.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 This means the virtual environment is not active or packages are missing.")
    print("Make sure you:")
    print("1. Are in the 'agent' directory")
    print("2. Have activated the virtual environment: .\\venv\\Scripts\\Activate.ps1")
    print("3. Have installed packages: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("Please check your setup and try again.")
