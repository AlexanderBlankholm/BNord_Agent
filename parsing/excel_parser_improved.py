import pandas as pd
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np

class ImprovedExcelComponentParser:
    """
    Improved parser for Excel files containing construction project components and pricing.
    Based on analysis of processed files, this parser can better extract component information
    with proper column mapping and categorization.
    """
    
    def __init__(self):
        self.processed_files = []
        self.errors = []
        
    def parse_excel_file(self, file_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Parse a single Excel file and extract component information.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of dictionaries containing component information, or None if parsing fails
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Clean and process the dataframe
            processed_df = self._clean_dataframe(df)
            
            # Extract components
            components = self._extract_components(processed_df)
            
            # Add metadata
            metadata = self._extract_metadata(file_path, processed_df)
            
            # Combine components with metadata
            result = {
                "metadata": metadata,
                "components": components
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error parsing {file_path}: {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            return None
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare the dataframe for processing."""
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Fill NaN values with appropriate defaults
        df = df.fillna(np.nan)
        
        return df
    
    def _extract_metadata(self, file_path: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract metadata from the Excel file."""
        filename = Path(file_path).stem
        
        # Try to extract date from filename
        date_match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', filename)
        date = None
        if date_match:
            date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        
        # Try to extract project name from filename
        project_name = filename.replace('_', ' ').replace('-', ' ')
        
        # Look for project information in the first few rows
        project_info = None
        for i in range(min(10, len(df))):
            for col in df.columns:
                cell_value = str(df.iloc[i, df.columns.get_loc(col)])
                if 'tilbud' in cell_value.lower() or 'budget' in cell_value.lower():
                    project_info = cell_value
                    break
            if project_info:
                break
        
        return {
            "filename": filename,
            "date": date,
            "project_name": project_name,
            "project_info": project_info,
            "total_rows": len(df),
            "total_columns": len(df.columns)
        }
    
    def _extract_components(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract component information from the dataframe."""
        components = []
        current_category = "Unknown"
        category_total = 0
        
        # First pass: identify categories and their totals
        categories = self._identify_categories(df)
        
        for idx, row in df.iterrows():
            component = self._extract_single_component(row, idx, categories)
            
            if component:
                components.append(component)
        
        return components
    
    def _identify_categories(self, df: pd.DataFrame) -> Dict[str, float]:
        """Identify categories and their totals from the dataframe."""
        categories = {}
        current_category = "Unknown"
        
        for idx, row in df.iterrows():
            # Check if this row indicates a new category
            if self._is_category_header(row):
                current_category = self._extract_category_name(row)
                category_total = self._extract_category_total(row)
                categories[current_category] = category_total
        
        return categories
    
    def _extract_single_component(self, row: pd.Series, row_idx: int, categories: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """Extract information for a single component row."""
        # Skip header rows and empty rows
        if self._is_header_row(row) or self._is_empty_row(row):
            return None
        
        # Skip category header rows
        if self._is_category_header(row):
            return None
        
        component = {}
        
        # Extract task description (usually in first few columns)
        task_description = self._extract_task_description(row)
        if not task_description:
            return None
        
        component["Opgave"] = task_description
        
        # Determine which category this component belongs to
        category, category_total = self._determine_component_category(row, categories)
        component["kategori"] = category
        component["kategori_total"] = category_total
        
        # Extract various fields based on column position and content
        component.update(self._extract_pricing_fields(row))
        component.update(self._extract_labor_fields(row))
        component.update(self._extract_material_fields(row))
        component.update(self._extract_supplier_fields(row))
        component.update(self._extract_additional_fields(row))
        
        # Add row index for reference
        component["row_index"] = row_idx
        
        return component
    
    def _determine_component_category(self, row: pd.Series, categories: Dict[str, float]) -> tuple:
        """Determine which category a component belongs to based on its position."""
        # This is a simplified approach - in practice, you might need more sophisticated logic
        # For now, we'll use the first category as default
        if categories:
            first_category = list(categories.keys())[0]
            return first_category, categories[first_category]
        return "Unknown", 0.0
    
    def _is_header_row(self, row: pd.Series) -> bool:
        """Check if a row is a header row."""
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).lower()
                if any(keyword in cell_str for keyword in ['tilbud', 'budget', 'dato', 'projekt', 'kategori', 'påslag', 'timer', 'takst']):
                    return True
        return False
    
    def _is_empty_row(self, row: pd.Series) -> bool:
        """Check if a row is essentially empty."""
        return all(pd.isna(cell) or str(cell).strip() == '' for cell in row)
    
    def _is_category_header(self, row: pd.Series) -> bool:
        """Check if a row indicates a new category."""
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).lower()
                if any(keyword in cell_str for keyword in ['rum', 'værelse', 'badeværelse', 'køkken', 'gang', 'projektledelse', 'nedrivning', 'murer', 'tømrer', 'snedker', 'vvs', 'el', 'maler']):
                    return True
        return False
    
    def _extract_category_name(self, row: pd.Series) -> str:
        """Extract category name from a category header row."""
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).strip()
                if cell_str and not cell_str.isdigit():
                    return cell_str
        return "Unknown"
    
    def _extract_category_total(self, row: pd.Series) -> float:
        """Extract category total from a category header row."""
        for cell in row:
            if pd.notna(cell):
                try:
                    if isinstance(cell, (int, float)):
                        return float(cell)
                    elif isinstance(cell, str) and cell.replace('.', '').replace(',', '').isdigit():
                        return float(cell.replace(',', '.'))
                except:
                    continue
        return 0.0
    
    def _extract_task_description(self, row: pd.Series) -> Optional[str]:
        """Extract task description from a row."""
        for i, cell in enumerate(row):
            if pd.notna(cell):
                cell_str = str(cell).strip()
                if cell_str and not cell_str.isdigit() and len(cell_str) > 3:
                    # Skip common header words
                    if not any(keyword in cell_str.lower() for keyword in ['tilbud', 'budget', 'dato', 'projekt', 'kategori', 'rum', 'værelse', 'påslag', 'timer', 'takst']):
                        return cell_str
        return None
    
    def _extract_pricing_fields(self, row: pd.Series) -> Dict[str, Any]:
        """Extract pricing-related fields from a row."""
        pricing = {}
        
        # Look for pricing columns (usually in the right side of the sheet)
        for i, cell in enumerate(row):
            if pd.notna(cell):
                try:
                    if isinstance(cell, (int, float)) and cell > 0:
                        # This might be a price - determine what type based on position
                        if i >= len(row) - 3:  # Last few columns often contain totals
                            pricing["Tilbud"] = float(cell)
                        elif i >= len(row) - 6:  # Middle columns might contain other pricing
                            pricing["Salgspris"] = float(cell)
                except:
                    continue
        
        return pricing
    
    def _extract_labor_fields(self, row: pd.Series) -> Dict[str, Any]:
        """Extract labor-related fields from a row."""
        labor = {}
        
        for i, cell in enumerate(row):
            if pd.notna(cell):
                try:
                    if isinstance(cell, (int, float)):
                        # Look for hours (usually smaller numbers)
                        if 0 < cell <= 100:  # Reasonable range for hours
                            labor["Timer"] = float(cell)
                        # Look for hourly rate (usually larger numbers)
                        elif 100 < cell <= 1000:  # Reasonable range for hourly rates
                            labor["Takst"] = float(cell)
                except:
                    continue
        
        return labor
    
    def _extract_material_fields(self, row: pd.Series) -> Dict[str, Any]:
        """Extract material-related fields from a row."""
        materials = {}
        
        for i, cell in enumerate(row):
            if pd.notna(cell):
                try:
                    if isinstance(cell, (int, float)) and cell > 0:
                        # This might be material cost
                        if "Materialer" not in materials:
                            materials["Materialer"] = float(cell)
                except:
                    continue
        
        return materials
    
    def _extract_supplier_fields(self, row: pd.Series) -> Dict[str, Any]:
        """Extract supplier information from a row."""
        supplier = {}
        
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).strip()
                if cell_str and not cell_str.isdigit() and len(cell_str) <= 20:
                    # This might be a supplier name
                    if any(keyword in cell_str.upper() for keyword in ['BNORD', 'VVS', 'EL', 'MALER', 'TØMRER', 'MURER', 'SNEDKER', 'IKEA', 'KRONE', '&SHUFL']):
                        supplier["Unnamed: 3"] = cell_str
                        break
        
        return supplier
    
    def _extract_additional_fields(self, row: pd.Series) -> Dict[str, Any]:
        """Extract additional fields that might be present."""
        additional = {}
        
        # Look for markup percentage
        for cell in row:
            if pd.notna(cell):
                try:
                    if isinstance(cell, (int, float)) and 0 < cell <= 1:  # Markup is usually 0.15
                        additional["Påslag"] = float(cell)
                except:
                    continue
        
        return additional
    
    def process_all_files(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Process all Excel files in the input directory and save JSON outputs.
        
        Args:
            input_dir: Directory containing Excel files to process
            output_dir: Directory to save JSON outputs
            
        Returns:
            Dictionary containing processing results
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get list of Excel files
        excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]
        
        results = {
            "total_files": len(excel_files),
            "processed_files": [],
            "errors": [],
            "output_directory": output_dir
        }
        
        print(f"Found {len(excel_files)} Excel files to process")
        
        for excel_file in excel_files:
            file_path = os.path.join(input_dir, excel_file)
            print(f"\nProcessing: {excel_file}")
            
            # Parse the Excel file
            parsed_data = self.parse_excel_file(file_path)
            
            if parsed_data:
                # Generate output filename
                base_name = Path(excel_file).stem
                output_file = os.path.join(output_dir, f"{base_name}_components_full.json")
                
                # Save JSON output
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(parsed_data, f, indent=2, ensure_ascii=False, default=str)
                    
                    results["processed_files"].append({
                        "input_file": excel_file,
                        "output_file": f"{base_name}_components_full.json",
                        "components_count": len(parsed_data.get("components", [])),
                        "status": "success"
                    })
                    
                    print(f"✓ Successfully processed {excel_file}")
                    print(f"  Components extracted: {len(parsed_data.get('components', []))}")
                    print(f"  Output saved to: {output_file}")
                    
                except Exception as e:
                    error_msg = f"Error saving {excel_file}: {str(e)}"
                    results["errors"].append(error_msg)
                    print(f"✗ {error_msg}")
            else:
                results["errors"].append(f"Failed to parse {excel_file}")
                print(f"✗ Failed to parse {excel_file}")
        
        # Save summary report
        summary_file = os.path.join(output_dir, "processing_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{'='*50}")
        print(f"PROCESSING COMPLETE")
        print(f"{'='*50}")
        print(f"Total files: {results['total_files']}")
        print(f"Successfully processed: {len(results['processed_files'])}")
        print(f"Errors: {len(results['errors'])}")
        print(f"Output directory: {output_dir}")
        print(f"Summary saved to: {summary_file}")
        
        return results

def main():
    """Main function to run the parser."""
    # Initialize parser
    parser = ImprovedExcelComponentParser()
    
    # Set input and output directories
    input_directory = "real_examples/other_files"
    output_directory = "real_examples/other_files_processed"
    
    # Process all files
    results = parser.process_all_files(input_directory, output_directory)
    
    return results

if __name__ == "__main__":
    main()
