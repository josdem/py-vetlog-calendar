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

from vetlog_calendar.pets.model import Pet, PetLog
from vetlog_calendar.pets.repository import PetRepository
from datetime import datetime
from typing import Sequence


class PetService:
    def __init__(self, repository: PetRepository) -> None:
        self.repository = repository

    def get_all(self):
        """Return all pets"""
        return self.repository.get_all()

    def get_by_id(self, id: int) -> Pet | None:
        """Return pet by id"""
        return self.repository.find_by_id(id)

    def get_logs_by_date_range(
        self, start_date: datetime, end_date: datetime, pet_id: int | None = None
    ) -> Sequence[PetLog]:
        """Return petlog"""
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")

        return self.repository.find_all_pet_logs(start_date, end_date, pet_id=pet_id)
