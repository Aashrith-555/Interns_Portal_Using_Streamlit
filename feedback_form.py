# feedback_form.py

import os
from PIL import Image
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
SHEET_NAME = "Internship Feedback"

@st.cache_resource
def get_gsheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

def append_feedback(data):
    sheet = get_gsheet()
    row = [
        data["Name"],
        data["College"],
        data["Email"],
        data["Mentor"],
        data["Experience"],
        data["Rating"],
        data["Suggestions"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    sheet.append_row(row)

def show_feedback_form():
    st.title("📝 Internship Feedback Form")
    st.markdown("Please provide your feedback about the internship program.")

    with st.form("feedback_form"):
        name = st.text_input("Full Name", max_chars=50)
        college = st.text_input("College Name", max_chars=100)
        email = st.text_input("Email ID")
        mentor = st.text_input("Mentor Name (optional)")
        experience = st.text_area("Your Internship Experience", height=120)
        rating = st.selectbox("Overall Rating", options=["", "5", "4", "3", "2", "1"])
        suggestions = st.text_area("Suggestions (Optional)", height=80)
        submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if not name or not college or not email or not experience or rating == "":
            st.error("⚠️ Please fill in all the required fields.")
        else:
            feedback_data = {
                "Name": name,
                "College": college,
                "Email": email,
                "Mentor": mentor,
                "Experience": experience,
                "Rating": rating,
                "Suggestions": suggestions,
            }
            try:
                append_feedback(feedback_data)
                st.success(f"✅ Thank you for your feedback, {name}!")
                st.balloons()
            except Exception as e:
                st.error("❌ Failed to submit feedback.")
                st.code(str(e))
