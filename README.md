# R Package Finder Agent

An interactive chatbot/web application that retrieves the latest available versions for R packages from CRAN and generates their corresponding reference links.

## Features

- **Single Bulk Data Fetch**: Retrieves CRAN PACKAGES file once per session and caches it for all queries
- **Multiple Input Methods**:
  - Text input (single or multiple package names)
  - Excel file upload for bulk queries
- **Fast Lookups**: In-memory package mapping for instant results
- **Excel Export**: Download results in Excel format with proper structure
- **Handles Missing Packages**: Shows "Version not found" for packages not in CRAN
- **Plain Text Output**: Follows exact format specifications with no markdown/tables

## Installation

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

The web interface will open in your browser at `http://localhost:8501`

### Text Input Method
- Enter package names one per line or comma-separated
- Click "Search Packages"
- View results and download as Excel if needed

### Excel Upload Method
- Prepare an Excel file with package names in the first column
- Upload the file
- Click "Process Excel"
- Results available in both text and Excel download format

## Output Format

For each package, the agent returns:

```
Package Name – <package name>
Latest Version Available – <version or "Version not found">
Reference Link : https://cran.r-project.org/web/packages/<package>/index.html
```

## Data Source

- **URL**: https://cran.r-project.org/src/contrib/PACKAGES
- **Fetch Frequency**: Once per session
- **Parse Method**: Line-by-line parsing of Package: and Version: fields
- **Lookup Type**: In-memory mapping

## Technical Details

- **Framework**: Streamlit (web-based interactive UI)
- **Data Processing**: Pandas (Excel I/O)
- **Caching**: Session-level caching to minimize network requests
- **Format**: Plain text output with optional Excel export

## Constraints Enforced

- No per-package HTML page lookups
- No DESCRIPTION file fetches
- No per-package API calls
- No web search or cached data fallbacks
- No markdown or table formatting in text output
- Exact output format as specified
