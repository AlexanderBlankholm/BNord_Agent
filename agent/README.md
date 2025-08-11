# Construction Project Agent

Two versions of a construction project planning agent - a simple Python version and an AI-powered LangChain version, now with a **Streamlit web interface**!

## 🚀 Quick Start

### **⚠️ IMPORTANT: Package Conflict Resolution**

If you get `ModuleNotFoundError: No module named 'langchain'`, use the **virtual environment**:

```bash
cd agent
.\venv\Scripts\Activate.ps1  # Activate virtual environment
streamlit run streamlit_app.py
```

**See `STREAMLIT_SETUP.md` for detailed setup instructions.**

### Option 1: Simple Agent (No AI, Works Offline)
```bash
cd agent
.\venv\Scripts\Activate.ps1  # Activate virtual environment first
python simple_agent.py
```

### Option 2: AI-Powered Agent (LangChain + OpenAI)
```bash
cd agent
.\venv\Scripts\Activate.ps1  # Activate virtual environment first
python ai_agent.py
```

### 🆕 Option 3: Streamlit Web Interface (Recommended!)
```bash
cd agent
.\venv\Scripts\Activate.ps1  # Activate virtual environment first
streamlit run streamlit_app.py
```

**Or use the launcher scripts:**
- **Windows:** Double-click `run_streamlit.bat`
- **PowerShell:** Right-click `run_streamlit.ps1` → "Run with PowerShell"

## 🌐 Streamlit Web Interface

The **Streamlit UI** provides a beautiful, interactive web interface that makes testing both agents incredibly easy:

### ✨ Features
- **Modern web interface** - No command line needed!
- **Interactive forms** - Easy input with validation
- **Real-time updates** - See changes immediately
- **Excel download** - One-click Excel export
- **Session persistence** - Your data stays while you work
- **Responsive design** - Works on desktop and mobile
- **Agent switching** - Toggle between Simple and AI agents

### 🎯 How to Use the Web Interface

1. **Choose your agent** - Simple (offline) or AI-powered
2. **Fill out the forms** - Step-by-step project planning
3. **Get AI assistance** - Smart suggestions and recommendations
4. **Download Excel** - Professional budget files ready to use

### 🖥️ Screenshots

The interface includes:
- **Project Description** - Text input with placeholders
- **Square Meters** - Number input with validation
- **Category Selection** - Checkboxes in organized columns
- **Task Management** - Add/remove tasks with delete buttons
- **AI Integration** - Buttons to get AI suggestions
- **Excel Export** - Download button with timestamped files

## 🔄 How It Works

Both agents follow the same 8-step workflow:

1. **Project Description** - User describes the project in Danish
2. **Follow-up Questions** - Agent asks for square meters
3. **Category Selection** - User selects relevant construction categories
4. **Task Gathering** - For each category, user specifies sub-tasks
5. **Excel Export** - All data is saved to a timestamped Excel file

## 📁 Files

- `simple_agent.py` - **Simple version**: Basic Python implementation, works offline
- `ai_agent.py` - **AI version**: LangChain + OpenAI integration for smarter conversations
- `streamlit_app.py` - **🌐 Web Interface**: Beautiful Streamlit UI for both agents
- `run_streamlit.py` - **Launcher**: Easy script to start the web interface
- `run_streamlit.bat` - **Windows Batch**: Double-click launcher
- `run_streamlit.ps1` - **PowerShell**: Advanced launcher with error handling
- `venv/` - **Virtual Environment**: Isolated dependencies (prevents conflicts)
- `categories.json` - Predefined construction categories
- `requirements.txt` - Python dependencies (includes Streamlit)
- `test_agent.py` - Test script for simple agent
- `test_ai_agent.py` - Test script for AI agent
- `STREAMLIT_SETUP.md` - **Setup Guide**: Resolves package conflicts

## 🤖 AI Agent Features

The **AI-powered version** (`ai_agent.py`) provides what Gemini suggested:

