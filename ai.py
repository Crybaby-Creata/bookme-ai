from openai import OpenAI

client = OpenAI()

def generate_reply(message):
    prompt = f"""
You are a professional construction business owner.
Reply politely, clearly, and briefly to this customer enquiry:

"{message}"

Offer to provide a quote or next steps.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=120
    )

    return response.choices[0].message.content.strip()

