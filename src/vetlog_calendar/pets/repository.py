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
from sqlmodel import Session, select
from datetime import datetime
from vetlog_calendar.pets.model import Pet
from vetlog_calendar.pets.model import PetLog


class PetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> Sequence[Pet]:
        return self.session.exec(select(Pet)).all()

    def find_by_id(self, id: int) -> Pet | None:
        return self.session.exec(select(Pet).where(Pet.id == id)).one_or_none()

    def find_all_pet_logs(
        self, start_date: datetime, end_date: datetime, pet_id: int | None = None
    ) -> Sequence[PetLog]:
        if pet_id is None:
            return []
        statement = (
            select(PetLog)
            .where(
                PetLog.date_created >= start_date,
                PetLog.date_created <= end_date,
                PetLog.pet_id == pet_id,
            )
            .order_by(PetLog.date_created)
        )
        results = self.session.exec(statement)
        return results.all()
