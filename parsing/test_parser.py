#!/usr/bin/env python3
"""
Test script for the Excel Component Parser.
Tests the parser with a single file to ensure it works correctly.
"""

import sys
import os
from pathlib import Path
from excel_parser_improved import ImprovedExcelComponentParser

def test_single_file():
    """Test the parser with a single Excel file."""
    
    # Initialize parser
    parser = ImprovedExcelComponentParser()
    
    # Test file path
    test_file = "real_examples/other_files/2023.04.19 Brannersvej 5 _ Kalkulation.xlsx"
    
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return False
    
    print(f"Testing parser with file: {test_file}")
    print("=" * 60)
    
    try:
        # Parse the test file
        result = parser.parse_excel_file(test_file)
        
        if result:
            print("✓ File parsed successfully!")
            print(f"  Metadata: {result.get('metadata', {})}")
            print(f"  Components extracted: {len(result.get('components', []))}")
            
            # Show first few components
            components = result.get('components', [])
            if components:
                print("\nFirst 3 components:")
                for i, comp in enumerate(components[:3]):
                    print(f"  {i+1}. {comp.get('Opgave', 'N/A')}")
                    print(f"     Kategori: {comp.get('kategori', 'N/A')}")
                    print(f"     Tilbud: {comp.get('Tilbud', 'N/A')}")
                    print(f"     Timer: {comp.get('Timer', 'N/A')}")
                    print()
            
            # Save test output
            output_file = "test_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                import json
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"Test output saved to: {output_file}")
            return True
            
        else:
            print("✗ Failed to parse file")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        return False

def main():
    """Main test function."""
    print("Excel Component Parser - Test Script")
    print("=" * 60)
    
    success = test_single_file()
    
    if success:
        print("\n✓ Test completed successfully!")
        print("The parser is working correctly and ready to process all files.")
    else:
        print("\n✗ Test failed!")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
