import openai
import json

def extract_lead_info(message):
    prompt = f"""
Extract details from this construction enquiry.

Return JSON ONLY in this format:
{{
  "name": "",
  "job_type": "",
  "location": ""
}}

Message:
"{message}"
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    try:
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"name": "", "job_type": "", "location": ""}


def generate_reply(message):
    prompt = f"""
You are a professional construction contractor.
Reply clearly and briefly to this enquiry:

"{message}"

Ask for:
- job details
- location
- best time to call
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )
    return response.choices[0].message.content.strip()


def generate_followup(name):
    name = name if name else "there"
    return f"Hi {name}, just checking in to see if you still need help with the job. Let me know 👍"


