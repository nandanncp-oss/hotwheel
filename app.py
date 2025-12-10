import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK TO YOUR SHEET ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Rater", page_icon="🚘")
st.title("🏎Hot Wheels Rater")

# 1. Connect and Load Data
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=SHEET_URL, ttl=5)
    df = pd.DataFrame(data)
except Exception as e:
    st.error("Could not load the list. Check your Google Sheet link!")
    st.stop()

# 2. Search Section
st.header("🔍 Find a Car")
search_term = st.text_input("Type car name:", placeholder="funkycart").lower().strip()

if search_term:
    # Check if 'Car Name' exists to prevent crashing
    if 'Car Name' not in df.columns:
        st.error("Error: I can't find a column named 'Car Name' in your sheet. Check row 1.")
    else:
        # Filter for the car
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} car(s):")
            for index, row in results.iterrows():
                with st.container(border=True):
                    st.subheader(row['Car Name'])
                    
                    # Create 3 columns for a clean look: Rating | Price | Stock
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Looks for 'Rating' column
                        rating = row.get('Rating', 'N/A')
                        st.write(f"**⭐ Rating**\n{rating}")
                    
                    with col2:
                        # Looks for 'max price' column
                        price = row.get('max price', 'N/A')
                        st.write(f"**💰 Price**\n{price}")
                        
                    with col3:
                        # Looks for 'Stock' column
                        stock = row.get('Stock', 'N/A')
                        st.write(f"**📦 Stock**\n{stock}")
                    
        else:
            st.warning("Car not found.")



