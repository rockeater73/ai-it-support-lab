import json
import ollama


TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string"
        },
        "priority": {
            "type": "string",
            "enum": ["Low", "Medium", "High", "Critical"]
        },
        "likely_causes": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "follow_up_questions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "troubleshooting_steps": {
            "type": "array",
            "items": {
                "type": "string"
            }
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


def get_it_support_response(ticket_text):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an IT support assistant. "
                    "Analyze the support ticket and return only the information "
                    "required by the provided JSON schema. "
                    "Do not invent facts that are not supported by the ticket."
                ),
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


def display_analysis(analysis):
    print("\nIT SUPPORT ANALYSIS")
    print("-------------------")

    print(f"\nCategory: {analysis['category']}")
    print(f"Priority: {analysis['priority']}")

    print("\nLikely Causes:")
    for cause in analysis["likely_causes"]:
        print(f"- {cause}")

    print("\nFollow-up Questions:")
    for question in analysis["follow_up_questions"]:
        print(f"- {question}")

    print("\nTroubleshooting Steps:")
    for number, step in enumerate(
        analysis["troubleshooting_steps"],
        start=1
    ):
        print(f"{number}. {step}")


def main():
    print("AI IT Support Lab")
    print("-----------------")

    ticket = input("\nEnter an IT support ticket:\n> ")

    if not ticket.strip():
        print("\nError: Ticket cannot be empty.")
        return

    print("\nAnalyzing ticket...")

    try:
        analysis = get_it_support_response(ticket)
        display_analysis(analysis)

    except json.JSONDecodeError:
        print("\nError: The model returned invalid JSON.")

    except Exception as error:
        print(f"\nError communicating with Ollama: {error}")


if __name__ == "__main__":
    main()
