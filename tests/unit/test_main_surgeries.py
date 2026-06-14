import pytest
from unittest.mock import MagicMock, patch
from vetlog_calendar.main import list_surgeries_without_logs
from vetlog_calendar.pets.model import PetLog


@pytest.fixture
def mock_surgery_events():
    return [
        {
            "summary": "Jose - Surgery for Sora",
            "pet_id": 1,
            "start": {"dateTime": "2026-06-01T11:00:00-06:00"},
        },
        {
            "summary": "Jose - Cirugía para Luna",
            "pet_id": 2,
            "start": {"dateTime": "2026-06-02T11:00:00-06:00"},
        },
    ]


def test_list_surgeries_without_logs_returns_surgeries_with_no_logs(
    mock_surgery_events,
):
    """Surgeries with no medical logs in the period are listed"""
    mock_calendar = MagicMock()
    mock_calendar.list_surgeries.return_value = mock_surgery_events

    mock_service = MagicMock()
    mock_service.get_logs_by_date_range.return_value = []  # no logs

    mock_event = {"summary": "Missing pet logs event"}
    mock_helper_instance = MagicMock()
    mock_helper_instance.get_missing_pet_logs_event.return_value = mock_event

    with (
        patch("vetlog_calendar.main.get_session"),
        patch(
            "vetlog_calendar.main.Helper", return_value=mock_helper_instance
        ) as mock_helper_cls,
    ):
        list_surgeries_without_logs(calendar=mock_calendar, service=mock_service)

    mock_calendar.list_surgeries.assert_called_once()
    mock_service.get_logs_by_date_range.assert_called_once()
    mock_helper_cls.assert_called_once_with(
        pet=None, vaccination=None, owner=None, language="en"
    )
    mock_helper_instance.get_missing_pet_logs_event.assert_called_once_with(
        mock_surgery_events
    )
    mock_calendar.create_event.assert_called_once_with(mock_event)


def test_list_surgeries_without_logs_uses_selected_language(mock_surgery_events):
    """Helper is created with the selected language when no logs are found"""
    mock_calendar = MagicMock()
    mock_calendar.list_surgeries.return_value = mock_surgery_events

    mock_service = MagicMock()
    mock_service.get_logs_by_date_range.return_value = []  # no logs

    mock_helper_instance = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session"),
        patch(
            "vetlog_calendar.main.Helper", return_value=mock_helper_instance
        ) as mock_helper_cls,
    ):
        list_surgeries_without_logs(
            calendar=mock_calendar, service=mock_service, language="es"
        )

    mock_helper_cls.assert_called_once_with(
        pet=None, vaccination=None, owner=None, language="es"
    )
    mock_helper_instance.get_missing_pet_logs_event.assert_called_once_with(
        mock_surgery_events
    )
    mock_calendar.create_event.assert_called_once()


def test_list_surgeries_without_logs_excludes_surgeries_with_logs(mock_surgery_events):
    """Surgeries that have a matching medical log are excluded"""
    mock_calendar = MagicMock()
    mock_calendar.list_surgeries.return_value = mock_surgery_events

    log = MagicMock(spec=PetLog)
    log.pet_id = 1  # pet 1 has a log

    mock_service = MagicMock()
    mock_service.get_logs_by_date_range.return_value = [log]

    with patch("vetlog_calendar.main.get_session"):
        list_surgeries_without_logs(calendar=mock_calendar, service=mock_service)

    mock_calendar.list_surgeries.assert_called_once()
    mock_calendar.create_event.assert_not_called()


def test_list_surgeries_without_logs_empty_when_all_have_logs(mock_surgery_events):
    """No surgeries returned when all have matching logs"""
    mock_calendar = MagicMock()
    mock_calendar.list_surgeries.return_value = mock_surgery_events

    logs = [MagicMock(spec=PetLog, pet_id=1), MagicMock(spec=PetLog, pet_id=2)]

    mock_service = MagicMock()
    mock_service.get_logs_by_date_range.return_value = logs

    with patch("vetlog_calendar.main.get_session"):
        list_surgeries_without_logs(calendar=mock_calendar, service=mock_service)

    mock_calendar.list_surgeries.assert_called_once()
    mock_calendar.create_event.assert_not_called()
