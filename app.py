import streamlit as st
import pandas as pd
import openai
from ai import generate_reply, generate_followup
from styles import load_styles

st.set_page_config(page_title="TradeLead AI", layout="wide")
st.markdown(load_styles(), unsafe_allow_html=True)

st.title("🏗️ TradeLead AI")
st.subheader("Lead handling for construction businesses")

openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Load leads
df = pd.read_csv("data/leads.csv")

# =========================
# 📥 ADD NEW ENQUIRY
# =========================
st.markdown("## ➕ Add New Enquiry")

with st.form("new_lead"):
    name = st.text_input("Client Name")
    phone = st.text_input("Phone / WhatsApp Number")
    job = st.selectbox("Job Type", [
        "Roofing", "Tiling", "Building", "Renovation", "Plumbing", "Electrical", "Other"
    ])
    location = st.text_input("Job Location")
    message = st.text_area("Paste WhatsApp Enquiry Here")

    submitted = st.form_submit_button("Add Lead")

    if submitted:
        new_row = {
            "Name": name,
            "Phone": phone,
            "JobType": job,
            "Location": location,
            "Message": message,
            "Status": "New"
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("data/leads.csv", index=False)
        st.success("Lead added successfully!")

st.divider()

# =========================
# 📊 DASHBOARD
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df))
col2.metric("New Leads", len(df[df.Status == "New"]))
col3.metric("Jobs Won", len(df[df.Status == "Won"]))

st.divider()

# =========================
# 📥 LEAD INBOX
# =========================
st.markdown("## 📥 Lead Inbox")
st.dataframe(df, use_container_width=True)

st.divider()

# =========================
# 🧠 LEAD ACTIONS
# =========================
lead_index = st.selectbox("Select a lead", df.index)
lead = df.loc[lead_index]

st.markdown(f"""
<div class="block">
<b>Name:</b> {lead.Name}<br>
<b>Job:</b> {lead.JobType}<br>
<b>Location:</b> {lead.Location}<br>
<b>Message:</b> {lead.Message}
</div>
""", unsafe_allow_html=True)

if st.button("Generate AI Reply"):
    reply = generate_reply(lead.Message)
    st.text_area("AI Reply", reply, height=100)

if st.button("Generate Follow-Up"):
    followup = generate_followup(lead.Name)
    st.text_area("Follow-Up Message", followup, height=80)

status = st.selectbox(
    "Update Status",
    ["New", "Replied", "Follow-up", "Won", "Lost"],
    index=["New", "Replied", "Follow-up", "Won", "Lost"].index(lead.Status)
)

if st.button("Save Status"):
    df.at[lead_index, "Status"] = status
    df.to_csv("data/leads.csv", index=False)
    st.success("Status updated")

