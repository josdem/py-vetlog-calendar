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

import os
import pytest

from unittest.mock import MagicMock, patch
from datetime import datetime

from pydantic import ValidationError

from vetlog_calendar import main
from vetlog_calendar.pets.model import Pet
from vetlog_calendar.shared.config import Settings
from vetlog_calendar.users.model import User
from vetlog_calendar.vaccinations.model import Vaccination


@pytest.fixture
def clean_env():
    with patch.dict(os.environ, {}, clear=True):
        yield


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        os.environ,
        {
            "db_host": "localhost",
            "db_name": "vetlog",
            "db_user": "vetlogUser",
            "db_password": "vetlogDB",
            "TOKEN_PATH": "path/to/token.json",
            "CREDENTIALS_PATH": "path/to/credentials.json",
            "default_emails": '["email1@example.com", "email2@example.com", "email3@example.com"]',
        },
    ):
        yield


def owner():
    return User(
        id=1,
        username="josdem",
        first_name="Jose",
        last_name="Morales",
        email="contact@josdem.io",
        mobile="1234567890",
        role="USER",
    )


def vaccination():
    return Vaccination(
        pet_id=1,
        name="Rabies",
        date=datetime(2024, 5, 21),
    )


def deworming():
    return Vaccination(
        pet_id=1,
        name="Deworming",
        date=datetime(2024, 5, 21),
    )


def pet():
    return Pet(
        id=1,
        user_id=1,
        adopter_id=None,
        name="Sora",
        birth_date=datetime(2020, 1, 1, 0, 0, 0),
        breed_id=1,
    )


def test_list_users_prints_users_with_pets_pending_vaccinations(caplog):
    """List all users with pet with pending vaccinations"""

    caplog.set_level("INFO")
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.VaccinationService.get_pending_vaccinations",
            return_value=[vaccination()],
        ),
        patch("vetlog_calendar.main.PetRepository.get_all", return_value=[pet()]),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_users()

    expected_output = (
        "josdem - Jose Morales - contact@josdem.io - Pet: Sora - awaiting vaccination"
    )
    assert expected_output in caplog.text


def test_list_vaccinations(caplog, mock_env_vars):
    """List pending vaccinations"""
    caplog.set_level("INFO")
    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()
    mock_service = MagicMock()
    vaccination_instance = vaccination()
    mock_service.get_pending_vaccinations.return_value = [vaccination_instance]

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_vaccinations(
            calendar=mock_calendar, service=mock_service, language="en"
        )

    mock_calendar.create_event.assert_called_once()
    mock_service.delete_rabies_vaccinations_for_pet.assert_called_once_with(pet().id)
    mock_service.update_vaccination_status.assert_called_once_with(vaccination_instance)

    expected_description = "Jose - Vaccination appointment for Sora"
    assert expected_description in caplog.text


def test_list_vaccinations_no_new_vaccinations_prints_message(caplog):
    """Show message when there are no NEW vaccinations to process"""

    caplog.set_level("INFO")
    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()
    mock_service = MagicMock()
    mock_service.get_pending_vaccinations.return_value = []

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_vaccinations(
            calendar=mock_calendar, service=mock_service, language="en"
        )

    mock_calendar.create_event.assert_not_called()
    mock_service.update_vaccination_status.assert_not_called()

    assert "no new vaccinations were found" in caplog.text


def test_list_vaccinations_handles_pet_has_owner(caplog):
    """List pending vaccinations"""

    caplog.set_level("INFO")
    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.VaccinationService.get_pending_vaccinations",
            return_value=[vaccination()],
        ),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_vaccinations(calendar=mock_calendar, language="en")

    mock_calendar.create_event.assert_called_once()
    expected_description = "Jose - Vaccination appointment for Sora"
    assert expected_description in caplog.text


