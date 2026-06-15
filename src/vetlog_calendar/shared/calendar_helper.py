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

from datetime import datetime
from typing import Optional

from . import date_helper

from vetlog_calendar.pets.model import Pet
from vetlog_calendar.shared.locale import Locale
from vetlog_calendar.users.model import User
from vetlog_calendar.vaccinations.model import Vaccination

from .config import get_settings


class Helper:
    def __init__(
        self,
        pet: Optional[Pet] = None,
        vaccination: Optional[Vaccination] = None,
        owner: Optional[User] = None,
        language: str = "en",
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
        description_info = f"{owner_info}\n{pet_info}\n{vaccine_type_info}\n{thank_you_info}\n{website_info}"
        if self.owner.email.lower().endswith("@vetlog.org"):
            description_info = f"{owner_info}\n{pet_info}\n{vaccine_type_info}\n{self.locale.get_description_note()}\n\n{thank_you_info}\n{website_info}"
        event = {
            "summary": self.__get_event_title(),
            "location": self.locale.get_event_location(),
            "description": description_info,
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
        return event

    def get_deworming_event(self) -> dict:
        owner_info = (
            f"{self.owner.first_name} {self.owner.last_name}\n{self.owner.mobile}\n"
        )
        validated_date = date_helper.validate_date(self.vaccination.date)
        last_deworming_date = date_helper.get_last_deworming_date(
            self.vaccination.date, self.pet.going_out_often
        )
        description_info = self.locale.get_deworming_description(
            pet=self.pet.name, date=last_deworming_date.strftime("%Y-%m-%d")
        )
        thank_you_info = self.locale.get_event_thanks()
        website_info = "https://vetlog.org/"
        body_info = (
            f"{owner_info}\n{description_info}\n{thank_you_info}\n{website_info}"
        )
        if self.owner.email.lower().endswith("@vetlog.org"):
            body_info = f"{owner_info}\n{description_info}\n{self.locale.get_description_note()}\n\n{thank_you_info}\n{website_info}"
        event = {
            "summary": self.__get_deworming_event_title(),
            "location": self.locale.get_event_location(),
            "description": body_info,
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
        return event

    def get_missing_pet_logs_event(self, surgeries: list) -> dict:
        doctor_info = self.locale.get_doctor_info()
        pet_logs_info_header = self.locale.get_pet_logs_info_header()
        surgery_list = "\n".join(
            [
                f"- {surgery['summary']} on {surgery['start']['dateTime']}"
                for surgery in surgeries
            ]
        )
        pet_logs_info_footer = self.locale.get_pet_logs_info_footer()
        thank_you_info = self.locale.get_event_thanks()
        website_info = "https://vetlog.org/"
        body_info = f"{doctor_info}\n{pet_logs_info_header}\n{surgery_list}\n\n{pet_logs_info_footer}\n{thank_you_info}\n{website_info}"
        event = {
            "summary": self.locale.get_missing_pet_logs_event_title(),
            "location": self.locale.get_event_location(),
            "description": body_info,
            "start": {
                "dateTime": f"{(datetime.now()).strftime('%Y-%m-%d')}T12:00:00-06:00",
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": f"{(datetime.now()).strftime('%Y-%m-%d')}T12:15:00-06:00",
                "timeZone": "UTC",
            },
            "attendees": [
                *[{"email": email} for email in get_settings().DEFAULT_EMAILS],
            ],
        }
        return event
