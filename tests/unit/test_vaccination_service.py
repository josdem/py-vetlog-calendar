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

import pytest

from datetime import datetime
from unittest.mock import MagicMock

from vetlog_calendar.vaccinations.model import Vaccination
from vetlog_calendar.vaccinations.service import VaccinationService


@pytest.fixture
def mock_repo():
    return MagicMock()


def test_get_vaccinations(mock_repo):
    """Get pending vaccinations"""
    service = VaccinationService(repository=mock_repo)
    vaccinations = [
        Vaccination(
            id=1, name="Rabies", date=datetime(2026, 4, 21), pet_id=2, status="NEW"
        )
    ]
    mock_repo.find_pending_vaccinations.return_value = vaccinations
    assert service.get_pending_vaccinations() == vaccinations
    mock_repo.find_pending_vaccinations.assert_called_once_with()


def test_get_dewormings(mock_repo):
    """Get pending dewormings"""
    service = VaccinationService(repository=mock_repo)
    dewormings = [
        Vaccination(
            id=1,
            name="Deworming",
            date=datetime(2026, 4, 21),
            pet_id=2,
            status="NEW",
        )
    ]
    mock_repo.find_pending_dewormings.return_value = dewormings
    assert service.get_pending_dewormings() == dewormings
    mock_repo.find_pending_dewormings.assert_called_once()


def test_update_vaccination_status(mock_repo):
    """Update vaccination status to PENDING"""
    service = VaccinationService(repository=mock_repo)
    vaccination = Vaccination(
        id=1, name="Rabies", date=datetime(2026, 4, 21), pet_id=2, status="NEW"
    )
    service.update_vaccination_status(vaccination)
    mock_repo.update_vaccination_status.assert_called_once_with(vaccination)


def test_delete_rabies_vaccinations_for_pet(mock_repo):
    """Delete rabies vaccinations for pet"""
    service = VaccinationService(repository=mock_repo)
    pet_id = 2
    service.delete_rabies_vaccinations_for_pet(pet_id)
    mock_repo.delete_rabies_vaccinations_for_pet.assert_called_once_with(pet_id)
