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

# 1. Load the Cars (From the first sheet, usually 'Sheet1')
try:
    # We specifically ask for Sheet1 for the cars
    data = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=5)
    df = pd.DataFrame(data)
except:
    st.error("Error loading cars. Make sure your main sheet is named 'Sheet1'")
    st.stop()

# 2. Load the Password (From the new 'Admin' sheet)
try:
    # We read the Admin tab to get the password
    admin_data = conn.read(spreadsheet=SHEET_URL, worksheet="Admin", ttl=5)
    df_admin = pd.DataFrame(admin_data)
    # We grab the value from the first row of the 'Password' column
    REAL_PASSWORD = str(df_admin['Password'].iloc[0])
except:
    # If the Admin tab is missing, default to 1234 so the app doesn't crash
    REAL_PASSWORD = "1234"

# ==========================================
# 🔐 ADMIN SIDEBAR
# ==========================================
with st.sidebar:
    st.header("🔐 Admin Access")
    input_pass = st.text_input("Enter Password:", type="password")
    
    # Compare input with the Google Sheet password
    if input_pass == REAL_PASSWORD:
        st.success("Access Granted!")
        st.write("Click below to edit Stock:")
        st.link_button("📝 Edit Google Sheet", SHEET_URL)
    elif input_pass:
        st.error("Wrong Password")

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
                        st.write(f"**Rating**\n{row.get('Rating', 'N/A')}")
                    with col2:
                        st.write(f"**Price**\n{row.get('max price', 'N/A')}")
                    with col3:
                        st.write(f"**Stock**\n{row.get('Stock', 'N/A')}")
        else:
            st.warning("Car not found.")
