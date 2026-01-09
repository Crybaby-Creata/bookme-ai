import streamlit as st
import pandas as pd
from datetime import datetime
from ai import generate_reply
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="BookMe AI – Construction CRM",
    layout="wide"
)

DATA_PATH = "data/leads.csv"

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background-color: #0f0f0f; }
h1, h2, h3 { color: #FFD400; }
.stButton button {
    background-color: #FFD400;
    color: black;
    font-weight: bold;
}
.card {
    background-color: #1a1a1a;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.small { color: #aaa; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
if not os.path.exists(DATA_PATH):
    os.makedirs("data", exist_ok=True)
    pd.DataFrame(columns=[
        "Name", "Phone", "JobType", "Location",
        "Message", "Status", "LastContacted"
    ]).to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

# ---------------- HEADER ----------------
st.title("🏗️ BookMe AI")
st.subheader("Never miss a construction lead again")

# ---------------- SESSION STATE ----------------
if "reply" not in st.session_state:
    st.session_state.reply = ""

# ---------------- LEAD LIST ----------------
st.markdown("## 📥 Incoming Leads")

if df.empty:
    st.info("No leads yet.")
else:
    for idx, lead in df.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f"### {lead['Name']} — {lead['JobType']}")
            st.markdown(f"📍 {lead['Location']} | 📞 {lead['Phone']}")
            st.markdown(f"💬 *{lead['Message']}*")

            # ----- FOLLOW-UP LOGIC -----
            needs_followup = True
            if isinstance(lead["LastContacted"], str) and lead["LastContacted"].strip():
                last = datetime.fromisoformat(lead["LastContacted"])
                days = (datetime.now() - last).days
                needs_followup = days >= 2

            if needs_followup:
                st.warning("⚠️ Needs follow-up")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✍️ Generate Reply", key=f"gen_{idx}"):
                    st.session_state.reply = generate_reply(lead["Message"])

            with col2:
                if st.button("✅ Mark Contacted", key=f"mark_{idx}"):
                    df.at[idx, "LastContacted"] = datetime.now().isoformat()
                    df.at[idx, "Status"] = "Replied"
                    df.to_csv(DATA_PATH, index=False)
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------- REPLY BOX ----------------
st.markdown("## 📤 Reply Draft")

if st.session_state.reply:
    st.text_area(
        "AI-generated reply (copy & send via WhatsApp/SMS):",
        st.session_state.reply,
        height=120
    )
else:
    st.caption("Click 'Generate Reply' on a lead")

# ---------------- ADD LEAD ----------------
st.markdown("## ➕ Add Lead Manually")

with st.form("add_lead"):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    job = st.text_input("Job Type (Roofing, Plumbing, etc)")
    location = st.text_input("Location")
    message = st.text_area("Client Message")

    submitted = st.form_submit_button("Add Lead")

    if submitted:
        new_row = {
            "Name": name or "Unknown",
            "Phone": phone,
            "JobType": job,
            "Location": location,
            "Message": message,
            "Status": "New",
            "LastContacted": ""
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success("Lead added")
        st.rerun()
