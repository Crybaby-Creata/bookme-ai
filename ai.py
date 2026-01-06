import openai

def generate_reply(message):
    prompt = f"""
You are an assistant for a construction business.
Write a short, professional reply to this enquiry:

"{message}"

Ask for:
- job details
- site location
- preferred time

Keep it practical and friendly.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )
    return response.choices[0].message.content.strip()


def generate_followup(name):
    return f"Hi {name}, just following up to see if you still need help with the job. Let me know 👍"
