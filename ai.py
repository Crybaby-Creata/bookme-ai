from openai import OpenAI

client = OpenAI()

def generate_reply(message: str) -> str:
    if not message:
        return "Hi, thanks for reaching out. Can you please share more details about the job?"

    prompt = f"""
You are a professional US construction contractor.
Write a short, polite, and clear reply to this customer enquiry.

Customer message:
"{message}"

Ask for next steps or offer a quote.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=120
    )

    return response.choices[0].message.content.strip()
