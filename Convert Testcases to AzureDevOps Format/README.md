# Convert Testcases to Azure DevOps Format

## Overview

This Python script converts test case data from a source CSV format into a  **Azure DevOps-compatible CSV format**. It's designed to help automate the migration of test cases into Azure DevOps while parsing and restructuring test step information (preconditions, actions, and expected results).

## What It Does

The script performs the following operations:

1. **Reads** an input CSV file containing test cases 
2. **Parses** the test case data, extracting:
   - Test case ID and title
   - Preconditions (setup steps)
   - Test steps with actions and expected results
   - Status information
3. **Restructures** the data into an Azure DevOps-compatible format
4. **Cleans** the data by:
   - Removing numbered list markers (e.g., "1-", "2-") from steps
   - Normalizing URLs (adding "Navigate to" prefix where appropriate)
   - Removing newline characters within cells
   - Handling multi-line entries
5. **Outputs** a properly formatted CSV file ready for import into Azure DevOps

## Input Format

The input CSV file should contain the following columns:
- **API Name** - The API or feature being tested
- **Case ID** - Unique test case identifier
- **Title** - Test case title/description
- **Preconditions** - Setup steps (can contain numbered lists)
- **Step** - Test steps (can contain numbered lists or multi-line entries)
- **Expected** - Expected result/outcome
- **Status** - Test case status

**Example input structure:**
```
API Name,Case ID,Title,Preconditions,Step,Expected,Status
GetById,TC001,Get Category by ID,"1- User is logged in
2- Database has test data","1- Navigate to /api/categories/1
2- Send GET request","200 OK with category data",Active
```

## Output Format

The output CSV file follows the Azure DevOps import format with these columns:
- **ID** - Test case identifier
- **Work Item Type** - Always "Test Case" for this script
- **Title** - Test case title
- **Test Step** - Sequential step number
- **Step Action** - What action to perform
- **Step Expected** - Expected result (for the final step)
- **Area Path** - Project area (default: "main")
- **Assigned To** - Assignee (empty by default)
- **State** - Work item state (default: "Design")

**Example output structure:**
```
ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Assigned To,State
TC001,Test Case,Get Category by ID,1,User is logged in,,main,,Design
TC001,Test Case,Get Category by ID,2,Database has test data,,main,,Design
TC001,Test Case,Get Category by ID,3,Navigate to /api/categories/1,,main,,Design
TC001,Test Case,Get Category by ID,4,Send GET request,200 OK with category data,main,,Design
```

## How to Use

### 1. Prepare Your Input File
- Create or obtain a CSV file with test cases in the source format
- Place it in the same directory as the script
- Update the `input_path` variable in the script with your filename:
  ```python
  input_path = "./your_input_file.csv"
  ```

### 2. Configure Output Path (Optional)
- By default, output is saved as `output.csv`
- To change this, modify the `output_path` variable:
  ```python
  output_path = "your_output_filename.csv"
  ```

### 3. Run the Script
```bash
python convert_testcases.py
```

### 4. Check the Output
- The converted file will be created in the same directory
- A confirmation message will appear: `Converted file saved to [filename]`
- Open the output CSV file to verify the conversion
- Import the file into Azure DevOps using the standard import feature

## Configuration

You can customize the output format by modifying the `OUTPUT_HEADER` list in the script:

```python
OUTPUT_HEADER = [
    "ID",
    "Work Item Type",
    "Title",
    "Test Step",
    "Step Action",
    "Step Expected",
    "Area Path",
    "Assigned To",
    "State",
]
```

You can also modify the default values in the `flush_case()` function to match your Azure DevOps project structure.

## Example Workflow

1. Export test cases from your source system as CSV
2. Place the CSV file in the script directory
3. Update `input_path` in the script
4. Run: `python convert_testcases.py`
5. Open the generated output file
6. Review the converted format for accuracy
7. Import into Azure DevOps using Work Items > Import from CSV


