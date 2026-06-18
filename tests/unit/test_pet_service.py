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

import datetime

import pytest

from unittest.mock import MagicMock

from vetlog_calendar.pets.model import Pet
from vetlog_calendar.pets.service import PetService


@pytest.fixture
def mock_repo():
    return MagicMock()


def test_get_pets(mock_repo):
    """Get all pets"""
    service = PetService(repository=mock_repo)
    pets = [Pet(id=1, name="Sora")]
    mock_repo.get_all.return_value = pets
    assert service.get_all() == pets


def test_get_pet_by_id(mock_repo):
    """Get pet by id"""
    service = PetService(repository=mock_repo)
    pet = Pet(id=1, name="Sora")
    mock_repo.find_by_id.return_value = pet
    assert service.get_by_id(1) == pet
    mock_repo.find_by_id.assert_called_once_with(1)


def test_get_logs_by_date_range_invalid_dates(mock_repo):
    """Get pet logs by date range with invalid dates"""
    service = PetService(repository=mock_repo)
    with pytest.raises(ValueError, match="Start date cannot be after end date."):
        service.get_logs_by_date_range(
            start_date=datetime.datetime(2024, 1, 2),
            end_date=datetime.datetime(2024, 1, 1),
        )


def test_get_logs_by_date_range(mock_repo):
    """Get pet logs by date range"""
    service = PetService(repository=mock_repo)
    start_date = datetime.datetime(2024, 1, 1)
    end_date = datetime.datetime(2024, 1, 31)
    pet_id = 1
    logs = [MagicMock()]
    mock_repo.find_all_pet_logs.return_value = logs
    assert service.get_logs_by_date_range(start_date, end_date, pet_id) == logs
    mock_repo.find_all_pet_logs.assert_called_once_with(
        start_date, end_date, pet_id=pet_id
    )
