import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Rater", page_icon="🔥")
st.title("🔥 Hot Wheels Rater")

# 1. Connect (Read-Only Mode)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=SHEET_URL, usecols=[0, 1, 2], ttl=5)
    df = pd.DataFrame(data)
except Exception as e:
    st.error("Error loading database.")
    st.stop()

# 2. Search Tab
st.header("🔍 Find a Rating")
search_term = st.text_input("Type car name:", placeholder="e.g. Bone Shaker").lower().strip()

if search_term:
    # Filter data
    results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
    
    if not results.empty:
        st.success(f"Found {len(results)} car(s):")
        for index, row in results.iterrows():
            with st.container(border=True):
                st.subheader(row['Car Name'])
                st.write(f"**Rating:** {row['Rating']}/10")
                st.write(f"**Notes:** {row['Notes']}")
    else:
        st.warning("Car not found yet.")

st.divider()

# 3. Add Button (Safe Mode)
st.subheader("➕ Want to rate a new car?")
st.write("Google requires manual entry for security.")
# This button opens your Google Sheet in a new tab
st.link_button("Go to Google Sheet to Add Car", SHEET_URL)
