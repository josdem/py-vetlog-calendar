import os.path

from google.oauth2.credentials import Credentials

CREDENTIALS_PATH = "/home/josdem/.calendar/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class Reader:
    def listing_events(self):
        print("Listing events")
        creds = None
        if os.path.exists(CREDENTIALS_PATH):
            creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH, SCOPES)
        if not creds or not creds.valid:
            print("No valid credentials")
