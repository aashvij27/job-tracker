import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE_NAME = "jobs.csv"

# Load data
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        df = pd.DataFrame(columns=[
            "Company", "Role", "Location", "Source",
            "Date Applied", "Expected Salary",
            "Status", "Response", "Notes"
        ])
        df.to_csv(FILE_NAME, index=False)
        return df

# Save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# UI
st.title("📊 Job Application Tracker")

df = load_data()

# --- Add Job ---
st.header("Add New Job")

with st.form("job_form"):
    company = st.text_input("Company")
    role = st.text_input("Role")
    location = st.text_input("Location")
    source = st.selectbox("Source", ["LinkedIn", "Naukri", "Company Site", "Other"])
    salary = st.text_input("Expected Salary")
    notes = st.text_input("Notes")

    submitted = st.form_submit_button("Add Job")

    if submitted:
        new_row = {
            "Company": company,
            "Role": role,
            "Location": location,
            "Source": source,
            "Date Applied": datetime.now().strftime("%Y-%m-%d"),
            "Expected Salary": salary,
            "Status": "Applied",
            "Response": "No",
            "Notes": notes
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Job added!")

# --- Dashboard ---
st.header("Overview")

total = len(df)
responses = len(df[df["Response"] == "Yes"])
offers = len(df[df["Status"] == "Offer"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", total)
col2.metric("Responses", responses)
col3.metric("Offers", offers)

# --- Filters ---
st.header("Filter Jobs")

status_filter = st.selectbox("Filter by Status", ["All"] + list(df["Status"].unique()))

filtered_df = df if status_filter == "All" else df[df["Status"] == status_filter]

st.dataframe(filtered_df)

# --- Update Status ---
st.header("Update Job")

if not df.empty:
    index = st.number_input("Select Row Index", min_value=0, max_value=len(df)-1, step=1)

    new_status = st.selectbox("New Status", ["Applied", "Interview", "Rejected", "Offer"])
    response = st.selectbox("Response", ["Yes", "No"])

    if st.button("Update"):
        df.at[index, "Status"] = new_status
        df.at[index, "Response"] = response
        save_data(df)
        st.success("Updated!")