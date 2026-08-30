from ticket_processor import create_ticket, process_ticket


def main():
    print("AI IT Support Automation Lab")
    print("----------------------------")

    sender = input("\nSender: ")
    subject = input("Subject: ")
    body = input("Issue description: ")

    ticket = create_ticket(
        sender=sender,
        subject=subject,
        body=body
    )

    result = process_ticket(ticket)

    analysis = result["analysis"]

    print("\nTICKET ANALYSIS")
    print("----------------")

    print(f"Category: {analysis['category']}")
    print(f"Priority: {analysis['priority']}")

    print("\nLikely Causes:")
    for cause in analysis["likely_causes"]:
        print(f"- {cause}")

    print("\nTroubleshooting Steps:")
    for number, step in enumerate(
        analysis["troubleshooting_steps"],
        start=1
    ):
        print(f"{number}. {step}")


if __name__ == "__main__":
    main()