#!/usr/bin/env python3
"""
Launcher script for the Enhanced Construction Project Agent Streamlit App.
This app integrates with the knowledge base search system for intelligent component selection.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Enhanced Construction Project Agent Streamlit App...")
    print("=" * 70)
    
    # Check if enhanced_streamlit_app.py exists
    if not os.path.exists("enhanced_streamlit_app.py"):
        print("❌ Error: enhanced_streamlit_app.py not found!")
        print("Make sure you're running this from the agent directory.")
        return
    
    # Check if knowledge base exists
    kb_path = os.path.join("..", "knowledge_base", "unified_knowledge_base.json")
    if not os.path.exists(kb_path):
        print("❌ Error: Knowledge base not found!")
        print(f"Expected path: {kb_path}")
        print("Make sure the knowledge_base folder exists with unified_knowledge_base.json")
        return
    
    # Check if embeddings exist
    embeddings_path = os.path.join("..", "knowledge_base", "embeddings_and_search", "component_embeddings.pkl")
    if not os.path.exists(embeddings_path):
        print("⚠️ Warning: Embeddings not found!")
        print(f"Expected path: {embeddings_path}")
        print("The app will generate embeddings on first run, which may take a moment.")
    
    # Check if virtual environment is activated
    if not os.getenv("VIRTUAL_ENV"):
        print("⚠️ Warning: Virtual environment not detected!")
        print("It's recommended to activate the virtual environment first:")
        print("  Windows: .\\venv\\Scripts\\activate")
        print("  Linux/Mac: source venv/bin/activate")
        print()
        print("Continuing anyway...")
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Warning: OPENAI_API_KEY not set!")
        print("The AI features won't work without an OpenAI API key.")
        print("Set it with: $env:OPENAI_API_KEY='your_key_here'")
        print()
        print("Continuing anyway...")
    
    print("\n✅ All checks passed! Starting Streamlit app...")
    print("🌐 The app will open in your browser at: http://localhost:8501")
    print("📱 You can also access it from other devices on your network")
    print("\n" + "=" * 70)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "enhanced_streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Streamlit app stopped by user")
    except Exception as e:
        print(f"\n❌ Error running Streamlit: {e}")
        print("Try running manually: streamlit run enhanced_streamlit_app.py")

if __name__ == "__main__":
    main()
