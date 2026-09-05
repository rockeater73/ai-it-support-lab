import os

import msal
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
TENANT_ID = os.getenv("MICROSOFT_TENANT_ID", "common")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = [
    "Mail.Read"
]


def get_access_token():
    if not CLIENT_ID:
        raise ValueError(
            "MICROSOFT_CLIENT_ID is missing from the .env file."
        )

    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY
    )

    accounts = app.get_accounts()

    if accounts:
        result = app.acquire_token_silent(
            SCOPES,
            account=accounts[0]
        )
    else:
        result = None

    if not result:
        flow = app.initiate_device_flow(
            scopes=SCOPES
        )

        if "user_code" not in flow:
            raise RuntimeError(
                f"Unable to start device login: {flow}"
            )

        print(flow["message"])

        result = app.acquire_token_by_device_flow(
            flow
        )

    if "access_token" not in result:
        raise RuntimeError(
            "Authentication failed: "
            + result.get(
                "error_description",
                str(result)
            )
        )

    return result["access_token"]