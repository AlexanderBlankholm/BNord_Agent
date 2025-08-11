# PowerShell script to launch the Construction Project Agent Streamlit App
Write-Host "🚀 Starting Construction Project Agent Streamlit App..." -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "streamlit_app.py")) {
    Write-Host "❌ Error: streamlit_app.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the 'agent' directory." -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if activation was successful
if (-not $env:VIRTUAL_ENV) {
    Write-Host "❌ Failed to activate virtual environment!" -ForegroundColor Red
    Read-Host "Press Enter to continue"
    exit 1
}

Write-Host "✅ Virtual environment activated: $env:VIRTUAL_ENV" -ForegroundColor Green

# Start Streamlit
Write-Host "🌐 Starting web interface..." -ForegroundColor Cyan
Write-Host "📱 The app will open in your browser automatically" -ForegroundColor White
Write-Host "🔗 If it doesn't open, go to: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "⏹️  To stop the app, press Ctrl+C in this terminal" -ForegroundColor Yellow
Write-Host "===========================================================" -ForegroundColor Cyan

try {
    & ".\venv\Scripts\streamlit.exe" run streamlit_app.py --server.port 8501 --server.address localhost
} catch {
    Write-Host "❌ Error running Streamlit: $_" -ForegroundColor Red
    Write-Host "Trying alternative method..." -ForegroundColor Yellow
    python -m streamlit run streamlit_app.py --server.port 8501 --server.address localhost
}

Read-Host "Press Enter to continue"
