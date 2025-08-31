# 🏗️ Construction Project Agent

A sophisticated AI-powered agent for construction project planning and budgeting, built with LangChain and OpenAI.

## 🚀 **NEW: Enhanced AI Agent with Quality-Aware RAG Pipeline**

The **Enhanced AI Agent** now features a sophisticated **Quality-Aware RAG** (Retrieval-Augmented Generation) pipeline that:

- **🤖 AI-Generated Components**: Automatically generates high-quality components based on user queries
- **🎯 Quality-First RAG**: Prioritizes high-quality pricing data by default, with smart fallback
- **🔍 Smart Context Selection**: Uses only reliable components for generation, ensuring realistic pricing
- **💰 Smart Pricing**: Inherits pricing structure from similar components in your knowledge base
- **📊 Professional Excel Output**: Detailed cost analysis with all fields preserved
- **🔍 Manual Backup**: Fallback to manual component selection when needed
- **⚙️ Quality Control Toggle**: User can choose between high-quality only or full database access

## 📁 **Agent Version**

### **Enhanced AI Agent** 🚀
- **File**: `enhanced_ai_agent.py`
- **Features**: Full RAG pipeline, quality control, AI-generated components
- **UI**: `enhanced_streamlit_app_fixed.py`
- **Status**: ✅ **Production Ready**

## 🎯 **Enhanced Agent Features**

### **Knowledge Base Integration**
- **633 Components**: Access to your complete validated component database
- **Semantic Search**: Find components using natural language descriptions
- **Cost Breakdowns**: Preserve all cost fields (Kostpris_EP, Materialer, Timer, Takst, Påslag, Salgspris)
- **Category Filtering**: Search within specific construction categories

### **RAG-Powered Workflow**
1. **Project Description**: User describes their construction project
2. **Category Selection**: Choose relevant construction categories
3. **Task Definition**: Describe specific tasks for each category
4. **AI Component Generation**: AI generates new components using RAG pipeline
5. **Component Review**: User reviews generated component with full cost breakdown
6. **Add to Project**: User approves and adds the AI-generated component
7. **Manual Backup**: Optional manual component selection for anything missed
8. **Excel Export**: Generate professional budget with full cost structure

### **How Quality-Aware RAG Works**
The Quality-Aware RAG pipeline combines:
- **Smart Retrieval**: Searches your knowledge base for similar components with quality filtering
- **Quality-First Context**: Prioritizes high-quality components (detailed pricing structure) by default
- **Intelligent Fallback**: Automatically falls back to broader database if no high-quality matches found
- **Generation**: Uses AI to create new components based on user queries + quality-filtered context
- **Pricing Inheritance**: Automatically calculates realistic pricing based on similar, reliable components
- **Quality Assurance**: Ensures generated components match your existing format and standards

### **Quality Control Features**
- **High-Quality Only Mode (Default)**: RAG uses only components with detailed pricing structure
- **Quality Toggle**: Users can override to include all components when needed
- **Transparency**: Clear indication of what data influenced generation and its quality level
- **Smart Fallback**: System never fails - automatically uses broader database when needed

### **Cost Structure Preservation**
The enhanced agent maintains the exact cost structure from your knowledge base:

| Field | Description | Example |
|-------|-------------|---------|
| `Kostpris_EP` | Cost price (Timer × Takst) | 2,040 DKK |
| `Materialer` | Material costs | 500 DKK |
| `Timer` | Labor hours | 4.0 |
| `Takst` | Hourly rate | 510 DKK |
| `Påslag_MAT` | Material markup | 100 DKK |
| `Salgspris_MAT` | Material sales price | 600 DKK |
| `Påslag_UE` | Subcontractor markup | 0 DKK |
| `Salgspris_UE` | Subcontractor sales price | 2,040 DKK |
| `Tilbud` | Total bid price | 2,640 DKK |

## 🛠️ **Setup & Installation**

### **1. Virtual Environment Setup**
```bash
# Navigate to agent directory
cd agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. OpenAI API Key**
```bash
# Set your OpenAI API key
$env:OPENAI_API_KEY="your_api_key_here"
```

### **3. Knowledge Base Access**
Ensure the knowledge base folder structure exists:
```
BNord_Agent/
├── agent/
│   ├── enhanced_ai_agent.py
│   └── enhanced_streamlit_app_fixed.py
└── knowledge_base/
    ├── unified_knowledge_base.json
    └── embeddings_and_search/
        ├── component_embeddings.pkl
        ├── semantic_search.py
        └── component_embeddings.py
```

### **4. Test RAG Functionality**
```bash
# Test the new RAG component generation
python test_rag_generation.py

# This will verify:
# - Search system connectivity
# - AI agent initialization
# - RAG component generation
# - Pricing structure inheritance
```

## 🚀 **Running the Enhanced Agent**

### **Command Line Interface**
```bash
# Activate virtual environment first
venv\Scripts\activate

