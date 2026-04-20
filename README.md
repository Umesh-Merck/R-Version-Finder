# R Package Finder Chatbot

An interactive chatbot web application that retrieves the latest available versions for R packages from CRAN and generates their corresponding reference links with **continuous conversation history**.

## Features

### Core Functionality
- ✅ **Single Bulk Data Fetch**: Retrieves CRAN PACKAGES file once per session and caches it
- ✅ **Fast Lookups**: In-memory package mapping for instant results
- ✅ **Handles Missing Packages**: Shows "Version not found" for packages not in CRAN

### Chatbot Architecture
- 💬 **Continuous Conversation**: Multiple queries in the same chat session
- 💬 **Chat History**: All previous requests and results retained in conversation
- 💬 **Clear Chat**: Button to reset conversation history anytime
- 📝 **Unified Input**: Single prompt bar for text and file uploads

### Input Methods
- **Text Input**: One per line or comma-separated
  ```
  ggplot2
  dplyr, tidyr
  data.table
  ```
- **File Upload**: Excel (.xlsx, .xls) or CSV (.csv) with package names in first column

### Output Formats
- **Plain Text**: All results in standard format per specifications
- **Table View**: Results displayed as interactive Pandas dataframe
- **Excel Download**: Export each result set as Excel file
- **Chat Display**: Results shown in chat message bubbles with timestamps

## Installation

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Step 1: Navigate to project
```bash
cd "c:\Users\X284176\OneDrive - MerckGroup\Desktop\AI Agents\R Package Finder"
```

### Step 2: Run the app
```bash
&".\.venv\Scripts\python.exe" -m streamlit run app.py
```

### Step 3: Access in browser
Open `http://localhost:8501`

## Usage Guide

### Text Input
1. Type or paste package names in the text box
2. Enter one per line or comma-separated
3. Click **🔍 Search Text**
4. View results in chat history

### File Upload
1. Click the file uploader button
2. Select Excel (.xlsx, .xls) or CSV (.csv)
3. Make sure package names are in the **first column**
4. Click **📤 Upload File**
5. View results in chat history

### Managing Conversations
- View all previous queries and results in **Conversation History**
- Click **🗑️ Clear Chat** to start fresh
- Each result shows timestamp and download option
- Results persist for the current session

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
- **Data Processing**: Pandas (Excel/CSV I/O)
- **State Management**: Streamlit Session State (persistent chat history)
- **Caching**: Session-level caching to minimize network requests
- **Output Formats**: Plain text, tables, and Excel files

## Constraints Enforced

- ✓ No per-package HTML page lookups
- ✓ No DESCRIPTION file fetches
- ✓ No per-package API calls
- ✓ No web search or cached data fallbacks
- ✓ Exact output format as specified
- ✓ Single bulk PACKAGES fetch per session

## Repository

GitHub: https://github.com/Umesh-Merck/R-Version-Finder
