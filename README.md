# Internship Feedback System

This is a **Streamlit-based web application** that collects and analyzes feedback from interns. It integrates with **Google Sheets** to store feedback data and provides a **real-time dashboard** to visualize insights like average ratings, distribution charts, and top keywords.

---

##  Features

-  Interactive feedback form for interns
-  Feedback stored directly in Google Sheets
-  Dashboard with:
  - Total feedback entries
  - Average rating (overall and by college)
  - Rating distribution pie chart
  - Top keywords from experience descriptions
-  Clean, modular structure with `app.py`, `feedback_form.py`, and `dashboard.py`

---

##  Folder Structure
- app.py
- feedback_from.py
- dashboard.py
- credentials.json

## Installations and Dependencies
- pip install streamlit gspread oauth2client pandas matplotlib wordcloud
- Google Sheet API Setup
- Google Sheet
