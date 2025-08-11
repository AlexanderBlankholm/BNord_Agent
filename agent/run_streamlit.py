#!/usr/bin/env python3
"""
Simple launcher script for the Streamlit app
This makes it easy to start the web interface
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    print("🚀 Starting Construction Project Agent Streamlit App...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ Error: streamlit_app.py not found!")
        print("Please run this script from the 'agent' directory.")
        return
    
    # Check if Streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} is installed")
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("Installing Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit>=1.28.0"])
        print("✅ Streamlit installed successfully!")
    
    print("\n🌐 Starting web interface...")
    print("📱 The app will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:8501")
    print("\n⏹️  To stop the app, press Ctrl+C in this terminal")
    print("=" * 60)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()
