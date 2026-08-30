import json
import ollama


TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [
                "Network",
                "Authentication",
                "Hardware",
                "Software",
                "Printer",
                "Security",
                "Email",
                "Other"
            ]
        },
        "priority": {
            "type": "string",
            "enum": ["Low", "Medium", "High", "Critical"]
        },
        "likely_causes": {
            "type": "array",
            "items": {"type": "string"}
        },
        "follow_up_questions": {
            "type": "array",
            "items": {"type": "string"}
        },
        "troubleshooting_steps": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "category",
        "priority",
        "likely_causes",
        "follow_up_questions",
        "troubleshooting_steps"
    ]
}


SYSTEM_PROMPT = """
You are a Tier 1 IT support ticket analysis assistant.

Analyze the technical issue described by the user.

Return only information required by the JSON schema.

Base your analysis only on information contained in the ticket.
"""


def analyze_ticket(ticket_text):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ticket_text,
            },
        ],
        format=TICKET_SCHEMA,
        options={
            "temperature": 0
        }
    )

    return json.loads(response["message"]["content"])