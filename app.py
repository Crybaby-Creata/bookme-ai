import streamlit as st
import pandas as pd
import openai
from datetime import datetime
from ai import generate_reply, generate_followup, extract_lead_info
from styles import load_styles

st.set_page_config(page_title="TradeLead AI", layout="wide")
st.markdown(load_styles(), unsafe_allow_html=True)

st.title("🏗️ TradeLead AI")
st.subheader("Lead handling for construction businesses")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load data
df = pd.read_csv("data/leads.csv")

# =========================
# ADD NEW ENQUIRY
# =========================
st.markdown("## ➕ Add New Enquiry")

pasted_message = st.text_area("Paste WhatsApp Enquiry Here")

auto_name = auto_location = ""

if pasted_message:
    extracted = extract_lead_info(pasted_message)
    auto_name = extracted.get("name", "")
    auto_location = extracted.get("location", "")

with st.form("new_lead"):
    name = st.text_input("Client Name", value=auto_name)
    phone = st.text_input("Phone / WhatsApp Number")
    job = st.selectbox("Job Type", [
        "Roofing", "Tiling", "Building", "Renovation",
        "Plumbing", "Electrical", "Other"
    ])
    location = st.text_input("Job Location", value=auto_location)

    submitted = st.form_submit_button("Add Lead")

    if submitted:
        new_row = {
            "Name": name,
            "Phone": phone,
            "JobType": job,
            "Location": location,
            "Message": pasted_message,
            "Status": "New",
            "LastContacted": ""
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("data/leads.csv", index=False)
        st.success("Lead added")

st.divider()

# =========================
# DASHBOARD
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df))
col2.metric("New", len(df[df.Status == "New"]))
col3.metric("Won", len(df[df.Status == "Won"]))

st.divider()

# =========================
# LEAD INBOX
# =========================
st.markdown("## 📥 Client Enquiries")
st.dataframe(df, use_container_width=True)

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

# =========================
# AI REPLY
# =========================
if st.button("Reply to Client"):
    st.session_state.reply = generate_reply(lead.Message)

if "reply" in st.session_state:
    st.text_area("Reply Message", st.session_state.reply, height=100)
    st.code(st.session_state.reply, language="text")

# =========================
# FOLLOW-UP SYSTEM
# =========================
st.divider()
st.markdown("## 🔁 Follow-Up")

if lead.LastContacted:
    last = datetime.fromisoformat(lead.LastContacted)
    days = (datetime.now() - last).days
else:
    days = 99

if days >= 2:
    st.warning("Follow-up recommended")

    if st.button("Generate Follow-Up"):
        followup = generate_followup(lead.Name)
        st.text_area("Follow-Up Message", followup, height=80)

        df.at[lead_index, "LastContacted"] = datetime.now().isoformat()
        df.at[lead_index, "Status"] = "Follow-up"
        df.to_csv("data/leads.csv", index=False)
