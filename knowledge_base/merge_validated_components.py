import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import glob

class ValidatedComponentsMerger:
    """
    Merger for validated components JSON files into a single unified knowledge base.
    Standardizes data schema and calculates missing values for consistency.
    """
    
    def __init__(self):
        self.unified_schema = {
            "kategori": "",
            "Opgave": "",
            "Fag": "",
            "Admin": 0.0,
            "Timer": 0.0,
            "Takst": 0.0,
            "Kostpris_EP": 0.0,
            "Materialer": 0.0,
            "Påslag_MAT": 0.0,
            "Salgspris_MAT": 0.0,
            "UE": 0.0,
            "Påslag_UE": 0.0,
            "Salgspris_UE": 0.0,
            "Tilbud": 0.0,
            "source_file": "",
            "original_format": ""
        }
        
        self.merged_components = []
        self.processing_stats = {
            "total_files": 0,
            "processed_files": 0,
            "total_components": 0,
            "format_old": 0,
            "format_new": 0,
            "errors": []
        }
    
    def load_json_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            error_msg = f"Error loading {file_path}: {str(e)}"
            self.processing_stats["errors"].append(error_msg)
            print(f"✗ {error_msg}")
            return None
    
    def detect_format(self, data: Any) -> str:
        """Detect the format of the JSON data."""
        if isinstance(data, list):
            # Check if it's the new format (list of components)
            if data and isinstance(data[0], dict):
                if "Kostpris_EP" in data[0] and "Påslag_MAT" in data[0]:
                    return "new"
        elif isinstance(data, dict):
            # Check if it's the old format (with metadata and components)
            if "components" in data and "metadata" in data:
                if data["components"] and isinstance(data["components"][0], dict):
                    if "kostpris" in data["components"][0] and "Påslag" in data["components"][0]:
                        return "old"
        
        return "unknown"
    
    def map_new_format(self, component: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """Map new format component to unified schema."""
        mapped = self.unified_schema.copy()
        
        # Direct mapping for new format
        mapped.update({
            "kategori": component.get("kategori", ""),
            "Opgave": component.get("Opgave", ""),
            "Fag": component.get("Fag", ""),
            "Admin": float(component.get("Admin", 0)),
            "Timer": float(component.get("Timer", 0)),
            "Takst": float(component.get("Takst", 0)),
            "Kostpris_EP": float(component.get("Kostpris_EP", 0)),
            "Materialer": float(component.get("Materialer", 0)),
            "Påslag_MAT": float(component.get("Påslag_MAT", 0)),
            "Salgspris_MAT": float(component.get("Salgspris_MAT", 0)),
            "UE": float(component.get("UE", 0)),
            "Påslag_UE": float(component.get("Påslag_UE", 0)),
            "Salgspris_UE": float(component.get("Salgspris_UE", 0)),
            "Tilbud": float(component.get("Tilbud", 0)),
            "source_file": source_file,
            "original_format": "new"
        })
        
        return mapped
    
    def map_old_format(self, component: Dict[str, Any], source_file: str) -> Dict[str, Any]:
        """Map old format component to unified schema with calculated values."""
        mapped = self.unified_schema.copy()
        
        # Extract basic fields
        timer = float(component.get("Timer", 0))
        takst = float(component.get("Takst", 0))
        materialer = float(component.get("Materialer", 0))
        kostpris = float(component.get("kostpris", 0))
        påslag = float(component.get("Påslag", 0))
        tilbud = float(component.get("Tilbud", 0))
        
        # Calculate Kostpris_EP (Timer * Takst)
        kostpris_ep = timer * takst if timer > 0 and takst > 0 else kostpris
        
        # Determine if this is primarily labor or materials
        is_labor_dominant = timer > 0 and takst > 0
        is_material_dominant = materialer > 0 and timer == 0
        
        # Calculate material-related fields
        påslag_mat = påslag if is_material_dominant else 0.0
        salgspris_mat = materialer * (1 + påslag_mat / 100) if påslag_mat > 0 else materialer
        
        # Calculate UE (subcontractor) fields
        # If kostpris_ep > 0 and not material dominant, assume it's UE
        ue = kostpris_ep if is_labor_dominant and not is_material_dominant else 0.0
        påslag_ue = påslag if is_labor_dominant and not is_material_dominant else 0.0
        salgspris_ue = ue * (1 + påslag_ue / 100) if påslag_ue > 0 else ue
        
        # Admin field - try to extract from existing data or estimate
        admin = float(component.get("Admin", 0))
        
        mapped.update({
            "kategori": component.get("kategori", ""),
            "Opgave": component.get("Opgave", ""),
            "Fag": component.get("Fag", ""),
            "Admin": admin,
            "Timer": timer,
            "Takst": takst,
            "Kostpris_EP": kostpris_ep,
            "Materialer": materialer,
            "Påslag_MAT": påslag_mat,
            "Salgspris_MAT": salgspris_mat,
            "UE": ue,
            "Påslag_UE": påslag_ue,
            "Salgspris_UE": salgspris_ue,
            "Tilbud": tilbud,
            "source_file": source_file,
            "original_format": "old"
        })
        
        return mapped
    
    def process_file(self, file_path: str) -> bool:
        """Process a single JSON file and add components to the merged list."""
        print(f"Processing: {Path(file_path).name}")
        
        # Load the JSON file
        data = self.load_json_file(file_path)
        if not data:
            return False
        
        # Detect format
        format_type = self.detect_format(data)
        print(f"  Detected format: {format_type}")
        
        if format_type == "unknown":
            error_msg = f"Unknown format in {file_path}"
            self.processing_stats["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
            return False
        
        # Extract components based on format
        components = []
        if format_type == "new":
            components = data  # Direct list of components
            self.processing_stats["format_new"] += 1
        elif format_type == "old":
            components = data.get("components", [])
            self.processing_stats["format_old"] += 1
        
        # Process each component
        processed_count = 0
        for component in components:
            if not isinstance(component, dict):
                continue
                
            try:
                if format_type == "new":
                    mapped_component = self.map_new_format(component, Path(file_path).stem)
                else:
                    mapped_component = self.map_old_format(component, Path(file_path).stem)
                
                self.merged_components.append(mapped_component)
                processed_count += 1
                
            except Exception as e:
                error_msg = f"Error processing component in {file_path}: {str(e)}"
                self.processing_stats["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")
                continue
        
        print(f"  ✓ Processed {processed_count} components")
        self.processing_stats["total_components"] += processed_count
        self.processing_stats["processed_files"] += 1
        
        return True
    
    def merge_all_files(self, input_dir: str, output_file: str) -> Dict[str, Any]:
        """Merge all JSON files in the input directory into a single knowledge base."""
        print(f"Starting merge of validated components...")
        print(f"Input directory: {input_dir}")
        print(f"Output file: {output_file}")
        print("=" * 60)
        
        # Get list of JSON files
        json_files = glob.glob(os.path.join(input_dir, "*.json"))
        self.processing_stats["total_files"] = len(json_files)
        
        print(f"Found {len(json_files)} JSON files to process")
        print()
        
        # Process each file
        for json_file in json_files:
            self.process_file(json_file)
            print()
        
        # Create the unified knowledge base
        knowledge_base = {
            "metadata": {
                "total_files_processed": self.processing_stats["processed_files"],
                "total_components": self.processing_stats["total_components"],
                "format_breakdown": {
                    "new_format": self.processing_stats["format_new"],
                    "old_format": self.processing_stats["format_old"]
                },
                "processing_errors": len(self.processing_stats["errors"]),
                "schema_version": "1.0",
                "description": "Unified knowledge base of construction project components"
            },
            "components": self.merged_components
        }
        
        # Save the merged knowledge base
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_base, f, indent=2, ensure_ascii=False, default=str)
            
            print("=" * 60)
            print("MERGE COMPLETE")
            print("=" * 60)
            print(f"Total files: {self.processing_stats['total_files']}")
            print(f"Successfully processed: {self.processing_stats['processed_files']}")
            print(f"Total components: {self.processing_stats['total_components']}")
            print(f"New format files: {self.processing_stats['format_new']}")
            print(f"Old format files: {self.processing_stats['format_old']}")
            print(f"Errors: {len(self.processing_stats['errors'])}")
            print(f"Output saved to: {output_file}")
            
            if self.processing_stats["errors"]:
                print("\nErrors encountered:")
                for error in self.processing_stats["errors"]:
                    print(f"  - {error}")
            
        except Exception as e:
            error_msg = f"Error saving merged knowledge base: {str(e)}"
            print(f"✗ {error_msg}")
            return {"error": error_msg}
        
        return {
            "success": True,
            "output_file": output_file,
            "stats": self.processing_stats
        }

def main():
    """Main function to run the merger."""
    # Initialize merger
    merger = ValidatedComponentsMerger()
    
    # Set input and output paths
    input_directory = "real_examples/validated_components"
    output_file = "unified_knowledge_base.json"
    
    # Merge all files
    result = merger.merge_all_files(input_directory, output_file)
    
    return result

if __name__ == "__main__":
    main()
