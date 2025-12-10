import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- DIRECT LINK TO YOUR DATABASE ---
# We put the link here so we don't need the Secrets box
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifx_HY5UPumM8qcFaIuhQx2BonJzr2ZWGNQnbbfMS48/edit?usp=sharing"

st.set_page_config(page_title="HW Rater", page_icon="🔥")
st.title("🔥 Hot Wheels Rater")

# Connect to Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # We use the hardcoded link here
    data = conn.read(spreadsheet=SHEET_URL, usecols=[0, 1, 2], ttl=5)
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

tab1, tab2 = st.tabs(["🔍 Find Rating", "➕ Add New Car"])

# --- TAB 1: SEARCH ---
with tab1:
    st.header("Check a Hot Wheel")
    search_term = st.text_input("Type car name:", placeholder="e.g. Bone Shaker").lower().strip()

    if search_term:
        # Search logic
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} match(es):")
            for index, row in results.iterrows():
                with st.container(border=True):
                    st.subheader(row['Car Name'])
                    st.write(f"**Rating:** {row['Rating']}/10")
                    st.write(f"**Notes:** {row['Notes']}")
        else:
            st.warning("No rating found for this car.")

# --- TAB 2: ADD ---
with tab2:
    st.header("Rate a New Car")
    with st.form("rating_form"):
        new_name = st.text_input("Car Name")
        new_rating = st.slider("Rating (1-10)", 1, 10, 5)
        new_note = st.text_area("Notes")
        
        submitted = st.form_submit_button("Save Rating")
        
        if submitted and new_name:
            # Check for duplicates
            if new_name.lower() in df['Car Name'].astype(str).str.lower().values:
                st.error("Car already exists!")
            else:
                new_data = pd.DataFrame([{"Car Name": new_name, "Rating": new_rating, "Notes": new_note}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                # Update using the direct link
                conn.update(spreadsheet=SHEET_URL, data=updated_df)
                st.success("Saved! Refreshing...")
                st.rerun()
