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

# --- CONNECT ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. LOAD INVENTORY (The Fix: We removed worksheet="Sheet1")
try:
    # We ask it to just read the default (first) sheet. 
    # This fixes the error if your sheet is named slightly differently.
    data = conn.read(spreadsheet=SHEET_URL, ttl=5)
    df = pd.DataFrame(data)
    
    # Clean up column names (remove hidden spaces)
    df.columns = df.columns.str.strip()
    
except Exception as e:
    st.error(f"Error loading cars: {e}")
    st.stop()

# 2. LOAD ADMIN (Safe Mode)
try:
    # We try to read the "Admin" tab. If it fails, we just don't allow login.
    admin_data = conn.read(spreadsheet=SHEET_URL, worksheet="Admin", ttl=5)
    df_admin = pd.DataFrame(admin_data)
    if not df_admin.empty:
        df_admin.columns = df_admin.columns.str.strip()
        df_admin['Username'] = df_admin['Username'].astype(str)
        df_admin['Password'] = df_admin['Password'].astype(str)
except:
    df_admin = pd.DataFrame()

# --- ADMIN LOGIN (SIDEBAR) ---
with st.sidebar:
    st.header("🔐 Admin Login")
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        if not df_admin.empty:
            match = df_admin[
                (df_admin['Username'] == user_input) & 
                (df_admin['Password'] == pass_input)
            ]
            if not match.empty:
                st.success(f"Hi {user_input}!")
                st.write("**Manage Inventory:**")
                st.link_button("📝 Edit Google Sheet", SHEET_URL)
            else:
                st.error("Wrong Username or Password")
        else:
            st.error("Admin tab not found in Sheet.")

# --- SEARCH ---
st.subheader("🔍 Search Inventory")
search_term = st.text_input("Type car name:", placeholder="e.g. BMW").lower().strip()

if search_term:
    # Double check column exists
    if 'Car Name' not in df.columns:
        st.error("⚠️ Column Error!")
        st.write(f"I found these columns: {df.columns.tolist()}")
        st.write("Please check Row 1 of your Google Sheet.")
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
                        stock_val = str(row.get('Stock', 'N/A'))
                        color = "green" if "in stock" in stock_val.lower() else "red"
                        st.markdown(f"**📦 Stock**\n:{color}[{stock_val}]")
        else:
            st.warning("Car not found.")
