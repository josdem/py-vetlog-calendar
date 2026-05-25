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
#  limitations under the License

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlmodel import Session

from vetlog_calendar.vaccinations.model import Vaccination
from vetlog_calendar.vaccinations.repository import VaccinationRepository


def test_find_pending_vaccinations():
    session = MagicMock(spec=Session)
    repository = VaccinationRepository(session)
    vaccination = Vaccination(
        id=1,
        pet_id=1,
        name="Rabies",
        date=datetime.now(),
        status="NEW",
    )
    session.exec.return_value.all.return_value = [vaccination]
    pending_vaccinations = repository.find_pending_vaccinations()
    session.exec.assert_called_once()
    statement = session.exec.call_args.args[0]
    compiled_statement = statement.compile()
    statement_text = str(compiled_statement)
    assert "status" in statement_text
    assert "name" in statement_text
    assert "!=" in statement_text or "<>" in statement_text
    assert any(value == "NEW" for value in compiled_statement.params.values())
    assert any(value == "Deworming" for value in compiled_statement.params.values())
    assert len(pending_vaccinations) == 1
    assert pending_vaccinations[0].id == vaccination.id
    assert pending_vaccinations[0].status == "NEW"


def test_find_pending_dewormings():
    session = MagicMock(spec=Session)
    repository = VaccinationRepository(session)
    vaccination = Vaccination(
        id=1,
        pet_id=1,
        name="Deworming",
        date=datetime.now() - timedelta(days=30),
        status="NEW",
    )
    session.exec.return_value.all.return_value = [vaccination]
    pending_dewormings = repository.find_pending_dewormings()
    session.exec.assert_called_once()
    statement = session.exec.call_args.args[0]
    compiled_statement = statement.compile()
    statement_text = str(compiled_statement)
    assert "status" in statement_text
    assert "name" in statement_text
    assert any(value == "NEW" for value in compiled_statement.params.values())
    assert any(value == "Deworming" for value in compiled_statement.params.values())
    assert len(pending_dewormings) == 1
    assert pending_dewormings[0].id == vaccination.id
    assert pending_dewormings[0].status == "NEW"


def test_delete_rabies_vaccinations_for_pet():
    session = MagicMock(spec=Session)
    repository = VaccinationRepository(session)
    pet_id = 1
    repository.delete_rabies_vaccinations_for_pet(pet_id)
    session.exec.assert_called_once()
    statement = session.exec.call_args.args[0]
    compiled_statement = statement.compile()
    statement_text = str(compiled_statement)
    assert "pet_id" in statement_text
    assert "name" in statement_text
    assert any(value == pet_id for value in compiled_statement.params.values())
    assert any(value == "Rabies" for value in compiled_statement.params.values())
