from email_reader import read_mock_emails
from ticket_processor import create_ticket, process_ticket
from escalation_rules import determine_escalation


def process_inbox():
    emails = read_mock_emails()

    print("AI IT SUPPORT AUTOMATION")
    print("=" * 50)
    print(f"Emails found: {len(emails)}")

    tier1_count = 0
    escalated_count = 0

    for email in emails:
        print("\n" + "=" * 50)
        print(f"Processing: {email['id']}")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")

        ticket = create_ticket(
            sender=email["sender"],
            subject=email["subject"],
            body=email["body"]
        )

        try:
            result = process_ticket(ticket)
            analysis = result["analysis"]

            routing = determine_escalation(analysis)

            print("\nAI ANALYSIS")
            print(f"Category: {analysis['category']}")
            print(f"Priority: {analysis['priority']}")

            print("\nROUTING")
            print(f"Assigned to: {routing['assigned_tier']}")
            print(f"Escalated: {routing['escalate']}")
            print(f"Reason: {routing['reason']}")

            if routing["escalate"]:
                escalated_count += 1
            else:
                tier1_count += 1

            print("\nTroubleshooting Steps:")

            for number, step in enumerate(
                analysis["troubleshooting_steps"],
                start=1
            ):
                print(f"{number}. {step}")

        except Exception as error:
            print(f"\nERROR: {error}")

    print("\n" + "=" * 50)
    print("INBOX SUMMARY")
    print("=" * 50)
    print(f"Emails processed: {len(emails)}")
    print(f"Tier 1 tickets: {tier1_count}")
    print(f"Escalated tickets: {escalated_count}")


if __name__ == "__main__":
    process_inbox()