# Run enhanced agent
python enhanced_ai_agent.py
```

### **Streamlit Web Interface** (Recommended)
```bash
# Activate virtual environment first
venv\Scripts\activate

# Run enhanced Streamlit app
streamlit run enhanced_streamlit_app_fixed.py
```

### **Quick Start**
```bash
# Navigate to agent directory
cd agent

# Activate virtual environment
venv\Scripts\activate

# Run the app
streamlit run enhanced_streamlit_app_fixed.py
```

## 🧪 **Testing**

### **Test Knowledge Base Integration**
```bash
# Test all components
python test_enhanced_agent.py
```

### **Test Individual Components**
```bash
# Test search system
python -c "from semantic_search import SemanticSearch; print('✅ Search system works')"

# Test enhanced agent
python -c "from enhanced_ai_agent import EnhancedAIAgent; print('✅ Enhanced agent works')"
```

## 📊 **Workflow Example**

### **User Input**
```
Project: "Total renovation af badeværelse"
Size: 8.5 m²
Categories: nedrivning, vvs, gulv
```

### **Task Definition**
```
nedrivning: "nedrivning af fliser på vægge"
vvs: "installation af nye vandhaner"
gulv: "lægning af nye fliser"
```

### **AI Search Results**
```
🔍 Found 3 relevant components for 'nedrivning af fliser på vægge':
• Fjerne vægstykker mellem entre og gang (nedrivning)
  - Total pris: 2,040 DKK
  - Kostpris EP: 2,040 DKK
  - Materialer: 0 DKK
  - Timer: 4.0 | Takst: 510 DKK
  - Lighedsscore: 0.856
```

### **Excel Output**
Professional Excel file with:
- **Project Information**: Description, size, categories
- **Component Details**: Full cost breakdowns for each selected component
- **Cost Analysis**: Material costs, labor hours, markups, total prices
- **Professional Formatting**: Styled headers, totals, auto-adjusted columns

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. ModuleNotFoundError: langchain**
```bash
# Solution: Activate virtual environment
venv\Scripts\activate
pip install -r requirements.txt
```

#### **2. Knowledge Base Not Found**
```bash
# Check file structure
ls ../knowledge_base/
# Ensure unified_knowledge_base.json exists
```

#### **3. Embeddings Not Found**
```bash
# The system will auto-generate embeddings on first run
# This may take a few minutes
```

#### **4. OpenAI API Errors**
```bash
# Check API key
echo $env:OPENAI_API_KEY
# Set if missing
$env:OPENAI_API_KEY="your_key_here"
```

### **Performance Tips**
- **First Run**: May be slower due to embedding generation
- **Subsequent Runs**: Fast semantic search through pre-generated embeddings
- **Memory Usage**: ~5MB for embeddings, ~300MB for knowledge base

## 📈 **Advanced Features**

### **Search Capabilities**
- **Semantic Matching**: Find components using natural language
- **Category Filtering**: Search within specific construction categories
- **Cost Range Filtering**: Find components within budget constraints
- **Similarity Scoring**: Rank results by relevance

### **Cost Optimization**
- **Alternative Suggestions**: Find similar components with different price points
- **Cost Analysis**: Break down total project costs by category
- **Budget Planning**: Estimate costs before component selection

### **Professional Output**
- **Excel Templates**: Industry-standard budget format
- **Cost Breakdowns**: Detailed analysis for client presentations
- **Project Summaries**: Comprehensive project overviews

## 🤝 **Contributing**

The enhanced agent is designed to be easily extensible:

- **New Search Methods**: Add to `semantic_search.py`
- **Additional Tools**: Extend the LangChain agent tools
- **UI Improvements**: Modify `enhanced_streamlit_app.py`
- **Cost Calculations**: Enhance Excel export functions

## 📚 **Dependencies**

- **LangChain**: AI agent framework
- **OpenAI**: GPT-3.5-turbo language model
- **Streamlit**: Web interface
- **OpenPyXL**: Excel file generation
- **NumPy**: Numerical operations for embeddings
- **Pandas**: Data manipulation

## 🎉 **What's New**

### **v2.0 - Enhanced Knowledge Base Integration**
- ✅ Semantic search through 633 components
- ✅ Full cost structure preservation
- ✅ AI-driven component selection
- ✅ Professional Excel output
- ✅ Enhanced Streamlit UI
- ✅ Comprehensive testing suite

### **v1.0 - Basic AI Agent**
- ✅ LangChain + OpenAI integration
- ✅ Basic conversation flow
- ✅ Simple Excel export

---

**Ready to revolutionize your construction project planning?** 🚀

Start with the Enhanced AI Agent for the full experience, or use the basic versions for simpler workflows.
