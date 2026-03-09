import os.path


class Reader:
    def listing_events(self):
        print("Listing events")
        creds = None
        if os.path.exists("token.json"):
            print("Token file exists")
        if not creds or not creds.valid:
            print("No valid credentials")
