#  Copyright 2026 Jose Morales contact@josdem.io
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os.path
import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import Settings

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class Calendar:
    def create_event(self, event: dict):
        print("Creating event")
        settings = Settings()
        token_path = settings.TOKEN_PATH
        credentials_path = settings.CREDENTIALS_PATH
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            print("No valid credentials")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        try:
            service = build("calendar", "v3", credentials=creds)
            service.events().insert(calendarId="primary", body=event).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")

    def list_surgeries(self):
        print("Listing surgeries from the previous 7 days")
        settings = Settings()
        token_path = settings.TOKEN_PATH
        credentials_path = settings.CREDENTIALS_PATH
        creds = None

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            print("No valid credentials")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)

            now = datetime.datetime.now(datetime.UTC)
            seven_days_ago = now - datetime.timedelta(days=7)

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=seven_days_ago.isoformat(),
                    timeMax=now.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            surgeries = [
                event
                for event in events
                if self._is_surgery(event.get("summary", ""))
            ]

            for event in surgeries:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")

    def _is_surgery(self, title: str) -> bool:
        title = title.lower()
        return "surgery" in title or "cirugia" in title or "cirugía" in title