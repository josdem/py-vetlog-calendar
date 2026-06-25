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

from .config import get_settings
from .medical_helper import is_medical_event

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class Calendar:
    def __init__(self):
        self.settings = get_settings()
        self.token_path = self.settings.TOKEN_PATH
        self.credentials_path = self.settings.CREDENTIALS_PATH
        self.creds = None

    def _ensure_credentials(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not self.creds or not self.creds.valid:
            print("No valid credentials")
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

    def create_event(self, event: dict):
        print("Creating event")
        self._ensure_credentials()
        try:
            service = build("calendar", "v3", credentials=self.creds)
            service.events().insert(calendarId="primary", body=event).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def list_surgeries(self) -> list:
        """Listing surgeries from the previous 7 days"""
        self._ensure_credentials()
        try:
            service = build("calendar", "v3", credentials=self.creds)
            yesterday = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)
            week_ago = yesterday - datetime.timedelta(days=8)
            print(f"Fetching surgeries from: {week_ago} to {yesterday}")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=week_ago.isoformat(),
                    timeMax=yesterday.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            surgeries = [
                event for event in events if is_medical_event(event.get("summary", ""))
            ]
            return surgeries
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
