import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK TO YOUR SHEET ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Rater", page_icon="🔥")
st.title("🔥 Hot Wheels Rater")

# 1. Connect and Load Data
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # We read the data from your specific link
    data = conn.read(spreadsheet=SHEET_URL, ttl=5)
    df = pd.DataFrame(data)
except Exception as e:
    st.error("Could not load the list. Make sure the Google Sheet link is correct!")
    st.stop()

# 2. Search Tab
st.header("🔍 Find a Car")
search_term = st.text_input("Type car name:", placeholder="e.g. BMW").lower().strip()

if search_term:
    # Check if 'Car Name' exists (Crash-proof check)
    if 'Car Name' not in df.columns:
        st.error("Error: I can't find a column named 'Car Name' in your sheet.")
    else:
        # Search for the car
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} car(s):")
            for index, row in results.iterrows():
                with st.container(border=True):
                    # Display the Name
                    st.subheader(row['Car Name'])
                    
                    # Display the Rating
                    st.write(f"**⭐ Rating:** {row['Rating']}/10")
                    
                    # Display the Price (Looking for 'max price')
                    # We use .get() so it doesn't crash if the column name is slightly different
                    price = row.get('max price', 'N/A')
                    st.write(f"**💰 Price:** {price}")
                    
        else:
            st.warning("Car not found.")

st.divider()

# 3. Add Button (Safe Mode)
st.subheader("➕ Add a New Car")
st.write("Click below to open the sheet and add a car manually:")
st.link_button("Go to Google Sheet", SHEET_URL)
