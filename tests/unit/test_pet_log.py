# Copyright 2026 Jose Morales contact@josdem.io
# Licensed under the Apache License, Version 2.0

import pytest
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine

from vetlog_calendar.pets.model import PetLog
from vetlog_calendar.pets.model import Pet
from vetlog_calendar.pets.repository import PetRepository # Assuming this is your path
from vetlog_calendar.pets.service import PetService

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_get_logs_by_date_range_success(session: Session):
    repo = PetRepository(session)
    service = PetService(repo)
    
    #medical logs
    log1 = PetLog(pet_id=1, log_date=datetime(2026, 6, 1), description="Routine Checkup", veterinarian="Dr. Joe")
    log2 = PetLog(pet_id=1, log_date=datetime(2026, 6, 5), description="Rabies Vaccination", veterinarian="Dr. Joe")
    log3 = PetLog(pet_id=1, log_date=datetime(2026, 6, 15), description="Future Appointment Log", veterinarian="Dr. Joe")
    
    session.add_all([log1, log2, log3])
    session.commit()

    start = datetime(2026, 6, 1)
    end = datetime(2026, 6, 10)
    results = service.get_logs_by_date_range(start, end)

    assert len(results) == 2
    assert results[0].description == "Routine Checkup"
    assert results[1].description == "Rabies Vaccination"

def test_get_logs_by_invalid_date_range(session: Session):
    repo = PetRepository(session)
    service = PetService(repo)
    
    start = datetime(2026, 6, 10)
    end = datetime(2026, 6, 1) # Invalid bounds

    with pytest.raises(ValueError, match="Start date cannot be after end date."):
        service.get_logs_by_date_range(start, end)