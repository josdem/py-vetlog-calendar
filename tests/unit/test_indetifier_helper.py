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

from vetlog_calendar.shared.identifier_helper import get_vetlog_id


def test_get_vetlog_id():

    event = {
        "summary": "Jose - Vaccination appointment for Sora",
        "location": "Whatever works for you",
        "description": """Jose Morales\n1234567890\n\nVetlogID: 338\nSurgery appointment for Sora\nVaccine type: C6CV\n\nThank you for trusting Vetlog!\nhttps://vetlog.org/""",
        "start": {
            "dateTime": "2026-05-21T11:00:00-06:00",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": "2026-05-21T11:15:00-06:00",
            "timeZone": "UTC",
        },
        "attendees": [
            {"email": "contact@josdem.io"},
            {"email": "email1@example.com"},
            {"email": "email2@example.com"},
            {"email": "email3@example.com"},
        ],
    }

    assert get_vetlog_id(event["description"]) == "338"


def test_get_vetlog_id_not_found():

    event = {
        "summary": "Jose - Vaccination appointment for Sora",
        "location": "Whatever works for you",
        "description": """Jose Morales\n1234567890\n\nSurgery appointment for Sora\nVaccine type: C6CV\n\nThank you for trusting Vetlog!\nhttps://vetlog.org/""",
        "start": {
            "dateTime": "2026-05-21T11:00:00-06:00",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": "2026-05-21T11:15:00-06:00",
            "timeZone": "UTC",
        },
        "attendees": [
            {"email": "contact@josdem.io"},
            {"email": "email1@example.com"},
            {"email": "email2@example.com"},
            {"email": "email3@example.com"},
        ],
    }

    try:
        get_vetlog_id(event["description"])
        assert False, "Expected ValueError not raised"
    except ValueError:
        pass
