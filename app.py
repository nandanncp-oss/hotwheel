import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="🏎️ HW Rater", page_icon="🔥")

st.title("🔥 Hot Wheels Rater")
st.write("The shared database for you and your friend.")

# 2. Connect to Google Sheets
# We use the built-in connection to grab your data live
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Sheet1", usecols=[0, 1, 2], ttl=5) # ttl=5 ensures updates appear quickly
    # Ensure data is treated as a clean DataFrame
    df = pd.DataFrame(data)
except Exception as e:
    st.error("Could not connect to database. Make sure your Secrets are set up!")
    st.stop()

# 3. Create Tabs for "Search" and "Add"
tab1, tab2 = st.tabs(["🔍 Find Rating", "➕ Add New Car"])

# --- TAB 1: FIND A CAR ---
with tab1:
    st.header("Check a Hot Wheel")
    search_term = st.text_input("Type car name:", placeholder="e.g. Bone Shaker").lower().strip()

    if search_term:
        # Filter the data (case insensitive search)
        # We convert the 'Car Name' column to string and lowercase to match
        results = df[df['Car Name'].astype(str).str.lower().str.contains(search_term, na=False)]

        if not results.empty:
            st.success(f"Found {len(results)} match(es):")
            for index, row in results.iterrows():
                # Display the result in a nice card
                with st.container(border=True):
                    st.subheader(row['Car Name'])
                    st.write(f"**Rating:** {row['Rating']}/10")
                    st.write(f"**Notes:** {row['Notes']}")
        else:
            st.warning("No rating found for this car yet.")

# --- TAB 2: ADD A RATING ---
with tab2:
    st.header("Rate a New Car")
    with st.form("rating_form"):
        new_name = st.text_input("Car Name")
        new_rating = st.slider("Rating (1-10)", 1, 10, 5)
        new_note = st.text_area("Notes (Rare? Fast? Cool paint?)")
        
        submitted = st.form_submit_button("Save Rating")
        
        if submitted and new_name:
            # Check if already exists to prevent duplicates (optional logic)
            if new_name.lower() in df['Car Name'].astype(str).str.lower().values:
                st.error(f"'{new_name}' is already in the list! Check the Search tab.")
            else:
                # Create a new row
                new_data = pd.DataFrame([{"Car Name": new_name, "Rating": new_rating, "Notes": new_note}])
                
                # Update the google sheet
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.success(f"Saved! {new_name} is now rated {new_rating}/10.")
                st.rerun() # Refresh app to show new data immediately