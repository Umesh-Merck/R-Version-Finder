import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import re

st.set_page_config(
    page_title="R Package Finder",
    page_icon="📦",
    layout="wide"
)

st.title("R Package Finder Agent")
st.markdown("Retrieve latest R package versions from CRAN")

# Session state for caching PACKAGES data
@st.cache_resource
def fetch_packages_data():
    """Fetch CRAN PACKAGES file once per session"""
    try:
        url = "https://cran.r-project.org/src/contrib/PACKAGES"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Failed to fetch CRAN PACKAGES file: {str(e)}")
        return None

def parse_packages_file(content):
    """Parse PACKAGES file into a dictionary mapping package names to versions"""
    package_dict = {}
    lines = content.split('\n')
    current_package = None
    
    for line in lines:
        if line.startswith('Package:'):
            current_package = line.replace('Package:', '').strip()
        elif line.startswith('Version:') and current_package:
            version = line.replace('Version:', '').strip()
            package_dict[current_package] = version
            current_package = None
    
    return package_dict

def generate_results(package_names, packages_dict):
    """Generate results for requested packages"""
    results = []
    
    for package_name in package_names:
        package_name = package_name.strip()
        if not package_name:
            continue
        
        version = packages_dict.get(package_name, "Version not found")
        reference_link = f"https://cran.r-project.org/web/packages/{package_name}/index.html"
        
        results.append({
            'Package Name': package_name,
            'Latest Version Available': version,
            'Reference Link': reference_link
        })
    
    return results

def format_text_output(results):
    """Format results as plain text per specifications"""
    output = []
    for result in results:
        output.append(f"Package Name – {result['Package Name']}")
        output.append(f"Latest Version Available – {result['Latest Version Available']}")
        output.append(f"Reference Link : {result['Reference Link']}")
        output.append("")  # Empty line between packages
    
    return "\n".join(output).strip()

# Fetch data once at start
packages_content = fetch_packages_data()

if packages_content:
    packages_dict = parse_packages_file(packages_content)
    st.success(f"✓ CRAN PACKAGES loaded: {len(packages_dict)} packages cached")
    
    # Input method selection
    st.markdown("---")
    input_method = st.radio("Choose input method:", ["Text Input", "Excel Upload"], horizontal=True)
    
    results = []
    
    if input_method == "Text Input":
        st.subheader("Enter Package Names")
        text_input = st.text_area(
            "Enter R package names (one per line or comma-separated):",
            placeholder="Example:\nggplot2\ndplyr\ntidyr",
            height=150
        )
        
        if st.button("Search Packages", key="text_search"):
            if text_input.strip():
                # Parse input: handle both newline and comma-separated
                package_names = []
                
                # Split by newlines first
                lines = text_input.split('\n')
                for line in lines:
                    # Split by commas within each line
                    names = [n.strip() for n in line.split(',')]
                    package_names.extend(names)
                
                # Remove empty strings
                package_names = [name for name in package_names if name]
                
                results = generate_results(package_names, packages_dict)
    
    else:  # Excel Upload
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader(
            "Upload Excel file with package names in first column:",
            type=["xlsx", "xls"]
        )
        
        if uploaded_file and st.button("Process Excel", key="excel_search"):
            try:
                df = pd.read_excel(uploaded_file)
                package_names = df.iloc[:, 0].astype(str).tolist()  # Get first column
                results = generate_results(package_names, packages_dict)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
    
    # Display results
    if results:
        st.markdown("---")
        st.subheader("Results")
        
        # Display as plain text
        text_output = format_text_output(results)
        st.text_area("Output:", value=text_output, height=300, disabled=True)
        
        # Option to download as Excel
        st.markdown("---")
        st.subheader("Download Results")
        
        df_results = pd.DataFrame(results)
        
        # Generate Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_results.to_excel(writer, index=False, sheet_name='CRAN Packages')
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name="CRAN_Packages_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Display preview
        st.markdown("**Excel Preview:**")
        st.dataframe(df_results, use_container_width=True)
        
        st.info(f"✓ Processed {len(results)} package(s)")

else:
    st.error("Cannot proceed: CRAN PACKAGES file could not be fetched. Please check your internet connection and try again.")