- **Intelligent follow-up questions** based on project description
- **Context-aware category explanations** tailored to your project
- **Smart task suggestions** with examples for each category
- **Natural language processing** for better user interaction
- **Conversation memory** to maintain context throughout the session
- **LangChain tools** for Excel export and category management
- **OpenAI GPT-3.5-turbo** for intelligent responses

## 🧪 Testing

### Test Simple Agent
```bash
cd agent
.\venv\Scripts\Activate.ps1
python test_agent.py
```

### Test AI Agent
```bash
cd agent
.\venv\Scripts\Activate.ps1
python test_ai_agent.py
```

### Test Web Interface
```bash
cd agent
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

## 💡 Example Session (AI Agent)

```
🤖 Hej! Jeg er din AI-assistent til at planlægge dit byggeprojekt.
Jeg vil stille dig spørgsmål på dansk og hjælpe dig med at strukturere dit projekt.
======================================================================

📝 **Trin 1: Projektbeskrivelse**
Beskriv dit projekt: Total renovation af badeværelse

🤖 Baseret på din beskrivelse af en total badeværelsesrenovering, vil jeg stille dig nogle relevante spørgsmål:

1. Hvor mange kvadratmeter er badeværelset?
2. Er det et helt nyt badeværelse eller en renovering af eksisterende?
3. Hvilke specifikke områder vil du gerne have fokus på?

Hvor mange kvadratmeter er der? 8.5

🏗️ **Trin 2: Kategorier**

🤖 For en badeværelsesrenovering på 8.5 m² vil jeg anbefale følgende kategorier:

1. nedrivning - Fjernelse af gamle materialer og installationer
2. vvs - Installation af nye rør og sanitære artikler
3. elektrisk - Opdatering af belysning og stikkontakter
4. gulv - Lægning af nye fliser eller andet gulvbelægning
5. vægge - Flisning eller anden vægbehandling
6. loft - Eventuel loftbehandling
7. tætning - Fugtisolering og tætning

Indtast numrene på de relevante kategorier: 1,2,4,5
```

## 🔧 Customization

- **Categories**: Edit `categories.json` to add/remove construction categories
- **AI Prompts**: Modify the prompt templates in `ai_agent.py` for different conversation styles
- **Excel Format**: Customize the Excel output in both agents
- **UI Styling**: Modify the CSS in `streamlit_app.py` for different looks
- **Language**: Change prompts to other languages if needed

## 🔑 OpenAI API Key

For the AI agent, you need to set your OpenAI API key:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows Command Prompt:**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

## 🎯 Next Steps for Enhancement

This gives you a **working foundation** that you can build upon:

1. **Integrate with Knowledge Base** - Connect to your `../knowledge_base/` components
2. **Add Cost Calculations** - Use your knowledge base to estimate prices
3. **Better UI** - Enhance the Streamlit interface with more features
4. **Template System** - Use different Excel templates for different project types
5. **Data Persistence** - Save projects to database
6. **User Authentication** - Add login system to the web interface

## ✅ What Makes This "Minimal but Working"

- **Two versions**: Simple offline version + AI-powered version
- **Web interface**: Beautiful Streamlit UI for easy testing
- **Virtual environment**: Prevents package conflicts
- **Same workflow**: Both implement your exact 8-step process
- **Immediate usability**: Run either version right now
- **Clear code**: Easy to understand and modify
- **Professional output**: Creates proper Excel files
- **Error handling**: Won't crash on invalid input
- **LangChain integration**: Uses the framework Gemini suggested

## 🎉 Ready to Use!

Choose the version that fits your needs:

- **Simple Agent** (`simple_agent.py`): Works offline, no API costs, immediate functionality
- **AI Agent** (`ai_agent.py`): Smarter conversations, better user experience, requires OpenAI API
- **🌐 Streamlit UI** (`streamlit_app.py`): Beautiful web interface for both agents

**The Streamlit UI is the easiest way to test and use both agents!** 

**🚀 Quick Launch:**
```bash
cd agent
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

All versions are **immediately functional** and follow your exact workflow! The AI version gives you the sophisticated agent that Gemini was describing, while the simple version provides a solid offline alternative. The Streamlit interface makes everything accessible through a beautiful web UI.
