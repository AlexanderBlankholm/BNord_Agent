# 🚀 Streamlit App Setup Guide

## ❌ **Package Conflict Issue Resolved!**

The error you encountered (`ModuleNotFoundError: No module named 'langchain'`) was due to package conflicts between your global Anaconda environment and the project dependencies.

## ✅ **Solution: Virtual Environment**

I've created a **virtual environment** specifically for this project that isolates all dependencies and prevents conflicts.

## 🔧 **Setup Instructions**

### **Option 1: Use the Virtual Environment (Recommended)**

1. **Navigate to the agent folder:**
   ```bash
   cd agent
   ```

2. **Activate the virtual environment:**
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # You should see (venv) in your prompt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

### **Option 2: Use the Launcher Scripts**

#### **Windows Batch File:**
```bash
# Double-click or run:
run_streamlit.bat
```

#### **PowerShell Script:**
```bash
# Right-click and "Run with PowerShell" or run:
.\run_streamlit.ps1
```

### **Option 3: Manual Launch (Advanced)**

1. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Verify packages are installed:**
   ```bash
   python -c "import langchain, streamlit, openai; print('✅ All packages available')"
   ```

3. **Launch Streamlit:**
   ```bash
   python -m streamlit run streamlit_app.py --server.port 8501
   ```

## 🌐 **Access the Web Interface**

Once running, the app will:
- **Automatically open** in your default browser
- **Or navigate to:** `http://localhost:8501`

## 📦 **What's in the Virtual Environment**

The virtual environment contains:
- ✅ **LangChain** - AI framework
- ✅ **OpenAI** - API client
- ✅ **Streamlit** - Web interface
- ✅ **Pandas** - Data manipulation
- ✅ **OpenPyXL** - Excel handling
- ✅ **All dependencies** - Properly isolated

## 🔍 **Troubleshooting**

### **If you still get import errors:**

1. **Make sure you're in the virtual environment:**
   ```bash
   # Should show (venv) in your prompt
   (venv) PS C:\...\agent>
   ```

2. **Reinstall packages if needed:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python path:**
   ```bash
   python -c "import sys; print(sys.executable)"
   # Should point to venv\Scripts\python.exe
   ```

### **If Streamlit won't start:**

1. **Check if port 8501 is free:**
   ```bash
   netstat -an | findstr 8501
   ```

2. **Try a different port:**
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

## 🎯 **Why This Happened**

- **Anaconda environment** had different package versions
- **Global pip** conflicted with conda packages
- **Virtual environment** isolates project dependencies
- **Clean installation** prevents version conflicts

## 🚀 **Quick Start (Copy-Paste)**

```bash
cd agent
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

## 📱 **What You'll See**

1. **Agent Selection** - Choose between Simple and AI agents
2. **Project Setup** - Follow the 8-step workflow
3. **AI Integration** - Get intelligent suggestions
4. **Excel Export** - Download professional budgets

## 🎉 **You're All Set!**

The virtual environment ensures:
- ✅ **No package conflicts**
- ✅ **Consistent dependencies**
- ✅ **Easy deployment**
- ✅ **Clean project isolation**

**Run the app and enjoy your AI-powered construction project agent!** 🏗️🤖
