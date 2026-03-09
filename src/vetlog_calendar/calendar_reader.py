import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_PATH = "/home/josdem/.calendar/token.json"
CREDENTIALS_PATH = "/home/josdem/.calendar/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class Reader:
    def listing_events(self):
        print("Listing events")
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            print("No valid credentials")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
