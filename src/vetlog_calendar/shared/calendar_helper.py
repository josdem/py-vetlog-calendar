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

from . import date_helper

from vetlog_calendar.pets.model import Pet
from vetlog_calendar.shared.locale import Locale
from vetlog_calendar.users.model import User
from vetlog_calendar.vaccinations.model import Vaccination

from .config import get_settings


class Helper:
    def __init__(
        self, pet: Pet, vaccination: Vaccination, owner: User, language: str = "en"
    ):
        self.pet = pet
        self.vaccination = vaccination
        self.owner = owner
        self.locale = Locale(language)

    def __get_event_title(self) -> str:
        owner_name = self.owner.first_name or self.owner.username
        return self.locale.get_event_title(owner=owner_name, pet=self.pet.name)

    def __get_deworming_event_title(self) -> str:
        owner_name = self.owner.first_name or self.owner.username
        return self.locale.get_deworming_event_title(
            owner=owner_name, pet=self.pet.name
        )

    def get_vaccination_event(self) -> dict:
        owner_info = (
            f"{self.owner.first_name} {self.owner.last_name}\n{self.owner.mobile}\n"
        )
        pet_info = self.locale.get_pet_info(pet=self.pet.name)
        vaccine_type_info = self.locale.get_vaccine_type(self.vaccination.name)
        thank_you_info = self.locale.get_event_thanks()
        website_info = "https://vetlog.org/"
        validated_date = date_helper.validate_date(self.vaccination.date)
        event = {
            "summary": self.__get_event_title(),
            "location": self.locale.get_event_location(),
            "description": f"{owner_info}\n{pet_info}\n{vaccine_type_info}\n{thank_you_info}\n{website_info}",
            "start": {
                "dateTime": f"{validated_date.strftime('%Y-%m-%d')}T11:00:00-06:00",
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": f"{validated_date.strftime('%Y-%m-%d')}T11:15:00-06:00",
                "timeZone": "UTC",
            },
            "attendees": [
                {"email": self.owner.email},
                *[{"email": email} for email in get_settings().DEFAULT_EMAILS],
            ],
        }
        if self.owner.email.lower().endswith("@vetlog.org"):
            event["note"] = self.locale.get_description_note()
        return event

    def get_deworming_event(self) -> dict:
        owner_info = (
            f"{self.owner.first_name} {self.owner.last_name}\n{self.owner.mobile}\n"
        )
        validated_date = date_helper.validate_date(self.vaccination.date)
        last_deworming_date = date_helper.get_last_deworming_date(self.vaccination.date, self.pet.going_out_often)
        description_info = self.locale.get_deworming_description(
            pet=self.pet.name, date=last_deworming_date.strftime("%Y-%m-%d")
        )
        thank_you_info = self.locale.get_event_thanks()
        website_info = "https://vetlog.org/"
        event = {
            "summary": self.__get_deworming_event_title(),
            "location": self.locale.get_event_location(),
            "description": f"{owner_info}\n{description_info}\n{thank_you_info}\n{website_info}",
            "start": {
                "dateTime": f"{validated_date.strftime('%Y-%m-%d')}T12:00:00-06:00",
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": f"{validated_date.strftime('%Y-%m-%d')}T12:15:00-06:00",
                "timeZone": "UTC",
            },
            "attendees": [
                *[{"email": email} for email in get_settings().DEFAULT_EMAILS],
            ],
        }
        if self.owner.email.lower().endswith("@vetlog.org"):
            event["note"] = self.locale.get_description_note()
        return event
