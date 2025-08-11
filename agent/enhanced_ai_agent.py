import os
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import sys

# Add the knowledge_base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'embeddings_and_search'))

# LangChain imports
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, AIMessage

# Import the existing search system
from semantic_search import SemanticSearch

@dataclass
class ProjectData:
    """Enhanced data structure to hold project information with cost details"""
    description: str = ""
    square_meters: float = 0.0
    selected_categories: List[str] = None
    category_tasks: Dict[str, List[str]] = None
    selected_components: Dict[str, List[Dict[str, Any]]] = None  # Store selected components with costs
    
    def __post_init__(self):
        if self.selected_categories is None:
            self.selected_categories = []
        if self.category_tasks is None:
            self.category_tasks = {}
        if self.selected_components is None:
            self.selected_components = {}

class EnhancedAIAgent:
    """Enhanced AI-powered agent using LangChain and OpenAI with knowledge base integration"""
    
    def __init__(self):
        self.project_data = ProjectData()
        self.categories = self.load_categories()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            temperature=0.1,  # Low temperature for consistent responses
            model="gpt-3.5-turbo"
        )
        
        # Initialize knowledge base search system with correct path
        # The search system needs to know where the knowledge base is located
        self.search_system = self._initialize_search_system()
        
        # Define enhanced tools
        self.tools = [
            Tool(
                name="SearchKnowledgeBase",
                func=self.search_knowledge_base,
                description="Search the construction knowledge base for components matching a task description. Use this to find relevant components with cost breakdowns."
            ),
            Tool(
                name="GetCategories",
                func=self.get_categories,
                description="Returns the list of available construction categories"
            ),
            Tool(
                name="SaveToExcel",
                func=self.save_to_excel,
                description="Saves the final project data to an Excel file with full cost breakdowns"
            )
        ]
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )
        
        # Create specialized prompts for different stages
        self.create_prompts()
    
    def load_categories(self) -> List[str]:
        """Load categories from JSON file"""
        try:
            with open("categories.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("categories", [])
        except FileNotFoundError:
            print("Warning: categories.json not found, using default categories")
            return ["nedrivning", "vvs", "elektrisk", "gulv", "vægge", "loft"]
    
    def create_prompts(self):
        """Create specialized prompts for different conversation stages"""
        
        # Initial project description prompt
        self.initial_prompt = PromptTemplate(
            input_variables=["chat_history"],
            template="""Du er en ekspert i byggeprojekter og badeværelsesrenovering. Din opgave er at hjælpe brugeren med at planlægge deres projekt.

{chat_history}

Du skal starte med at spørge om projektets beskrivelse. Stil spørgsmål på dansk og vær venlig og professionel.

Hvis brugeren allerede har beskrevet deres projekt, så spørg om yderligere detaljer som kvadratmeter."""
        )
        
        # Follow-up questions prompt
        self.followup_prompt = PromptTemplate(
            input_variables=["chat_history", "project_description"],
            template="""Baseret på projektbeskrivelsen: "{project_description}"

{chat_history}

Stil relevante opfølgende spørgsmål på dansk for at få mere information om projektet. 
Spørg specifikt om kvadratmeter og andre vigtige detaljer."""
        )
        
        # Category selection prompt
        self.category_prompt = PromptTemplate(
            input_variables=["chat_history", "categories"],
            template="""Her er de tilgængelige byggekategorier:

{categories}

{chat_history}

Præsenter disse kategorier for brugeren på dansk og hjælp dem med at vælge hvilke der er relevante for deres projekt.
Forklar kort hvad hver kategori indebærer."""
        )
        
        # Task gathering prompt with knowledge base integration
        self.task_prompt = PromptTemplate(
            input_variables=["chat_history", "category"],
            template="""Nu arbejder vi med kategorien: {category}

{chat_history}

Spørg brugeren om hvilke specifikke underopgaver der er nødvendige i denne kategori.
Giv eksempler på typiske opgaver for {category}.
Når brugeren beskriver en opgave, brug SearchKnowledgeBase værktøjet til at finde relevante komponenter med omkostninger.
Husk at spørge om der er flere opgaver før du går videre til næste kategori."""
        )
    
    def search_knowledge_base(self, query: str) -> str:
        """Tool function to search the knowledge base for components"""
        try:
            # Check if search system is available
            if not self.search_system:
                return f"⚠️ Søgesystemet er ikke tilgængeligt. Prøv at genstarte agenten."
            
            # Search for components matching the query
            results = self.search_system.search(query, top_k=5, min_similarity=0.2)
            
            if not results:
                return f"Ingen komponenter fundet for '{query}'. Prøv at beskrive opgaven mere specifikt."
            
            # Format results for the agent
            formatted_results = []
            for result in results:
                opgave = result.get('Opgave', 'N/A')
                kategori = result.get('kategori', 'N/A')
                tilbud = result.get('Tilbud', 0)
                kostpris_ep = result.get('Kostpris_EP', 0)
                materialer = result.get('Materialer', 0)
                timer = result.get('Timer', 0)
                takst = result.get('Takst', 0)
                similarity = result.get('similarity_score', 0)
                
                formatted_results.append(
                    f"• {opgave} ({kategori})\n"
                    f"  - Total pris: {tilbud:,.0f} DKK\n"
                    f"  - Kostpris EP: {kostpris_ep:,.0f} DKK\n"
                    f"  - Materialer: {materialer:,.0f} DKK\n"
                    f"  - Timer: {timer:.1f} | Takst: {takst:,.0f} DKK\n"
                    f"  - Lighedsscore: {similarity:.3f}"
                )
            
            return f"Fandt {len(results)} relevante komponenter for '{query}':\n\n" + "\n\n".join(formatted_results)
            
        except Exception as e:
            return f"Fejl ved søgning i videnbasen: {str(e)}"
    
    def get_categories(self) -> str:
        """Tool function to get available categories"""
        return f"Tilgængelige kategorier: {', '.join(self.categories)}"
    
    def save_to_excel(self, project_summary: str) -> str:
        """Enhanced tool function to save project data to Excel with full cost breakdowns"""
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, PatternFill
            
            # Create Excel file
            wb = Workbook()
            ws = wb.active
            ws.title = "Projekt Budget"
            
            # Enhanced headers with cost structure
            headers = [
                "Kategori", "Opgave", "Beskrivelse", "Kostpris_EP", "Materialer", 
                "Timer", "Takst", "Påslag_MAT", "Salgspris_MAT", "Påslag_UE", "Salgspris_UE", "Tilbud"
            ]
            
            # Style for headers
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")
            
            # Add project info
            ws.cell(row=2, column=1, value="PROJEKT INFO")
            ws.cell(row=3, column=1, value="Beskrivelse")
            ws.cell(row=3, column=2, value=self.project_data.description)
            ws.cell(row=4, column=1, value="Kvadratmeter")
            ws.cell(row=4, column=2, value=self.project_data.square_meters)
            
            # Add components with full cost breakdown
            current_row = 6
            total_cost = 0
            
            for category, components in self.project_data.selected_components.items():
                for component in components:
                    # Extract cost data from component
                    ws.cell(row=current_row, column=1, value=component.get('kategori', category))
                    ws.cell(row=current_row, column=2, value=component.get('Opgave', ''))
                    ws.cell(row=current_row, column=3, value=f"Komponent fra {component.get('source_file', 'videnbase')}")
                    ws.cell(row=current_row, column=4, value=component.get('Kostpris_EP', 0))
                    ws.cell(row=current_row, column=5, value=component.get('Materialer', 0))
                    ws.cell(row=current_row, column=6, value=component.get('Timer', 0))
                    ws.cell(row=current_row, column=7, value=component.get('Takst', 0))
                    ws.cell(row=current_row, column=8, value=component.get('Påslag_MAT', 0))
                    ws.cell(row=current_row, column=9, value=component.get('Salgspris_MAT', 0))
                    ws.cell(row=current_row, column=10, value=component.get('Påslag_UE', 0))
                    ws.cell(row=current_row, column=11, value=component.get('Salgspris_UE', 0))
                    ws.cell(row=current_row, column=12, value=component.get('Tilbud', 0))
                    
                    total_cost += component.get('Tilbud', 0)
                    current_row += 1
            
            # Add total row
            if current_row > 6:
                ws.cell(row=current_row, column=1, value="TOTAL")
                ws.cell(row=current_row, column=12, value=total_cost)
                
                # Style total row
                total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
                total_font = Font(bold=True)
                for col in range(1, 13):
                    cell = ws.cell(row=current_row, column=col)
                    cell.fill = total_fill
                    cell.font = total_font
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Save file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_projekt_budget_{timestamp}.xlsx"
            wb.save(filename)
            
            return f"Excel-fil gemt som: {filename} med total omkostning: {total_cost:,.0f} DKK"
            
        except Exception as e:
            return f"Fejl ved oprettelse af Excel-fil: {e}"
    
    def run_conversation(self):
        """Enhanced conversation loop using AI agent with knowledge base integration"""
        print("🤖 Hej! Jeg er din forbedrede AI-assistent til at planlægge dit byggeprojekt.")
        print("Jeg kan nu søge i videnbasen og give dig præcise omkostninger!")
        print("=" * 70)
        
        # Step 1: Get project description
        print("\n📝 **Trin 1: Projektbeskrivelse**")
        user_input = input("Beskriv dit projekt (f.eks. 'Total renovation af badeværelse'): ")
        self.project_data.description = user_input
        
        # Use AI to ask follow-up questions
        response = self.agent.run(f"Brugeren har beskrevet deres projekt som: {user_input}. Stil relevante opfølgende spørgsmål på dansk.")
        print(f"\n🤖 {response}")
        
        # Get square meters
        square_meters_input = input("Hvor mange kvadratmeter er der? (f.eks. 8.5): ")
        try:
            self.project_data.square_meters = float(square_meters_input)
        except ValueError:
            self.project_data.square_meters = 0.0
        
        # Step 2: Present categories with AI assistance
        print(f"\n🏗️ **Trin 2: Kategorier**")
        categories_text = "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(self.categories)])
        
        response = self.agent.run(f"Præsenter disse kategorier for brugeren og forklar hvilke der kunne være relevante for et projekt om: {self.project_data.description}")
        print(f"\n🤖 {response}")
        
        # User selects categories
        print(f"\n{categories_text}")
        selection = input("Indtast numrene på de relevante kategorier (adskilt med komma, f.eks. 1,3,5): ")
        
        try:
            selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
            self.project_data.selected_categories = [self.categories[idx] for idx in selected_indices if 0 <= idx < len(self.categories)]
        except ValueError:
            self.project_data.selected_categories = []
        
        # Step 3: AI-guided task gathering with knowledge base search
        print(f"\n🔨 **Trin 3: Opgaver for hver kategori med omkostninger**")
        
        for category in self.project_data.selected_categories:
            print(f"\n📋 **Kategori: {category}**")
            
            # Initialize components list for this category
            if category not in self.project_data.selected_components:
                self.project_data.selected_components[category] = []
            
            # Use AI to ask about tasks and search knowledge base
            response = self.agent.run(f"Spørg brugeren om hvilke specifikke opgaver der er nødvendige i kategorien '{category}' for et projekt om {self.project_data.description}. Når de beskriver en opgave, brug SearchKnowledgeBase værktøjet til at finde relevante komponenter.")
            print(f"\n🤖 {response}")
            
            tasks = []
            while True:
                task = input(f"Hvilke underopgaver er nødvendige i {category}? ")
                if task.strip():
                    tasks.append(task.strip())
                    
                    # Search knowledge base for this task
                    print(f"\n🔍 Søger i videnbasen efter: {task}")
                    search_result = self.search_knowledge_base(task)
                    print(f"\n{search_result}")
                    
                    # Ask user to select components
                    print(f"\nVil du tilføje komponenter fra søgeresultaterne til dit projekt? (ja/nej): ")
                    add_components = input().lower().strip()
                    
                    if add_components in ['ja', 'j', 'yes', 'y']:
                        # Add components from search results
                        if self.search_system:
                            search_results = self.search_system.search(task, top_k=3, min_similarity=0.2)
                            if search_results:
                                print(f"\nVælg komponenter at tilføje (indtast numre adskilt med komma, f.eks. 1,2):")
                                for i, result in enumerate(search_results, 1):
                                    opgave = result.get('Opgave', 'N/A')
                                    tilbud = result.get('Tilbud', 0)
                                    print(f"{i}. {opgave} - {tilbud:,.0f} DKK")
                                
                                selection = input("Vælg komponenter: ").strip()
                                try:
                                    selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
                                    for idx in selected_indices:
                                        if 0 <= idx < len(search_results):
                                            component = search_results[idx]
                                            self.project_data.selected_components[category].append(component)
                                            print(f"✅ Tilføjet: {component.get('Opgave', 'N/A')}")
                                except ValueError:
                                    print("Ugyldig valg, ingen komponenter tilføjet")
                            else:
                                print("Ingen komponenter fundet at tilføje")
                        else:
                            print("⚠️ Søgesystemet er ikke tilgængeligt")
                
                more = input("Er der andet du vil tilføje til denne kategori? (ja/nej): ").lower().strip()
                if more not in ['ja', 'j', 'yes', 'y']:
                    break
            
            self.project_data.category_tasks[category] = tasks
            print(f"✅ {len(tasks)} opgaver tilføjet til {category}")
        
        # Step 4: AI generates project summary and saves to Excel
        print(f"\n💾 **Trin 4: Gem til Excel med fuld omkostningsstruktur**")
        
        # Create project summary
        total_components = sum(len(components) for components in self.project_data.selected_components.values())
        total_cost = sum(
            sum(comp.get('Tilbud', 0) for comp in components)
            for components in self.project_data.selected_components.values()
        )
        
        summary = f"""
Projekt: {self.project_data.description}
Kvadratmeter: {self.project_data.square_meters} m²
Kategorier: {', '.join(self.project_data.selected_categories)}
Total opgaver: {sum(len(tasks) for tasks in self.project_data.category_tasks.values())}
Valgte komponenter: {total_components}
Total omkostning: {total_cost:,.0f} DKK
        """.strip()
        
        response = self.agent.run(f"Opret et sammendrag af projektet og brug SaveToExcel værktøjet til at gemme dataene med fuld omkostningsstruktur. Projekt sammendrag: {summary}")
        print(f"\n🤖 {response}")
        
        print(f"\n✅ Projektet er nu færdigt! Excel-filen er oprettet med fuld omkostningsstruktur.")

    def _initialize_search_system(self):
        """Initialize the search system with the correct knowledge base path"""
        try:
            # Get the path to the knowledge base
            kb_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', 'unified_knowledge_base.json')
            
            # Create a custom search system that knows the correct path
            from component_embeddings import ComponentEmbeddings
            
            # Create embeddings manager with correct path
            embeddings_manager = ComponentEmbeddings(knowledge_base_path=kb_path)
            
            # Create semantic search with the embeddings manager
            search_system = SemanticSearch(embeddings_manager=embeddings_manager)
            
            print(f"✓ Search system initialized with knowledge base: {kb_path}")
            return search_system
            
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize search system: {e}")
            print("Search functionality will be limited")
            return None

def main():
    """Main function to run the enhanced AI agent"""
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Fejl: OPENAI_API_KEY miljøvariabel er ikke sat.")
        print("Sæt venligst din OpenAI API nøgle før du kører denne agent.")
        return
    
    try:
        agent = EnhancedAIAgent()
        agent.run_conversation()
    except Exception as e:
        print(f"❌ Fejl under kørsel af agent: {e}")
        print("Sørg for at du har installeret alle nødvendige pakker: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
