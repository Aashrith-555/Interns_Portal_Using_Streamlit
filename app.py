# app.py

import streamlit as st
from feedback_form import show_feedback_form
from dashboard import show_dashboard

st.set_page_config(page_title="Internship Feedback App", page_icon="📝", layout="wide")

def main():
    st.sidebar.title("📍 Navigation")
    page = st.sidebar.radio("Go to", ["Feedback Form", "Dashboard"])

    if page == "Feedback Form":
        show_feedback_form()
    elif page == "Dashboard":
        show_dashboard()

if __name__ == "__main__":
    main()
