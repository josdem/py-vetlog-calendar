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


class Locale:
    """Locale class"""

    def __init__(self, language: str = "en"):
        self.language = language

    def get_event_title(self, owner: str, pet: str) -> str:
        """Get the event title based on language"""
        if self.language == "es":
            return f"{owner} - Cita de vacunación para {pet}"
        return f"{owner} - Vaccination appointment for {pet}"

    def get_deworming_event_title(self, owner: str, pet: str) -> str:
        """Get the deworming event title based on language"""
        if self.language == "es":
            return f"{owner} - Cita de desparasitación para {pet}"
        return f"{owner} - Deworming appointment for {pet}"

    def get_pet_info(self, pet: str) -> str:
        """Get the pet info based on language"""
        if self.language == "es":
            return f"Cita de vacunación para {pet}"
        return f"Vaccination appointment for {pet}"

    def get_event_location(self) -> str:
        """Get the event location based on language"""
        if self.language == "es":
            return "La que mejor funcione para ambos"
        return "Whatever works for you"

    def get_event_thanks(self) -> str:
        """Get the event thanks message based on language"""
        if self.language == "es":
            return "¡Gracias por confiar en Vetlog!"
        return "Thank you for trusting Vetlog!"

    def get_description_note(self) -> str:
        """Get the description note based on language"""
        if self.language == "es":
            return "Favor de dar seguimiento usando WhatsApp."
        return "Please follow up by phone."

    def get_deworming_description(self, pet: str, date: str) -> str:
        """Get the deworming description based on language"""
        if self.language == "es":
            return f"Favor de validar cita de desparasitación para {pet} desde que la reciente fue: {date}\n"
        return f"Please validate deworming appointment for pet {pet} since the last deworming was: {date}\n"

    VACCINE_TRANSLATIONS = {
        "Rabies": "Rabia",
    }

    def get_vaccine_type(self, name: str) -> str:
        """Get the vaccine type, translated if language is Spanish"""
        if self.language == "es":
            return f"Dosis: {self.VACCINE_TRANSLATIONS.get(name, name)}"
        return f"Vaccine type: {name}"
