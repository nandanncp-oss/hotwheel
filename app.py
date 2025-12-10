import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Shop", page_icon="🏎️")

# --- LOGO ---
try:
    st.image("logo.png", width=300)
except:
    st.title("🏎️ Hot Wheels Shop")

# --- CONNECT TO DATABASE ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Load Inventory (Sheet1)
try:
    data = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=5)
    df = pd.DataFrame(data)
except:
    st.error("Error loading inventory. Check if 'Sheet1' exists.")
    st.stop()

# 2. Load Admin Credentials (Admin Sheet)
try:
    admin_data = conn.read(spreadsheet=SHEET_URL, worksheet="Admin", ttl=5)
    df_admin = pd.DataFrame(admin_data)
    # Ensure data is text so numbers don't break it
    df_admin['Username'] = df_admin['Username'].astype(str)
    df_admin['Password'] = df_admin['Password'].astype(str)
except:
    st.warning("Admin tab not found. Login disabled.")
    df_admin = pd.DataFrame()

# ==========================================
# 🔐 ADMIN LOGIN (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("🔐 Admin Login")
    
    # Inputs
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if user_input and pass_input:
        # Check if Username AND Password match a row in the Admin sheet
        # We look for a row where BOTH columns match what you typed
        match = df_admin[
            (df_admin['Username'] == user_input) & 
            (df_admin['Password'] == pass_input)
        ]
        
        if not match.empty:
            st.success(f"Welcome, {user_input}!")
            st.write("---")
            st.write("**Manage Inventory:**")
            st.link_button("📝 Edit Google Sheet", SHEET_URL)
        else:
            st.error("Invalid Username or Password")

# ==========================================
# 🔍 SEARCH
# ==========================================
st.subheader("🔍 Search Inventory")
search_term = st.text_input("Type car name:", placeholder="e.g. BMW").lower().strip()

if search_term:
    if 'Car Name' not in df.columns:
        st.error("Error: 'Car Name' column is missing in Sheet1.")
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
                        stock = row.get('Stock', 'N/A')
                        st.write(f"**📦 Stock**\n{stock}")
        else:
            st.warning("Car not found.")
