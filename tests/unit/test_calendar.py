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

from unittest.mock import MagicMock, mock_open, patch

import pytest

from vetlog_calendar.shared.calendar import Calendar


@pytest.fixture
def event():
    return {
        "summary": "Jose - Vaccination appointment for Sora",
        "location": "Whatever works for you",
        "description": "Jose Morales\n1234567890\n\nVaccination appointment for Sora",
        "start": {"dateTime": "2026-04-21T11:00:00-06:00", "timeZone": "UTC"},
        "end": {"dateTime": "2026-04-21T11:15:00-06:00", "timeZone": "UTC"},
    }


def test_create_event_with_valid_credentials(event):
    """Create event when token file exists with valid credentials"""
    mock_creds = MagicMock()
    mock_creds.valid = True

    mock_service = MagicMock()

    with (
        patch("vetlog_calendar.shared.calendar.get_settings") as mock_get_settings,
        patch("vetlog_calendar.shared.calendar.os.path.exists", return_value=True),
        patch(
            "vetlog_calendar.shared.calendar.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ),
        patch("vetlog_calendar.shared.calendar.build", return_value=mock_service),
    ):
        mock_get_settings.return_value.TOKEN_PATH = "/tmp/token.json"
        mock_get_settings.return_value.CREDENTIALS_PATH = "/tmp/credentials.json"

        Calendar().create_event(event)

    mock_service.events().insert.assert_called_once_with(
        calendarId="primary", body=event
    )
    mock_service.events().insert().execute.assert_called_once()


def test_create_event_refreshes_expired_credentials(event):
    """Create event when credentials are expired and a refresh token is available"""
    mock_creds = MagicMock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = "refresh-token"

    mock_service = MagicMock()

    with (
        patch("vetlog_calendar.shared.calendar.get_settings") as mock_get_settings,
        patch("vetlog_calendar.shared.calendar.os.path.exists", return_value=True),
        patch(
            "vetlog_calendar.shared.calendar.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ),
        patch("vetlog_calendar.shared.calendar.Request") as mock_request_cls,
        patch("vetlog_calendar.shared.calendar.build", return_value=mock_service),
        patch("builtins.open", mock_open()),
    ):
        mock_get_settings.return_value.TOKEN_PATH = "/tmp/token.json"
        mock_get_settings.return_value.CREDENTIALS_PATH = "/tmp/credentials.json"

        Calendar().create_event(event)

    mock_creds.refresh.assert_called_once_with(mock_request_cls.return_value)
    mock_service.events().insert.assert_called_once_with(
        calendarId="primary", body=event
    )


def test_create_event_runs_oauth_flow_when_no_token(event):
    """Create event when no token file exists, triggering the OAuth flow"""
    mock_creds = MagicMock()
    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = mock_creds

    mock_service = MagicMock()

    with (
        patch("vetlog_calendar.shared.calendar.get_settings") as mock_get_settings,
        patch("vetlog_calendar.shared.calendar.os.path.exists", return_value=False),
        patch(
            "vetlog_calendar.shared.calendar.InstalledAppFlow.from_client_secrets_file",
            return_value=mock_flow,
        ),
        patch("vetlog_calendar.shared.calendar.build", return_value=mock_service),
        patch("builtins.open", mock_open()),
    ):
        mock_get_settings.return_value.TOKEN_PATH = "/tmp/token.json"
        mock_get_settings.return_value.CREDENTIALS_PATH = "/tmp/credentials.json"

        Calendar().create_event(event)

    mock_flow.run_local_server.assert_called_once_with(port=0)
    mock_service.events().insert.assert_called_once_with(
        calendarId="primary", body=event
    )


def test_create_event_handles_http_error(event, capsys):
    """Create event logs error when an HttpError is raised"""
    from googleapiclient.errors import HttpError

    mock_creds = MagicMock()
    mock_creds.valid = True

    mock_response = MagicMock()
    mock_response.status = 403
    mock_response.reason = "Forbidden"
    http_error = HttpError(resp=mock_response, content=b"Forbidden")

    mock_service = MagicMock()
    mock_service.events().insert().execute.side_effect = http_error

    with (
        patch("vetlog_calendar.shared.calendar.get_settings") as mock_get_settings,
        patch("vetlog_calendar.shared.calendar.os.path.exists", return_value=True),
        patch(
            "vetlog_calendar.shared.calendar.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ),
        patch("vetlog_calendar.shared.calendar.build", return_value=mock_service),
    ):
        mock_get_settings.return_value.TOKEN_PATH = "/tmp/token.json"
        mock_get_settings.return_value.CREDENTIALS_PATH = "/tmp/credentials.json"

        Calendar().create_event(event)

    captured = capsys.readouterr()
    assert "An error occurred" in captured.out


def test_is_surgery_detects_english_surgery():
    """Detect surgery events in English"""
    assert Calendar()._is_surgery("Jose - Surgery appointment for Sora")


def test_is_surgery_detects_spanish_cirugia():
    """Detect surgery events in Spanish without accent"""
    assert Calendar()._is_surgery("Jose - Cirugia appointment for Sora")


def test_is_surgery_detects_spanish_cirugia_with_accent():
    """Detect surgery events in Spanish with accent"""
    assert Calendar()._is_surgery("Jose - Cirugía appointment for Sora")


def test_is_surgery_ignores_non_surgery_event():
    """Ignore events that are not surgeries"""
    assert not Calendar()._is_surgery("Jose - Vaccination appointment for Sora")


def test_list_surgeries_with_valid_credentials(capsys):
    """List surgery events from the previous 7 days"""
    mock_creds = MagicMock()
    mock_creds.valid = True

    mock_service = MagicMock()
    mock_events = mock_service.events.return_value
    mock_list = mock_events.list
    mock_list.return_value.execute.return_value = {
        "items": [
            {
                "summary": "Jose - Surgery appointment for Sora",
                "start": {"dateTime": "2026-06-01T11:00:00-06:00"},
            },
            {
                "summary": "Jose - Cita de Cirugia para Luna",
                "start": {"dateTime": "2026-06-02T11:00:00-06:00"},
            },
            {
                "summary": "Jose - Vaccination appointment for Milo",
                "start": {"dateTime": "2026-06-03T11:00:00-06:00"},
            },
        ]
    }

    with (
        patch("vetlog_calendar.shared.calendar.get_settings") as mock_get_settings,
        patch("vetlog_calendar.shared.calendar.os.path.exists", return_value=True),
        patch(
            "vetlog_calendar.shared.calendar.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ),
        patch("vetlog_calendar.shared.calendar.build", return_value=mock_service),
    ):
        mock_get_settings.return_value.TOKEN_PATH = "/tmp/token.json"
        mock_get_settings.return_value.CREDENTIALS_PATH = "/tmp/credentials.json"

        Calendar().list_surgeries()

    captured = capsys.readouterr()

    assert "Jose - Surgery appointment for Sora" in captured.out
    assert "Jose - Cita de Cirugia para Luna" in captured.out
    assert "Jose - Vaccination appointment for Milo" not in captured.out

    mock_list.assert_called_once()
    call_kwargs = mock_list.call_args.kwargs
    assert call_kwargs["calendarId"] == "primary"
    assert call_kwargs["singleEvents"] is True
    assert call_kwargs["orderBy"] == "startTime"
    assert "timeMin" in call_kwargs
    assert "timeMax" in call_kwargs
