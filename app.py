import streamlit as st
import pandas as pd
import openai
from ai import generate_reply, generate_followup
from styles import load_styles

st.set_page_config(page_title="TradeLead AI", layout="wide")
st.markdown(load_styles(), unsafe_allow_html=True)

st.title("🏗️ TradeLead AI")
st.subheader("Lead handling for construction businesses")

openai.api_key = st.sidebar.text_input("OpenAI API Key", type="password")

df = pd.read_csv("data/leads.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df))
col2.metric("New Leads", len(df[df.Status == "New"]))
col3.metric("Jobs Won", len(df[df.Status == "Won"]))

st.divider()

st.markdown("### 📥 Lead Inbox")
st.dataframe(df, use_container_width=True)

st.divider()

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

status = st.selectbox("Update Status", ["New", "Replied", "Follow-up", "Won", "Lost"])
if st.button("Save Status"):
    df.at[lead_index, "Status"] = status
    df.to_csv("data/leads.csv", index=False)
    st.success("Status updated")
