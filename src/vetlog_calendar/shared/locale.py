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
            return "Nota: Favor de dar seguimiento usando WhatsApp."
        return "Note: Please follow up by phone."

    def get_deworming_description(self, pet: str, date: str) -> str:
        """Get the deworming description based on language"""
        if self.language == "es":
            return f"Favor de validar cita de desparasitación para {pet} desde que la reciente fue: {date}\n"
        return f"Please validate deworming appointment for pet {pet} since the last deworming was: {date}\n"

    VACCINE_TRANSLATIONS = {
        "Rabies": "Rabia",
    }

    def get_vaccine_type(self, name: str) -> str:
        """Get the vaccine type line (localized label + translated name), including a trailing newline."""
        if self.language == "es":
            return f"Dosis: {self.VACCINE_TRANSLATIONS.get(name, name)}\n"
        return f"Vaccine type: {name}\n"

    def get_missing_pet_logs_event_title(self) -> str:
        """Get the missing pet logs event title based on language"""
        if self.language == "es":
            return "Médico - Registros de mascota pendientes"
        return "Doctor - Missing pet logs"

    def get_doctor_info(self) -> str:
        """Get the doctor info based on language"""
        if self.language == "es":
            return "Estimad@ Médico,\n"
        return "Dear Doctor,\n"

    def get_pet_logs_info_header(self) -> str:
        """Get the pet logs info header based on language"""
        if self.language == "es":
            return "Nuestros registros muestran que no tenemos registros médicos y tuvimos las siguiente cirugías en la semana previa.\n"
        return "Our records show that we have missing medical logs and we had the following surgeries in the precvious week.\n"

    def get_pet_logs_info_footer(self) -> str:
        """Get the pet logs info footer based on language"""
        if self.language == "es":
            return "Favor de crear esos registros médicos en cuanto sea posible.\n"
        return "Please create those medical logs as soon as possible.\n"
