import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Shop", page_icon="🏎️")
st.title("🏎️ Hot Wheels Shop")

# --- CONNECT TO DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Load the data
    data = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=5)
    df = pd.DataFrame(data)
    
    # ⚠️ MAGIC FIX: This removes hidden spaces from your headers
    df.columns = df.columns.str.strip()
    
    # Optional: Print columns to the screen so you can see what the app sees
    # st.write("Debug - Columns found:", df.columns.tolist()) 

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SEARCH ---
search_term = st.text_input("Type car name:", placeholder="e.g. BMW").lower().strip()

if search_term:
    # Check if 'Car Name' exists AFTER cleaning spaces
    if 'Car Name' not in df.columns:
        st.error("⚠️ Column Error!")
        st.write(f"The app is looking for **'Car Name'**, but your sheet has these columns: {df.columns.tolist()}")
        st.write("Please check the spelling in your Google Sheet Row 1.")
    else:
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} car(s):")
            for index, row in results.iterrows():
                with st.container(border=True):
                    st.subheader(row['Car Name'])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**⭐ Rating**\n{row.get('Rating', 'N/A')}")
                    with col2:
                        st.write(f"**💰 Price**\n{row.get('max price', 'N/A')}")
                    with col3:
                        st.write(f"**📦 Stock**\n{row.get('Stock', 'N/A')}")
        else:
            st.warning("Car not found.")

# --- ADMIN LOGIN (Simple Version) ---
with st.sidebar:
    st.header("Admin Access")
    if st.text_input("Password", type="password") == "1234":
        st.success("Logged In")
        st.link_button("📝 Edit Inventory", SHEET_URL)
