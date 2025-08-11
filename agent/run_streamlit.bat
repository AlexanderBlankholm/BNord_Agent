@echo off
echo 🚀 Starting Construction Project Agent Streamlit App...
echo ============================================================

REM Check if we're in the right directory
if not exist "streamlit_app.py" (
    echo ❌ Error: streamlit_app.py not found!
    echo Please run this script from the 'agent' directory.
    pause
    exit /b 1
)

REM Activate virtual environment and run Streamlit
echo 🌐 Starting web interface...
echo 📱 The app will open in your browser automatically
echo 🔗 If it doesn't open, go to: http://localhost:8501
echo.
echo ⏹️  To stop the app, press Ctrl+C in this terminal
echo ============================================================

call venv\Scripts\activate.bat
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

pause
