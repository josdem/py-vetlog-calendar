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

from typing import Sequence
from sqlmodel import Session, delete, select, update

from vetlog_calendar.vaccinations.model import Vaccination, VaccineType


class VaccinationRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_pending_vaccinations(self) -> Sequence[Vaccination]:
        stmt = select(Vaccination).where(
            (Vaccination.status == "NEW") & (Vaccination.name != VaccineType.DEWORMING)
        )
        return self.session.exec(stmt).all()

    def find_pending_dewormings(self) -> Sequence[Vaccination]:
        stmt = select(Vaccination).where(
            (Vaccination.status == "NEW") & (Vaccination.name == VaccineType.DEWORMING)
        )
        return self.session.exec(stmt).all()

    def update_vaccination_status(self, vaccination: Vaccination):
        stmt = (
            update(Vaccination)
            .where(Vaccination.id == vaccination.id)
            .values(status="PENDING")
        )
        self.session.exec(stmt)
        self.session.commit()

    def delete_rabies_vaccinations_for_pet(self, pet_id: int):
        stmt = delete(Vaccination).where(
            (Vaccination.pet_id == pet_id)
            & (Vaccination.name == VaccineType.RABIES)
            & (Vaccination.status == "PENDING")
        )
        self.session.exec(stmt)
        self.session.commit()
