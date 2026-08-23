import ollama


def get_it_support_response(ticket_text):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an IT support assistant. "
                    "Analyze the user's support ticket and provide a concise response with: "
                    "1. Issue category, "
                    "2. Priority level, "
                    "3. Likely causes, "
                    "4. Follow-up questions, and "
                    "5. Troubleshooting steps."
                ),
            },
            {
                "role": "user",
                "content": ticket_text,
            },
        ],
    )

    return response["message"]["content"]


def main():
    print("AI IT Support Lab")
    print("-----------------")

    ticket = input("\nEnter an IT support ticket:\n> ")

    if not ticket.strip():
        print("\nError: Ticket cannot be empty.")
        return

    print("\nAnalyzing ticket...\n")

    try:
        response = get_it_support_response(ticket)
        print(response)

    except Exception as error:
        print(f"Error communicating with Ollama: {error}")
        print(
            "\nMake sure Ollama is running and that you have downloaded "
            "the llama3 model with: ollama run llama3"
        )


if __name__ == "__main__":
    main()