def test_list_vaccinations_handles_pet_has_adopter(caplog):
    """List pending vaccinations"""

    caplog.set_level("INFO")
    adopter = User(
        id=2,
        username="sofiaD",
        first_name="Sofia",
        last_name="Morales",
        email="sofia@vetlog.org",
        mobile="0987654321",
        role="USER",
    )

    pet = Pet(
        id=1,
        user_id=1,
        adopter_id=2,
        name="Sora",
        birth_date=datetime(2020, 1, 1, 0, 0, 0),
        breed_id=1,
        status="ADOPTED",
        uuid="pet-uuid",
    )

    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.VaccinationService.get_pending_vaccinations",
            return_value=[vaccination()],
        ),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet),
        patch(
            "vetlog_calendar.main.UserRepository.find_by_id", return_value=adopter
        ) as mock_find_user_by_id,
    ):
        main.list_vaccinations(calendar=mock_calendar, language="en")

    mock_find_user_by_id.assert_called_with(pet.adopter_id)
    mock_calendar.create_event.assert_called_once()
    expected_description = "Sofia - Vaccination appointment for Sora"
    assert expected_description in caplog.text


def test_list_dewormings_processes_inactive_pet():
    """Produce deworming calendar event for INACTIVE pets"""

    inactive_pet = Pet(
        id=1,
        user_id=1,
        adopter_id=None,
        name="Sora",
        birth_date=datetime(2020, 1, 1, 0, 0, 0),
        breed_id=1,
        status="INACTIVE",
        uuid="pet-uuid",
        going_out_often=True,
    )

    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()
    mock_service = MagicMock()
    deworming_instance = deworming()
    mock_service.get_pending_dewormings.return_value = [deworming_instance]

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.PetRepository.find_by_id", return_value=inactive_pet
        ),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_dewormings(
            calendar=mock_calendar, service=mock_service, language="en"
        )

    mock_calendar.create_event.assert_called_once()
    mock_service.update_vaccination_status.assert_called_once_with(deworming_instance)


def test_list_dewormings_processes_deceased_pet():
    """Produce deworming calendar event for DECEASED pets"""

    deceased_pet = Pet(
        id=1,
        user_id=1,
        adopter_id=None,
        name="Sora",
        birth_date=datetime(2020, 1, 1, 0, 0, 0),
        breed_id=1,
        status="DECEASED",
        uuid="pet-uuid",
        going_out_often=True,
    )

    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()
    mock_service = MagicMock()
    deworming_instance = deworming()
    mock_service.get_pending_dewormings.return_value = [deworming_instance]

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.PetRepository.find_by_id", return_value=deceased_pet
        ),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_dewormings(
            calendar=mock_calendar, service=mock_service, language="en"
        )

    mock_calendar.create_event.assert_called_once()
    mock_service.update_vaccination_status.assert_called_once_with(deworming_instance)


def test_list_pets_prints_pending_vaccinations(caplog):
    """List all owners/adopters with pets waiting for vaccination"""

    caplog.set_level("INFO")
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.VaccinationService.get_pending_vaccinations",
            return_value=[vaccination()],
        ),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_pets()

    expected_output = "Owner: Jose Morales, Pet: Sora, awaiting vaccination"
    assert expected_output in caplog.text


def test_prints_pending_dewormings(caplog):
    """List pets with pending dewormings"""

    caplog.set_level("INFO")
    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch(
            "vetlog_calendar.main.VaccinationService.get_pending_dewormings",
            return_value=[deworming()],
        ),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
    ):
        main.list_dewormings(calendar=mock_calendar, language="en")

    expected_output = "Jose - Deworming appointment for Sora"
    assert expected_output in caplog.text


def test_list_dewormings_calls_update_vaccination_status(mock_env_vars):
    """update_vaccination_status is called after creating a deworming calendar event"""
    mock_session_cm = MagicMock()
    mock_calendar = MagicMock()
    mock_service = MagicMock()
    deworming_instance = deworming()
    mock_service.get_pending_dewormings.return_value = [deworming_instance]

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch("vetlog_calendar.main.PetRepository.find_by_id", return_value=pet()),
        patch("vetlog_calendar.main.UserRepository.find_by_id", return_value=owner()),
    ):
        main.list_dewormings(
            calendar=mock_calendar, service=mock_service, language="en"
        )

    mock_calendar.create_event.assert_called_once()
    mock_service.update_vaccination_status.assert_called_once_with(deworming_instance)


def test_settings_missing_required_vars(clean_env):
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_list_deworming_delegates_to_list_dewormings():
    """list_deworming() CLI entry point delegates to list_dewormings()"""
    with patch("vetlog_calendar.main.list_dewormings") as mock:
        main.list_dewormings(language="en")
    mock.assert_called_once()
