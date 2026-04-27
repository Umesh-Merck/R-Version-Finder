import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="R Package Finder",
    page_icon="📦",
    layout="centered"
)

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# ===================== STYLING =====================
st.markdown("""
<style>
.block-container {
    max-width: 900px;
    padding-top: 1.5rem;
    padding-bottom: 150px;
}

/* Header */
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #888888;
    margin-bottom: 2rem;
    font-size: 13px;
    line-height: 1.5;
}

/* Chat message styling */
.stChatMessage {
    background-color: transparent;
    padding: 1rem 0;
    border-radius: 0;
}

/* Result card */
.result-card {
    background-color: transparent;
    padding: 0;
    border-radius: 0;
    border: none;
}

/* Dataframe styling */
.dataframe {
    font-size: 13px;
}

.dataframe th {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 12px;
    font-weight: 600;
    text-align: left;
}

.dataframe td {
    padding: 12px;
    border-bottom: 1px solid #30363d;
}

.dataframe tbody tr:hover {
    background-color: #0d1117;
}

/* Input section styling */
.stChatInputContainer {
    background-color: transparent;
    border-top: 1px solid #30363d;
    padding-top: 1rem;
    margin-top: 2rem;
}

/* File uploader styling */
.stFileUploader {
    background-color: #0d1117;
    border: 1px dashed #30363d;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

/* Download button */
.stDownloadButton {
    margin: 0.5rem 0;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #30363d;
    margin: 1.5rem 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0d1117;
}

::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #444c56;
}
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "packages_dict" not in st.session_state:
    st.session_state.packages_dict = None

# ===================== FUNCTIONS =====================
@st.cache_resource
def fetch_packages_data():
    """Fetch CRAN PACKAGES file once per session"""
    try:
        url = "https://cran.r-project.org/src/contrib/PACKAGES"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return None

def parse_packages_file(content):
    """Parse PACKAGES file into a dictionary"""
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

    for pkg in package_names:
        pkg = pkg.strip()
        if not pkg:
            continue

        version = packages_dict.get(pkg, "Version not found")
        link = f"https://cran.r-project.org/web/packages/{pkg}/index.html"

        results.append({
            "Package": pkg,
            "Version": version,
            "Link": link
        })

    return results

# ===================== LOAD DATA =====================
data = fetch_packages_data()
if not data:
    st.error("❌ Failed to fetch CRAN data. Please check your internet connection.")
    st.stop()

packages_dict = parse_packages_file(data)
st.session_state.packages_dict = packages_dict

# ===================== HEADER =====================
st.markdown('<div class="title">R Package Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Chat-style interface for CRAN package lookup</div>', unsafe_allow_html=True)
st.divider()

# ===================== DISPLAY CHAT HISTORY =====================
st.markdown("")  # Add spacing

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="📦" if msg["role"] == "user" else "📊"):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            st.markdown("**Results**")
            
            # Display dataframe with custom styling
            col1, col2 = st.columns([3, 1])
            with col1:
                st.dataframe(msg["data"], use_container_width=True, hide_index=True)
            
            with col2:
                st.download_button(
                    "📥 Download",
                    data=msg["excel"],
                    file_name=msg["file_name"],
                    key=f"download_{idx}"
                )
    
    if idx < len(st.session_state.messages) - 1:
        st.divider()

# ===================== SEPARATE INPUT SECTION =====================
st.markdown("")
st.divider()

# Use form to prevent uncontrolled reruns on every interaction
with st.form("package_search_form", clear_on_submit=True):
    st.markdown("**📊 Enter packages or upload a file**")
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx", "xls"], label_visibility="collapsed", key="file_input_form")
    
    with col2:
        st.markdown("")  # Spacing
    
    # Text input
    user_input = st.text_area(
        "Enter packages",
        placeholder="ggplot2\ndplyr, tidyr\ndata.table",
        height=80,
        label_visibility="collapsed"
    )
    
    # Submit button
    submit_button = st.form_submit_button("🔍 Search Packages", use_container_width=True)

# ===================== PROCESS INPUT (ONLY ONCE PER SUBMIT) =====================
if submit_button:
    package_names = []
    input_display = ""
    
    # Handle text input
    if user_input.strip():
        package_names = [
            p.strip()
            for p in user_input.replace("\n", ",").split(",")
            if p.strip()
        ]
        input_display = f"📦 {user_input}"
    
    # Handle file upload
    elif uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_input = pd.read_csv(uploaded_file)
            else:
                df_input = pd.read_excel(uploaded_file)
            
            package_names = df_input.iloc[:, 0].astype(str).tolist()
            package_names = [name.strip() for name in package_names if name.strip()]
            input_display = f"📁 Uploaded: {uploaded_file.name}"
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()
    
    else:
        st.error("❌ Please enter package names or upload a file")
        st.stop()
    
    # Validate we have packages
    if not package_names:
        st.error("❌ No valid package names found")
        st.stop()
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": input_display
    })
    
    # Generate results
    results = generate_results(package_names, packages_dict)
    df = pd.DataFrame(results)
    
    # Create Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='CRAN Packages')
    
    excel_data = output.getvalue()
    filename = f"cran_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "data": df,
        "excel": excel_data,
        "file_name": filename
    })
    
    # Rerun to display new messages
    st.rerun()
