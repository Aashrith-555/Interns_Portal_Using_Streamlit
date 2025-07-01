import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from collections import Counter

# --- Google Sheets Setup ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
SHEET_NAME = "Internship Feedback"

@st.cache_resource
def get_gsheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    data = sheet.get_all_records()
    if not data:
        st.error("❌ No data found in the Google Sheet.")
        st.stop()
    return sheet

def load_data():
    sheet = get_gsheet()
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def show_dashboard():
    st.set_page_config(page_title="Internship Feedback Dashboard", layout="wide")
    st.title("📊 Internship Feedback Dashboard")

    df = load_data()

    if df.empty:
        st.warning("No feedback entries found.")
    else:
        # Total feedback count
        st.metric("Total Feedback Entries", len(df))

        # Raw data preview
        st.subheader("📋 Raw Data Preview")
        st.write(df.head())

        # Average rating
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        avg_rating = df['Rating'].mean()
        st.metric("Average Rating", f"{avg_rating:.2f} / 5")

        # Average rating by college
        st.subheader("🏫 Average Rating by College")
        avg_by_college = df.groupby("College")['Rating'].mean().sort_values(ascending=False)
        st.dataframe(avg_by_college.reset_index().rename(columns={"Rating": "Avg. Rating"}))

        # Rating distribution pie chart
        st.subheader("📈 Rating Distribution")
        rating_counts = df['Rating'].value_counts().sort_index()
        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots()
            ax1.pie(
                rating_counts,
                labels=rating_counts.index,
                autopct='%1.1f%%',
                startangle=90
            )
            ax1.axis('equal')
            st.pyplot(fig1)

        # Top keywords from experience
        with col2:
            all_text = " ".join(df['Experience'].dropna().astype(str))
            words = [word.lower() for word in all_text.split() if len(word) > 3]
            common_words = Counter(words).most_common(10)
            keywords = [word for word, count in common_words]
            st.markdown("**Top Keywords in Experience:**")
            block_html = "<div style='display:flex; flex-wrap:wrap; gap:8px;'>"
            for kw in keywords:
                block_html += f"""
                    <div style='width:60px; height:60px; background:#e0e0e0; color:#333; border-radius:8px;
                                display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:bold;'>
                        {kw}
                    </div>
                """
            block_html += "</div>"
            st.markdown(block_html, unsafe_allow_html=True)
