import json
import random

def generate_test_set():
    """
    Generate a test set of 50 random components from the knowledge base
    where original_format is "new"
    """
    
    # Load the knowledge base
    with open('knowledge_base/unified_knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter components with original_format "new"
    new_format_components = [
        comp for comp in data['components'] 
        if comp.get('original_format') == 'new'
    ]
    
    print(f"Found {len(new_format_components)} components with original_format 'new'")
    
    # Randomly select 50 components
    random.seed(42)  # For reproducibility
    selected_components = random.sample(new_format_components, 50)
    
    # Create test set in the required format
    test_set = []
    
    for i, component in enumerate(selected_components):
        # Extract the relevant fields for the test set
        test_component = {
            "Admin": component.get("Admin", 0.0),
            "Timer": component.get("Timer", 0.0),
            "Takst": component.get("Takst", 0.0),
            "Kostpris_EP": component.get("Kostpris_EP", 0.0),
            "Materialer": component.get("Materialer", 0.0),
            "Påslag_MAT": component.get("Påslag_MAT", 0.0),
            "Salgspris_MAT": component.get("Salgspris_MAT", 0.0),
            "UE": component.get("UE", 0.0),
            "Påslag_UE": component.get("Påslag_UE", 0.0),
            "Salgspris_UE": component.get("Salgspris_UE", 0.0),
            "Tilbud": component.get("Tilbud", 0.0)
        }
        
        # Create tuple with Opgave field value and component data
        test_tuple = (component.get("Opgave", "random_string"), test_component)
        test_set.append(test_tuple)
        
        # Print some info about the selected component
        print(f"Test {i+1}: {component.get('kategori', 'N/A')} - {component.get('Opgave', 'N/A')} (Tilbud: {component.get('Tilbud', 0)})")
    
    return test_set

def save_test_set(test_set, filename='test_set.json'):
    """Save the test set to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(test_set, f, indent=2, ensure_ascii=False)
    print(f"\nTest set saved to {filename}")

def print_test_set_summary(test_set):
    """Print a summary of the test set"""
    print(f"\nTest Set Summary:")
    print(f"Total test cases: {len(test_set)}")
    
    # Calculate some statistics
    tilbud_values = [item[1]["Tilbud"] for item in test_set]
    admin_values = [item[1]["Admin"] for item in test_set]
    timer_values = [item[1]["Timer"] for item in test_set]
    
    print(f"Tilbud range: {min(tilbud_values):.2f} - {max(tilbud_values):.2f}")
    print(f"Admin range: {min(admin_values):.2f} - {max(admin_values):.2f}")
    print(f"Timer range: {min(timer_values):.2f} - {max(timer_values):.2f}")
    
    # Count non-zero values
    non_zero_tilbud = sum(1 for v in tilbud_values if v > 0)
    non_zero_admin = sum(1 for v in admin_values if v > 0)
    non_zero_timer = sum(1 for v in timer_values if v > 0)
    
    print(f"Components with non-zero Tilbud: {non_zero_tilbud}")
    print(f"Components with non-zero Admin: {non_zero_admin}")
    print(f"Components with non-zero Timer: {non_zero_timer}")

if __name__ == "__main__":
    # Generate the test set
    test_set = generate_test_set()
    
    # Print summary
    print_test_set_summary(test_set)
    
    # Save to file
    save_test_set(test_set)
    
    # Also save as Python list for easy copy-paste
    with open('test_set_python.py', 'w', encoding='utf-8') as f:
        f.write("# Test set for agent evaluation\n")
        f.write("# Generated from knowledge base components with original_format 'new'\n\n")
        f.write("test_set = [\n")
        for i, (placeholder, component) in enumerate(test_set):
            f.write(f"    (\"{placeholder}\", {component}),  # Test {i+1}\n")
        f.write("]\n")
    
    print("Test set also saved as Python list in test_set_python.py")
