from outlook_reader import read_outlook_emails


def main():
    emails = read_outlook_emails(
        limit=5
    )

    print(
        f"Emails retrieved: {len(emails)}"
    )

    for email in emails:
        print("\n" + "=" * 60)
        print(
            f"From: {email['sender']}"
        )
        print(
            f"Subject: {email['subject']}"
        )
        print(
            f"Received: {email['received_at']}"
        )
        print(
            f"Read: {email['is_read']}"
        )

        print("\nBODY")
        print(
            email["body"][:500]
        )


if __name__ == "__main__":
    main()