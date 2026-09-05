import requests

from graph_auth import get_access_token


GRAPH_MESSAGES_URL = (
    "https://graph.microsoft.com/v1.0/"
    "me/mailFolders/inbox/messages"
)


def read_outlook_emails(limit=5):
    access_token = get_access_token()

    headers = {
    "Authorization": f"Bearer {access_token}",
    "Prefer": 'outlook.body-content-type="text"'
}

    params = {
        "$top": limit,
        "$select": (
            "id,subject,from,body,"
            "receivedDateTime,isRead"
        ),
        "$orderby": "receivedDateTime desc"
    }

    response = requests.get(
        GRAPH_MESSAGES_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    messages = response.json().get(
        "value",
        []
    )

    emails = []

    for message in messages:
        sender = (
            message.get("from", {})
            .get("emailAddress", {})
            .get("address", "")
        )

        emails.append({
            "id": message["id"],
            "sender": sender,
            "subject": message.get(
                "subject",
                ""
            ),
            "body": (
                message.get("body", {})
                .get("content", "")
            ),
            "received_at": message.get(
                "receivedDateTime"
            ),
            "is_read": message.get(
                "isRead"
            )
        })

    return emails