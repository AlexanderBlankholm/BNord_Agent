# Excel Component Parser for Construction Projects

This project contains a comprehensive parser for Excel files containing construction project components and pricing information. The parser extracts detailed component breakdowns from Excel files and generates structured JSON outputs with all the components, categories, labor hours, material costs, and pricing information.

## Project Overview

The parser was designed to process Excel files similar to those in the `real_examples/first_three` folder, which contain well-processed construction project data. The goal is to automatically process the 10 unprocessed Excel files in the `real_examples/other_files` folder and generate similar JSON outputs with detailed component breakdowns.

## Features

- **Automatic Excel Processing**: Processes multiple Excel files in batch
- **Component Extraction**: Extracts task descriptions, labor hours, material costs, and pricing
- **Category Detection**: Automatically identifies project categories and their totals
- **Supplier Information**: Extracts supplier/contractor information
- **Structured Output**: Generates consistent JSON format matching the processed examples
- **Error Handling**: Comprehensive error reporting and logging
- **Metadata Extraction**: Extracts project information, dates, and file details

## File Structure

```
BNord_Agent/
├── real_examples/
│   ├── first_three/                    # Processed examples (reference)
│   │   ├── 2025.05.03_Tilbud_Peter_Fabers_gade.xlsx
│   │   ├── 2025.05.03_Tilbud_Peter_Fabers_gade_components_full.json
│   │   └── ...
│   └── other_files/                    # Files to be processed
│       ├── 2023.04.19 Brannersvej 5 _ Kalkulation.xlsx
│       ├── 2023.06.10 H.P. Ørums Gade 27 CB.xlsx
│       └── ...
├── excel_parser_improved.py            # Main parser implementation
├── excel_parser.py                     # Original parser (basic version)
├── test_parser.py                      # Test script for single file
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import pandas, openpyxl, numpy; print('Dependencies installed successfully')"
   ```

## Usage

### 1. Test the Parser (Recommended First Step)

Test the parser with a single file to ensure it works correctly:

```bash
python test_parser.py
```

This will:
- Test the parser with one Excel file
- Show extracted components
- Save a test output file
- Verify the parser is working correctly

### 2. Process All Files

Once testing is successful, process all Excel files in the `other_files` folder:

```bash
python excel_parser_improved.py
```

This will:
- Process all 10 Excel files in `real_examples/other_files/`
- Generate JSON outputs in `real_examples/other_files_processed/`
- Create a processing summary report
- Show progress and results

### 3. Custom Processing

You can also use the parser programmatically:

```python
from excel_parser_improved import ImprovedExcelComponentParser

# Initialize parser
parser = ImprovedExcelComponentParser()

# Process a single file
result = parser.parse_excel_file("path/to/file.xlsx")

# Process all files in a directory
results = parser.process_all_files("input_dir", "output_dir")
```

## Output Format

The parser generates JSON files with the following structure:

```json
{
  "metadata": {
    "filename": "2023.04.19 Brannersvej 5 _ Kalkulation",
    "date": "2023-04-19",
    "project_name": "2023.04.19 Brannersvej 5 _ Kalkulation",
    "project_info": "Tilbud Brannersvej 5 1.th",
    "total_rows": 94,
    "total_columns": 18
  },
  "components": [
    {
      "Opgave": "Projektledelse, Dokumentation og Administration",
      "kategori": "Projekt",
      "kategori_total": 39150.0,
      "Timer": null,
      "Takst": null,
      "Materialer": null,
      "Tilbud": 6000.0,
      "Unnamed: 3": "Bnord",
      "row_index": 4
    }
  ]
}
```

## Component Fields

Each component contains:

- **Opgave**: Task description
- **kategori**: Project category (e.g., "Murer", "Tømrer", "VVS", "EL")
- **kategori_total**: Total amount for the category
- **Timer**: Labor hours
- **Takst**: Hourly rate
- **Materialer**: Material costs
- **Tilbud**: Final price/quote
- **Unnamed: 3**: Supplier/contractor information
- **Påslag**: Markup percentage
- **row_index**: Original row number in Excel

## Error Handling

The parser includes comprehensive error handling:

- **File-level errors**: Individual file parsing failures
- **Data extraction errors**: Issues with specific data fields
- **Output errors**: Problems saving JSON files
- **Summary reporting**: Complete processing status

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   ```bash
   pip install pandas openpyxl numpy
   ```

2. **File Access Issues**:
   - Ensure Excel files are not open in other applications
   - Check file permissions

3. **Memory Issues**:
   - Process files individually if memory is limited
   - Use the test script first

### Debug Mode

For detailed debugging, modify the parser to include more verbose output:

```python
# Add debug prints in the parser methods
print(f"Processing row {idx}: {row}")
```

## Performance

- **Processing Speed**: Typically 1-5 seconds per file depending on size
- **Memory Usage**: Minimal memory footprint
- **Scalability**: Can handle hundreds of files efficiently

## Future Enhancements

Potential improvements for future versions:

- **Machine Learning**: Better category detection using ML models
- **Template Recognition**: Automatic template detection for different Excel formats
- **Validation**: Data validation and quality checks
- **API Integration**: REST API for web-based processing
- **Batch Processing**: Parallel processing for large file sets

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and business use.

## Support

For questions or issues:

1. Check the troubleshooting section above
2. Review the test output for specific errors
3. Examine the processing summary for detailed results

## Example Output

After successful processing, you'll see output similar to:

```
==================================================
PROCESSING COMPLETE
==================================================
Total files: 10
Successfully processed: 10
Errors: 0
Output directory: real_examples/other_files_processed
Summary saved to: real_examples/other_files_processed/processing_summary.json
```

Each processed file will have a corresponding JSON file with the suffix `_components_full.json` containing all the extracted component information.
