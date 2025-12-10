import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
# 1. Your Main Sheet ID (I extracted this from your link)
SHEET_ID = "1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48"

# 2. YOUR ADMIN TAB ID (GID)
# Look at your browser URL when on the Admin tab. It says "#gid=12345".
# Paste that number below inside the quotes.
ADMIN_GID = "1449805165" 

# Construct the bulletproof CSV links
MAIN_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
ADMIN_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={ADMIN_GID}"
EDIT_LINK = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

st.set_page_config(page_title="HW Shop", page_icon="🏎️")

# --- LOGO ---
try:
    st.image("logo.png", width=300)
except:
    st.title("🏎️ Hot Wheels Shop")

# --- LOAD DATA (The Safe Way) ---
# We use pandas directly. It is much faster and doesn't get Access Denied errors as easily.
try:
    df = pd.read_csv(MAIN_URL)
    df.columns = df.columns.str.strip() # Clean column names
except Exception as e:
    st.error("Could not load inventory.")
    st.info("Tip: Make sure your Sheet is set to 'Anyone with the link' -> 'Viewer'")
    st.stop()

# --- SEARCH ---
st.subheader("🔍 Search Inventory")
search_term = st.text_input("Type car name:", placeholder="e.g. BMW").lower().strip()

if search_term:
    if 'Car Name' not in df.columns:
        st.error("Column Error: Could not find 'Car Name' in row 1.")
    else:
        # Search logic
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} car(s):")
            for index, row in results.iterrows():
                with st.container(border=True):
                    st.subheader(row['Car Name'])
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**⭐ Rating:**\n{row.get('Rating', '-')}")
                    c2.write(f"**💰 Price:**\n{row.get('max price', '-')}")
                    c3.write(f"**📦 Stock:**\n{row.get('Stock', '-')}")
        else:
            st.warning("Car not found.")

# --- ADMIN LOGIN ---
with st.sidebar:
    st.header("🔐 Admin Login")
    user_in = st.text_input("Username")
    pass_in = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        try:
            # Read the Admin tab directly
            df_admin = pd.read_csv(ADMIN_URL)
            df_admin.columns = df_admin.columns.str.strip()
            
            # Check credentials
            match = df_admin[
                (df_admin['Username'].astype(str) == user_in) & 
                (df_admin['Password'].astype(str) == pass_in)
            ]
            
            if not match.empty:
                st.success(f"Hi {user_in}!")
                st.write("**Admin Controls:**")
                st.link_button("📝 Edit Inventory", EDIT_LINK)
            else:
                st.error("Wrong Username or Password")
        except:
            st.error("Could not verify password. Check Admin GID.")



